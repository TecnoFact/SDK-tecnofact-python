"""CFDI 4.0 XML builder for comprobante types I (Ingreso) and E (Egreso).

Generates the SAT-compliant XML string required by CfdiService.timbrar().
The produced XML follows the namespace and attribute ordering mandated by the
SAT Anexo 20 (version 4.0) schema.

Usage::

    from tecnofact.xml import CfdiXmlBuilder
    from tecnofact.models import Cfdi4Request, Emisor, Receptor, Concepto
    from decimal import Decimal

    request = Cfdi4Request(
        emisor=Emisor(rfc="AAA010101AAA", nombre="Mi Empresa", regimen_fiscal="601", cp="06300"),
        receptor=Receptor(
            rfc="XAXX010101000",
            nombre="Publico General",
            uso_cfdi="S01",
            domicilio_fiscal_receptor="06300",
            regimen_fiscal_receptor="616",
        ),
        conceptos=[
            Concepto(
                clave_prod_serv="01010101",
                cantidad=Decimal("1"),
                clave_unidad="E48",
                descripcion="Servicio",
                valor_unitario=Decimal("100.00"),
                importe=Decimal("100.00"),
                objeto_imp="01",
            )
        ],
        tipo_comprobante="I",
        forma_pago="01",
        metodo_pago="PUE",
        moneda="MXN",
        subtotal=Decimal("100.00"),
        total=Decimal("100.00"),
        lugar_expedicion="06300",
    )

    builder = CfdiXmlBuilder()
    xml_string = builder.build(request)
"""

import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from decimal import Decimal
from typing import Optional

from ..models.cfdi4_request import Cfdi4Request
from ..models.concepto import Concepto
from ..models.impuestos import Impuestos
from ..models.impuestos_concepto import ImpuestosConcepto
from ..models.cfdi_relacionados import CfdiRelacionados


_CFDI_NS = "http://www.sat.gob.mx/cfd/4"
_XSI_NS = "http://www.w3.org/2001/XMLSchema-instance"
_SCHEMA_LOCATION = (
    "http://www.sat.gob.mx/cfd/4 "
    "http://www.sat.gob.mx/sitio_internet/cfd/4/cfdv40.xsd"
)

# Allowed TipoDeComprobante values for this builder
_SUPPORTED_TYPES = {"I", "E"}


