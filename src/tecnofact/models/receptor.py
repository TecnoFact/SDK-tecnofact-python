from dataclasses import dataclass
from typing import Dict, Any, Optional


@dataclass
class Receptor:
    rfc: str
    nombre: str
    uso_cfdi: str
    domicilio_fiscal_receptor: str
    regimen_fiscal_receptor: str
    residencia_fiscal: Optional[str] = None
    num_reg_id_trib: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        data = {
            "rfc": self.rfc,
            "nombre": self.nombre,
            "uso_cfdi": self.uso_cfdi,
            "domicilio_fiscal_receptor": self.domicilio_fiscal_receptor,
            "regimen_fiscal_receptor": self.regimen_fiscal_receptor
        }
        if self.residencia_fiscal:
            data["residencia_fiscal"] = self.residencia_fiscal
        if self.num_reg_id_trib:
            data["num_reg_id_trib"] = self.num_reg_id_trib
        return data

    def get_rfc(self) -> str:
        return self.rfc

    def get_nombre(self) -> str:
        return self.nombre

    def get_uso_cfdi(self) -> str:
        return self.uso_cfdi
