from dataclasses import dataclass
from typing import Dict, Any, List, Optional
from decimal import Decimal
from .emisor import Emisor
from .receptor import Receptor
from .concepto import Concepto
from .impuestos import Impuestos
from .cfdi_relacionados import CfdiRelacionados


@dataclass
class Cfdi4Request:
    emisor: Emisor
    receptor: Receptor
    conceptos: List[Concepto]
    tipo_comprobante: str
    forma_pago: str
    metodo_pago: str
    moneda: str
    subtotal: Decimal
    total: Decimal
    serie: Optional[str] = None
    folio: Optional[str] = None
    fecha: Optional[str] = None
    lugar_expedicion: Optional[str] = None
    tipo_cambio: Optional[Decimal] = None
    descuento: Optional[Decimal] = None
    impuestos: Optional[Impuestos] = None
    cfdi_relacionados: Optional[List[CfdiRelacionados]] = None
    condiciones_pago: Optional[str] = None
    exportacion: str = "01"

    def to_dict(self) -> Dict[str, Any]:
        data = {
            "emisor": self.emisor.to_dict(),
            "receptor": self.receptor.to_dict(),
            "conceptos": [c.to_dict() for c in self.conceptos],
            "tipo_comprobante": self.tipo_comprobante,
            "forma_pago": self.forma_pago,
            "metodo_pago": self.metodo_pago,
            "moneda": self.moneda,
            "subtotal": float(self.subtotal),
            "total": float(self.total),
            "exportacion": self.exportacion
        }
        
        if self.serie:
            data["serie"] = self.serie
        if self.folio:
            data["folio"] = self.folio
        if self.fecha:
            data["fecha"] = self.fecha
        if self.lugar_expedicion:
            data["lugar_expedicion"] = self.lugar_expedicion
        if self.tipo_cambio is not None:
            data["tipo_cambio"] = float(self.tipo_cambio)
        if self.descuento is not None:
            data["descuento"] = float(self.descuento)
        if self.impuestos:
            data["impuestos"] = self.impuestos.to_dict()
        if self.cfdi_relacionados:
            data["cfdi_relacionados"] = [cr.to_dict() for cr in self.cfdi_relacionados]
        if self.condiciones_pago:
            data["condiciones_pago"] = self.condiciones_pago
        
        return data
