import pytest
from decimal import Decimal
from tecnofact.models import (
    Emisor,
    Receptor,
    Concepto,
    ImpuestosConcepto,
    Traslado,
    Retencion,
    TrasladoGlobal,
    RetencionGlobal,
    Impuestos,
    CfdiRelacionados,
    Cfdi4Request,
    CuentaPredial,
    InformacionAduanera,
    Parte
)


class TestEmisor:
    def test_emisor_creation(self):
        emisor = Emisor(
            rfc="XAXX010101000",
            nombre="EMPRESA EMISORA SA DE CV",
            regimen_fiscal="601",
            cp="06300"
        )
        
        assert emisor.rfc == "XAXX010101000"
        assert emisor.nombre == "EMPRESA EMISORA SA DE CV"
        assert emisor.regimen_fiscal == "601"
        assert emisor.cp == "06300"

    def test_emisor_getters(self):
        emisor = Emisor(
            rfc="XAXX010101000",
            nombre="EMPRESA EMISORA SA DE CV",
            regimen_fiscal="601",
            cp="06300"
        )
        
        assert emisor.get_rfc() == "XAXX010101000"
        assert emisor.get_nombre() == "EMPRESA EMISORA SA DE CV"
        assert emisor.get_regimen_fiscal() == "601"
        assert emisor.get_cp() == "06300"

    def test_emisor_to_dict(self):
        emisor = Emisor(
            rfc="XAXX010101000",
            nombre="EMPRESA EMISORA SA DE CV",
            regimen_fiscal="601",
            cp="06300"
        )
        
        data = emisor.to_dict()
        
        assert data["rfc"] == "XAXX010101000"
        assert data["nombre"] == "EMPRESA EMISORA SA DE CV"
        assert data["regimen_fiscal"] == "601"
        assert data["cp"] == "06300"


class TestReceptor:
    def test_receptor_creation(self):
        receptor = Receptor(
            rfc="XAXX010101001",
            nombre="CLIENTE RECEPTOR",
            uso_cfdi="G03",
            domicilio_fiscal_receptor="06300",
            regimen_fiscal_receptor="612"
        )
        
        assert receptor.rfc == "XAXX010101001"
        assert receptor.nombre == "CLIENTE RECEPTOR"
        assert receptor.uso_cfdi == "G03"

    def test_receptor_with_optional_fields(self):
        receptor = Receptor(
            rfc="XAXX010101001",
            nombre="CLIENTE RECEPTOR",
            uso_cfdi="G03",
            domicilio_fiscal_receptor="06300",
            regimen_fiscal_receptor="612",
            residencia_fiscal="USA",
            num_reg_id_trib="123456"
        )
        
        assert receptor.residencia_fiscal == "USA"
        assert receptor.num_reg_id_trib == "123456"

    def test_receptor_to_dict(self):
        receptor = Receptor(
            rfc="XAXX010101001",
            nombre="CLIENTE RECEPTOR",
            uso_cfdi="G03",
            domicilio_fiscal_receptor="06300",
            regimen_fiscal_receptor="612"
        )
        
        data = receptor.to_dict()
        
        assert data["rfc"] == "XAXX010101001"
        assert data["nombre"] == "CLIENTE RECEPTOR"
        assert "residencia_fiscal" not in data


class TestTraslado:
    def test_traslado_creation(self):
        traslado = Traslado(
            base=Decimal("10000.00"),
            impuesto="002",
            tipo_factor="Tasa",
            tasa_o_cuota=Decimal("0.160000"),
            importe=Decimal("1600.00")
        )
        
        assert traslado.base == Decimal("10000.00")
        assert traslado.impuesto == "002"
        assert traslado.tipo_factor == "Tasa"

    def test_traslado_to_dict(self):
        traslado = Traslado(
            base=Decimal("10000.00"),
            impuesto="002",
            tipo_factor="Tasa",
            tasa_o_cuota=Decimal("0.160000"),
            importe=Decimal("1600.00")
        )
        
        data = traslado.to_dict()
        
        assert data["base"] == 10000.00
        assert data["impuesto"] == "002"
        assert data["tasa_o_cuota"] == "0.160000"
        assert data["importe"] == 1600.00


