from dataclasses import dataclass
from typing import Dict, Any, Optional, List
from decimal import Decimal
from .impuestos_concepto import ImpuestosConcepto
from .cuenta_predial import CuentaPredial
from .informacion_aduanera import InformacionAduanera
from .parte import Parte


@dataclass
class Concepto:
    clave_prod_serv: str
    cantidad: Decimal
    clave_unidad: str
    descripcion: str
    valor_unitario: Decimal
    importe: Decimal
    objeto_imp: str
    no_identificacion: Optional[str] = None
    unidad: Optional[str] = None
    descuento: Optional[Decimal] = None
    impuestos: Optional[ImpuestosConcepto] = None
    cuenta_predial: Optional[CuentaPredial] = None
    informacion_aduanera: Optional[List[InformacionAduanera]] = None
    partes: Optional[List[Parte]] = None

    def to_dict(self) -> Dict[str, Any]:
        data = {
            "clave_prod_serv": self.clave_prod_serv,
            "cantidad": float(self.cantidad),
            "clave_unidad": self.clave_unidad,
            "descripcion": self.descripcion,
            "valor_unitario": float(self.valor_unitario),
            "importe": float(self.importe),
            "objeto_imp": self.objeto_imp
        }
        
        if self.no_identificacion:
            data["no_identificacion"] = self.no_identificacion
        if self.unidad:
            data["unidad"] = self.unidad
        if self.descuento is not None:
            data["descuento"] = float(self.descuento)
        if self.impuestos:
            data["impuestos"] = self.impuestos.to_dict()
        if self.cuenta_predial:
            data["cuenta_predial"] = self.cuenta_predial.to_dict()
        if self.informacion_aduanera:
            data["informacion_aduanera"] = [ia.to_dict() for ia in self.informacion_aduanera]
        if self.partes:
            data["partes"] = [p.to_dict() for p in self.partes]
        
        return data
