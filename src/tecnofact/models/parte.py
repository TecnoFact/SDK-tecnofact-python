from dataclasses import dataclass
from typing import Dict, Any, Optional
from decimal import Decimal


@dataclass
class Parte:
    clave_prod_serv: str
    cantidad: Decimal
    unidad: Optional[str] = None
    descripcion: Optional[str] = None
    valor_unitario: Optional[Decimal] = None
    importe: Optional[Decimal] = None

    def to_dict(self) -> Dict[str, Any]:
        data = {
            "clave_prod_serv": self.clave_prod_serv,
            "cantidad": float(self.cantidad)
        }
        if self.unidad:
            data["unidad"] = self.unidad
        if self.descripcion:
            data["descripcion"] = self.descripcion
        if self.valor_unitario is not None:
            data["valor_unitario"] = float(self.valor_unitario)
        if self.importe is not None:
            data["importe"] = float(self.importe)
        return data
