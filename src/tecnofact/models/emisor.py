from dataclasses import dataclass
from typing import Dict, Any


@dataclass
class Emisor:
    rfc: str
    nombre: str
    regimen_fiscal: str
    cp: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "rfc": self.rfc,
            "nombre": self.nombre,
            "regimen_fiscal": self.regimen_fiscal,
            "cp": self.cp
        }

    def get_rfc(self) -> str:
        return self.rfc

    def get_nombre(self) -> str:
        return self.nombre

    def get_regimen_fiscal(self) -> str:
        return self.regimen_fiscal

    def get_cp(self) -> str:
        return self.cp