class TestRetencion:
    def test_retencion_creation(self):
        retencion = Retencion(
            base=Decimal("10000.00"),
            impuesto="001",
            tipo_factor="Tasa",
            tasa_o_cuota=Decimal("0.100000"),
            importe=Decimal("1000.00")
        )
        
        assert retencion.base == Decimal("10000.00")
        assert retencion.impuesto == "001"

    def test_retencion_to_dict(self):
        retencion = Retencion(
            base=Decimal("10000.00"),
            impuesto="001",
            tipo_factor="Tasa",
            tasa_o_cuota=Decimal("0.100000"),
            importe=Decimal("1000.00")
        )
        
        data = retencion.to_dict()
        
        assert data["base"] == 10000.00
        assert data["importe"] == 1000.00


class TestImpuestosConcepto:
    def test_impuestos_concepto_with_traslados(self):
        traslado = Traslado(
            base=Decimal("10000.00"),
            impuesto="002",
            tipo_factor="Tasa",
            tasa_o_cuota=Decimal("0.160000"),
            importe=Decimal("1600.00")
        )
        
        impuestos = ImpuestosConcepto(traslados=[traslado])
        
        assert len(impuestos.traslados) == 1
        assert impuestos.retenciones is None

    def test_impuestos_concepto_to_dict(self):
        traslado = Traslado(
            base=Decimal("10000.00"),
            impuesto="002",
            tipo_factor="Tasa",
            tasa_o_cuota=Decimal("0.160000"),
            importe=Decimal("1600.00")
        )
        
        impuestos = ImpuestosConcepto(traslados=[traslado])
        data = impuestos.to_dict()
        
        assert "traslados" in data
        assert len(data["traslados"]) == 1


class TestConcepto:
    def test_concepto_creation(self):
        concepto = Concepto(
            clave_prod_serv="01010101",
            cantidad=Decimal("1"),
            clave_unidad="E48",
            descripcion="Servicio de desarrollo",
            valor_unitario=Decimal("10000.00"),
            importe=Decimal("10000.00"),
            objeto_imp="02"
        )
        
        assert concepto.clave_prod_serv == "01010101"
        assert concepto.cantidad == Decimal("1")
        assert concepto.descripcion == "Servicio de desarrollo"

    def test_concepto_with_impuestos(self):
        traslado = Traslado(
            base=Decimal("10000.00"),
            impuesto="002",
            tipo_factor="Tasa",
            tasa_o_cuota=Decimal("0.160000"),
            importe=Decimal("1600.00")
        )
        
        impuestos = ImpuestosConcepto(traslados=[traslado])
        
        concepto = Concepto(
            clave_prod_serv="01010101",
            cantidad=Decimal("1"),
            clave_unidad="E48",
            descripcion="Servicio de desarrollo",
            valor_unitario=Decimal("10000.00"),
            importe=Decimal("10000.00"),
            objeto_imp="02",
            impuestos=impuestos
        )
        
        assert concepto.impuestos is not None
        assert len(concepto.impuestos.traslados) == 1

    def test_concepto_to_dict(self):
        concepto = Concepto(
            clave_prod_serv="01010101",
            cantidad=Decimal("1"),
            clave_unidad="E48",
            descripcion="Servicio de desarrollo",
            valor_unitario=Decimal("10000.00"),
            importe=Decimal("10000.00"),
            objeto_imp="02"
        )
        
        data = concepto.to_dict()
        
        assert data["clave_prod_serv"] == "01010101"
        assert data["cantidad"] == 1.0
        assert data["valor_unitario"] == 10000.00


class TestCfdiRelacionados:
    def test_cfdi_relacionados_creation(self):
        cfdi_rel = CfdiRelacionados(
            tipo_relacion="01",
            uuids=["UUID1", "UUID2"]
        )
        
        assert cfdi_rel.tipo_relacion == "01"
        assert len(cfdi_rel.uuids) == 2

    def test_cfdi_relacionados_to_dict(self):
        cfdi_rel = CfdiRelacionados(
            tipo_relacion="01",
            uuids=["UUID1", "UUID2"]
        )
        
        data = cfdi_rel.to_dict()
        
        assert data["tipo_relacion"] == "01"
        assert data["uuids"] == ["UUID1", "UUID2"]


