from dataclasses import dataclass
from typing import Dict, Any


@dataclass
class CuentaPredial:
    numero: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "numero": self.numero
        }
