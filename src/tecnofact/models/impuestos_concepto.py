from dataclasses import dataclass
from typing import Dict, Any, List, Optional
from .traslado import Traslado
from .retencion import Retencion


@dataclass
class ImpuestosConcepto:
    traslados: Optional[List[Traslado]] = None
    retenciones: Optional[List[Retencion]] = None

    def to_dict(self) -> Dict[str, Any]:
        data = {}
        if self.traslados:
            data["traslados"] = [t.to_dict() for t in self.traslados]
        if self.retenciones:
            data["retenciones"] = [r.to_dict() for r in self.retenciones]
        return data
