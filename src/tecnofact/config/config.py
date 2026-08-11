from dataclasses import dataclass
from typing import Dict, Any
from ..enums.environment import Environment


@dataclass(frozen=True)
class Config:
    email: str
    password: str
    environment: Environment = Environment.PRODUCTION
    timeout: int = 30
    retries: int = 3

    def __post_init__(self) -> None:
        if not self.email:
            raise ValueError("email is required")
        if not self.password:
            raise ValueError("password is required")
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
            "email": self.email,
            "environment": self.environment.value,
            "base_url": self.get_base_url(),
            "timeout": self.timeout,
            "retries": self.retries,
        }
