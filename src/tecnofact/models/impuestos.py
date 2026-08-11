from dataclasses import dataclass
from typing import Dict, Any, List, Optional, TypedDict
from decimal import Decimal
from .traslado_global import TrasladoGlobal
from .retencion_global import RetencionGlobal


class ImpuestosData(TypedDict, total=False):
    total_impuestos_trasladados: float
    total_impuestos_retenidos: float
    traslados: List[Dict[str, Any]]
    retenciones: List[Dict[str, Any]]


@dataclass
class Impuestos:
    total_impuestos_trasladados: Optional[Decimal] = None
    total_impuestos_retenidos: Optional[Decimal] = None
    traslados: Optional[List[TrasladoGlobal]] = None
    retenciones: Optional[List[RetencionGlobal]] = None

    def to_dict(self) -> ImpuestosData:
        data: ImpuestosData = {}
        if self.total_impuestos_trasladados is not None:
            data["total_impuestos_trasladados"] = float(self.total_impuestos_trasladados)
        if self.total_impuestos_retenidos is not None:
            data["total_impuestos_retenidos"] = float(self.total_impuestos_retenidos)
        if self.traslados:
            data["traslados"] = [t.to_dict() for t in self.traslados]
        if self.retenciones:
            data["retenciones"] = [r.to_dict() for r in self.retenciones]
        return data
