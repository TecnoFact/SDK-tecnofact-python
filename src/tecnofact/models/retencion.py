from dataclasses import dataclass
from typing import Dict, Any
from decimal import Decimal


@dataclass
class Retencion:
    base: Decimal
    impuesto: str
    tipo_factor: str
    tasa_o_cuota: Decimal
    importe: Decimal

    def to_dict(self) -> Dict[str, Any]:
        return {
            "base": float(self.base),
            "impuesto": self.impuesto,
            "tipo_factor": self.tipo_factor,
            "tasa_o_cuota": str(self.tasa_o_cuota),
            "importe": float(self.importe)
        }
