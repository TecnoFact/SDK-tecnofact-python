from dataclasses import dataclass
from typing import Dict, Any, Optional


@dataclass
class InformacionAduanera:
    numero_pedimento: str
    fecha: Optional[str] = None
    aduana: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        data = {
            "numero_pedimento": self.numero_pedimento
        }
        if self.fecha:
            data["fecha"] = self.fecha
        if self.aduana:
            data["aduana"] = self.aduana
        return data