class TestCfdi4Request:
    def test_cfdi4_request_creation(self):
        emisor = Emisor(
            rfc="XAXX010101000",
            nombre="EMPRESA EMISORA SA DE CV",
            regimen_fiscal="601",
            cp="06300"
        )
        
        receptor = Receptor(
            rfc="XAXX010101001",
            nombre="CLIENTE RECEPTOR",
            uso_cfdi="G03",
            domicilio_fiscal_receptor="06300",
            regimen_fiscal_receptor="612"
        )
        
        concepto = Concepto(
            clave_prod_serv="01010101",
            cantidad=Decimal("1"),
            clave_unidad="E48",
            descripcion="Servicio de desarrollo",
            valor_unitario=Decimal("10000.00"),
            importe=Decimal("10000.00"),
            objeto_imp="02"
        )
        
        cfdi = Cfdi4Request(
            emisor=emisor,
            receptor=receptor,
            conceptos=[concepto],
            tipo_comprobante="I",
            forma_pago="01",
            metodo_pago="PUE",
            moneda="MXN",
            subtotal=Decimal("10000.00"),
            total=Decimal("11600.00")
        )
        
        assert cfdi.emisor.rfc == "XAXX010101000"
        assert cfdi.receptor.rfc == "XAXX010101001"
        assert len(cfdi.conceptos) == 1
        assert cfdi.total == Decimal("11600.00")

    def test_cfdi4_request_to_dict(self):
        emisor = Emisor(
            rfc="XAXX010101000",
            nombre="EMPRESA EMISORA SA DE CV",
            regimen_fiscal="601",
            cp="06300"
        )
        
        receptor = Receptor(
            rfc="XAXX010101001",
            nombre="CLIENTE RECEPTOR",
            uso_cfdi="G03",
            domicilio_fiscal_receptor="06300",
            regimen_fiscal_receptor="612"
        )
        
        concepto = Concepto(
            clave_prod_serv="01010101",
            cantidad=Decimal("1"),
            clave_unidad="E48",
            descripcion="Servicio de desarrollo",
            valor_unitario=Decimal("10000.00"),
            importe=Decimal("10000.00"),
            objeto_imp="02"
        )
        
        cfdi = Cfdi4Request(
            emisor=emisor,
            receptor=receptor,
            conceptos=[concepto],
            tipo_comprobante="I",
            forma_pago="01",
            metodo_pago="PUE",
            moneda="MXN",
            subtotal=Decimal("10000.00"),
            total=Decimal("11600.00")
        )
        
        data = cfdi.to_dict()
        
        assert "emisor" in data
        assert "receptor" in data
        assert "conceptos" in data
        assert data["subtotal"] == 10000.00
        assert data["total"] == 11600.00
        assert data["exportacion"] == "01"


class TestCuentaPredial:
    def test_cuenta_predial_creation(self):
        cuenta = CuentaPredial(numero="123456")
        
        assert cuenta.numero == "123456"

    def test_cuenta_predial_to_dict(self):
        cuenta = CuentaPredial(numero="123456")
        data = cuenta.to_dict()
        
        assert data["numero"] == "123456"


class TestInformacionAduanera:
    def test_informacion_aduanera_creation(self):
        info = InformacionAduanera(
            numero_pedimento="12345678901234567890123",
            fecha="2024-01-01",
            aduana="01"
        )
        
        assert info.numero_pedimento == "12345678901234567890123"
        assert info.fecha == "2024-01-01"

    def test_informacion_aduanera_to_dict(self):
        info = InformacionAduanera(
            numero_pedimento="12345678901234567890123"
        )
        
        data = info.to_dict()
        
        assert data["numero_pedimento"] == "12345678901234567890123"
        assert "fecha" not in data


class TestParte:
    def test_parte_creation(self):
        parte = Parte(
            clave_prod_serv="01010101",
            cantidad=Decimal("5"),
            descripcion="Componente"
        )
        
        assert parte.clave_prod_serv == "01010101"
        assert parte.cantidad == Decimal("5")

    def test_parte_to_dict(self):
        parte = Parte(
            clave_prod_serv="01010101",
            cantidad=Decimal("5"),
            descripcion="Componente"
        )
        
        data = parte.to_dict()
        
        assert data["clave_prod_serv"] == "01010101"
        assert data["cantidad"] == 5.0