class CfdiXmlBuilder:
    """Builds a CFDI 4.0 XML string from a :class:`~tecnofact.models.Cfdi4Request`."""

    def build(self, request: Cfdi4Request) -> str:
        """Return the UTF-8 XML string (without XML declaration) for stamping.

        :param request: A fully populated :class:`Cfdi4Request`.
        :raises ValueError: If ``tipo_comprobante`` is not ``"I"`` or ``"E"``.
        """
        if request.tipo_comprobante not in _SUPPORTED_TYPES:
            raise ValueError(
                f"CfdiXmlBuilder only supports TipoDeComprobante I and E, "
                f"got '{request.tipo_comprobante}'"
            )

        ET.register_namespace("cfdi", _CFDI_NS)
        ET.register_namespace("xsi", _XSI_NS)

        comprobante = self._build_comprobante(request)
        self._append_cfdi_relacionados(comprobante, request)
        self._append_emisor(comprobante, request)
        self._append_receptor(comprobante, request)
        self._append_conceptos(comprobante, request)
        self._append_impuestos_globales(comprobante, request)

        return ET.tostring(comprobante, encoding="unicode", xml_declaration=False)

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    def _fmt(self, value: Decimal, decimals: int = 2) -> str:
        return f"{value:.{decimals}f}"

    def _now_iso(self) -> str:
        """Return current UTC time formatted as SAT expects: 2024-01-15T12:00:00."""
        now = datetime.now(timezone.utc).replace(microsecond=0)
        return now.strftime("%Y-%m-%dT%H:%M:%S")

    def _build_comprobante(self, r: Cfdi4Request) -> ET.Element:
        attrib = {
            f"{{{_XSI_NS}}}schemaLocation": _SCHEMA_LOCATION,
            "Version": "4.0",
            "Fecha": r.fecha or self._now_iso(),
            "Sello": "",  # PAC fills this during timbrado
            "FormaPago": r.forma_pago,
            "NoCertificado": "",  # PAC fills this
            "Certificado": "",    # PAC fills this
            "SubTotal": self._fmt(r.subtotal),
            "Moneda": r.moneda,
            "Total": self._fmt(r.total),
            "TipoDeComprobante": r.tipo_comprobante,
            "Exportacion": r.exportacion,
            "MetodoPago": r.metodo_pago,
            "LugarExpedicion": r.lugar_expedicion or "",
        }

        if r.serie:
            attrib["Serie"] = r.serie
        if r.folio:
            attrib["Folio"] = r.folio
        if r.tipo_cambio is not None:
            attrib["TipoCambio"] = self._fmt(r.tipo_cambio, decimals=6)
        if r.descuento is not None:
            attrib["Descuento"] = self._fmt(r.descuento)
        if r.condiciones_pago:
            attrib["CondicionesDePago"] = r.condiciones_pago

        return ET.Element(f"{{{_CFDI_NS}}}Comprobante", attrib)

    def _append_cfdi_relacionados(
        self, parent: ET.Element, r: Cfdi4Request
    ) -> None:
        if not r.cfdi_relacionados:
            return
        for grupo in r.cfdi_relacionados:
            relacionados_el = ET.SubElement(
                parent,
                f"{{{_CFDI_NS}}}CfdiRelacionados",
                {"TipoRelacion": grupo.tipo_relacion},
            )
            for uuid in grupo.uuids:
                ET.SubElement(
                    relacionados_el,
                    f"{{{_CFDI_NS}}}CfdiRelacionado",
                    {"UUID": uuid},
                )

    def _append_emisor(self, parent: ET.Element, r: Cfdi4Request) -> None:
        ET.SubElement(
            parent,
            f"{{{_CFDI_NS}}}Emisor",
            {
                "Rfc": r.emisor.rfc,
                "Nombre": r.emisor.nombre,
                "RegimenFiscal": r.emisor.regimen_fiscal,
            },
        )

    def _append_receptor(self, parent: ET.Element, r: Cfdi4Request) -> None:
        attrib = {
            "Rfc": r.receptor.rfc,
            "Nombre": r.receptor.nombre,
            "DomicilioFiscalReceptor": r.receptor.domicilio_fiscal_receptor,
            "RegimenFiscalReceptor": r.receptor.regimen_fiscal_receptor,
            "UsoCFDI": r.receptor.uso_cfdi,
        }
        if r.receptor.residencia_fiscal:
            attrib["ResidenciaFiscal"] = r.receptor.residencia_fiscal
        if r.receptor.num_reg_id_trib:
            attrib["NumRegIdTrib"] = r.receptor.num_reg_id_trib

        ET.SubElement(parent, f"{{{_CFDI_NS}}}Receptor", attrib)

    def _append_conceptos(self, parent: ET.Element, r: Cfdi4Request) -> None:
        conceptos_el = ET.SubElement(parent, f"{{{_CFDI_NS}}}Conceptos")
        for concepto in r.conceptos:
            self._append_concepto(conceptos_el, concepto)

    def _append_concepto(self, parent: ET.Element, c: Concepto) -> None:
        attrib = {
            "ClaveProdServ": c.clave_prod_serv,
            "Cantidad": self._fmt(c.cantidad, decimals=6).rstrip("0").rstrip(".") or "0",
            "ClaveUnidad": c.clave_unidad,
            "Descripcion": c.descripcion,
            "ValorUnitario": self._fmt(c.valor_unitario),
            "Importe": self._fmt(c.importe),
            "ObjetoImp": c.objeto_imp,
        }
        if c.no_identificacion:
            attrib["NoIdentificacion"] = c.no_identificacion
        if c.unidad:
            attrib["Unidad"] = c.unidad
        if c.descuento is not None:
            attrib["Descuento"] = self._fmt(c.descuento)

        concepto_el = ET.SubElement(parent, f"{{{_CFDI_NS}}}Concepto", attrib)

        if c.informacion_aduanera:
            for ia in c.informacion_aduanera:
                ET.SubElement(
                    concepto_el,
                    f"{{{_CFDI_NS}}}InformacionAduanera",
                    {"NumeroPedimento": ia.numero_pedimento},
                )

        if c.cuenta_predial:
            ET.SubElement(
                concepto_el,
                f"{{{_CFDI_NS}}}CuentaPredial",
                {"Numero": c.cuenta_predial.numero},
            )

        if c.partes:
            for parte in c.partes:
                parte_attrib = {
                    "ClaveProdServ": parte.clave_prod_serv,
                    "Cantidad": self._fmt(parte.cantidad, decimals=6).rstrip("0").rstrip(".") or "0",
                }
                if parte.unidad:
                    parte_attrib["Unidad"] = parte.unidad
                if parte.descripcion:
                    parte_attrib["Descripcion"] = parte.descripcion
                if parte.valor_unitario is not None:
                    parte_attrib["ValorUnitario"] = self._fmt(parte.valor_unitario)
                if parte.importe is not None:
                    parte_attrib["Importe"] = self._fmt(parte.importe)

                parte_el = ET.SubElement(
                    concepto_el,
                    f"{{{_CFDI_NS}}}Parte",
                    parte_attrib,
                )
                if parte.informacion_aduanera:
                    for ia in parte.informacion_aduanera:
                        ET.SubElement(
                            parte_el,
                            f"{{{_CFDI_NS}}}InformacionAduanera",
                            {"NumeroPedimento": ia.numero_pedimento},
                        )

        if c.impuestos:
            self._append_impuestos_concepto(concepto_el, c.impuestos)

    def _append_impuestos_concepto(
        self, parent: ET.Element, imp: ImpuestosConcepto
    ) -> None:
        imp_el = ET.SubElement(parent, f"{{{_CFDI_NS}}}Impuestos")

        if imp.traslados:
            traslados_el = ET.SubElement(imp_el, f"{{{_CFDI_NS}}}Traslados")
            for t in imp.traslados:
                attrib = {
                    "Base": self._fmt(t.base),
                    "Impuesto": t.impuesto,
                    "TipoFactor": t.tipo_factor,
                    "TasaOCuota": self._fmt(t.tasa_o_cuota, decimals=6),
                }
                if t.importe is not None:
                    attrib["Importe"] = self._fmt(t.importe)
                ET.SubElement(traslados_el, f"{{{_CFDI_NS}}}Traslado", attrib)

        if imp.retenciones:
            retenciones_el = ET.SubElement(imp_el, f"{{{_CFDI_NS}}}Retenciones")
            for r in imp.retenciones:
                ET.SubElement(
                    retenciones_el,
                    f"{{{_CFDI_NS}}}Retencion",
                    {
                        "Base": self._fmt(r.base),
                        "Impuesto": r.impuesto,
                        "TipoFactor": r.tipo_factor,
                        "TasaOCuota": self._fmt(r.tasa_o_cuota, decimals=6),
                        "Importe": self._fmt(r.importe),
                    },
                )

    def _append_impuestos_globales(
        self, parent: ET.Element, r: Cfdi4Request
    ) -> None:
        if not r.impuestos:
            return

        imp = r.impuestos
        attrib = {}
        if imp.total_impuestos_trasladados is not None:
            attrib["TotalImpuestosTrasladados"] = self._fmt(imp.total_impuestos_trasladados)
        if imp.total_impuestos_retenidos is not None:
            attrib["TotalImpuestosRetenidos"] = self._fmt(imp.total_impuestos_retenidos)

        imp_el = ET.SubElement(parent, f"{{{_CFDI_NS}}}Impuestos", attrib)

        if imp.retenciones:
            retenciones_el = ET.SubElement(imp_el, f"{{{_CFDI_NS}}}Retenciones")
            for ret in imp.retenciones:
                ET.SubElement(
                    retenciones_el,
                    f"{{{_CFDI_NS}}}Retencion",
                    {
                        "Impuesto": ret.impuesto,
                        "Importe": self._fmt(ret.importe),
                    },
                )

        if imp.traslados:
            traslados_el = ET.SubElement(imp_el, f"{{{_CFDI_NS}}}Traslados")
            for tras in imp.traslados:
                ET.SubElement(
                    traslados_el,
                    f"{{{_CFDI_NS}}}Traslado",
                    {
                        "Impuesto": tras.impuesto,
                        "TipoFactor": tras.tipo_factor,
                        "TasaOCuota": self._fmt(tras.tasa_o_cuota, decimals=6),
                        "Importe": self._fmt(tras.importe),
                    },
                )
