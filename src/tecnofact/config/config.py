from dataclasses import dataclass
from typing import Dict, Any
from ..enums.environment import Environment


@dataclass(frozen=True)
class Config:
    api_key: str
    api_secret: str
    environment: Environment = Environment.SANDBOX
    timeout: int = 30
    retries: int = 3

    def __post_init__(self):
        if not self.api_key:
            raise ValueError("api_key is required")
        if not self.api_secret:
            raise ValueError("api_secret is required")
        if self.timeout <= 0:
            raise ValueError("timeout must be greater than 0")
        if self.retries < 0:
            raise ValueError("retries must be non-negative")

    def get_base_url(self) -> str:
        return self.environment.get_base_url()

    def get_environment(self) -> Environment:
        return self.environment

    def get_timeout(self) -> int:
        return self.timeout

    def get_retries(self) -> int:
        return self.retries

    def to_dict(self) -> Dict[str, Any]:
        return {
            "api_key": self.api_key,
            "api_secret": self.api_secret,
            "environment": self.environment.value,
            "base_url": self.get_base_url(),
            "timeout": self.timeout,
            "retries": self.retries
        }
