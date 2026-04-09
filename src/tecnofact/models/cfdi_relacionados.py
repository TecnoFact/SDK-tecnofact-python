from dataclasses import dataclass
from typing import Dict, Any, List


@dataclass
class CfdiRelacionados:
    tipo_relacion: str
    uuids: List[str]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "tipo_relacion": self.tipo_relacion,
            "uuids": self.uuids
        }
