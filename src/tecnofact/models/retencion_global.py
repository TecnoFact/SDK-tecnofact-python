from dataclasses import dataclass
from typing import Dict, Any
from decimal import Decimal


@dataclass
class RetencionGlobal:
    impuesto: str
    importe: Decimal

    def to_dict(self) -> Dict[str, Any]:
        return {
            "impuesto": self.impuesto,
            "importe": float(self.importe)
        }
