from dataclasses import dataclass
from typing import Dict, Any, List, Optional
from decimal import Decimal
from .traslado_global import TrasladoGlobal
from .retencion_global import RetencionGlobal


@dataclass
class Impuestos:
    total_impuestos_trasladados: Optional[Decimal] = None
    total_impuestos_retenidos: Optional[Decimal] = None
    traslados: Optional[List[TrasladoGlobal]] = None
    retenciones: Optional[List[RetencionGlobal]] = None

    def to_dict(self) -> Dict[str, Any]:
        data = {}
        if self.total_impuestos_trasladados is not None:
            data["total_impuestos_trasladados"] = float(self.total_impuestos_trasladados)
        if self.total_impuestos_retenidos is not None:
            data["total_impuestos_retenidos"] = float(self.total_impuestos_retenidos)
        if self.traslados:
            data["traslados"] = [t.to_dict() for t in self.traslados]
        if self.retenciones:
            data["retenciones"] = [r.to_dict() for r in self.retenciones]
        return data
