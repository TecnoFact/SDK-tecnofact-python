from enum import Enum


class Environment(Enum):
    SANDBOX = "sandbox"
    PRODUCTION = "production"

    def is_production(self) -> bool:
        return self == Environment.PRODUCTION

    def is_sandbox(self) -> bool:
        return self == Environment.SANDBOX

    def label(self) -> str:
        labels = {
            Environment.SANDBOX: "Sandbox",
            Environment.PRODUCTION: "Producción"
        }
        return labels[self]

    def get_base_url(self) -> str:
        urls = {
            Environment.SANDBOX: "https://sandbox.tecnofact.com/api",
            Environment.PRODUCTION: "https://api.tecnofact.com/api"
        }
        return urls[self]
