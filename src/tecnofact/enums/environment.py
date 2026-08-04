from enum import Enum


class Environment(Enum):
    PRODUCTION = "production"

    def is_production(self) -> bool:
        return self == Environment.PRODUCTION

    def label(self) -> str:
        return "Producción"

    def get_base_url(self) -> str:
        return "https://panelcfdi.tecnofact.mx"
