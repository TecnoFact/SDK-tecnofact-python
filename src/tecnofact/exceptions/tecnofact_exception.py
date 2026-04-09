from typing import Optional, Dict, Any


class TecnoFactException(Exception):
    def __init__(
        self,
        message: str,
        code: Optional[int] = None,
        details: Optional[Dict[str, Any]] = None
    ):
        self.message = message
        self.code = code
        self.details = details or {}
        super().__init__(self.message)

    def __str__(self) -> str:
        if self.code:
            return f"[{self.code}] {self.message}"
        return self.message

    def get_details(self) -> Dict[str, Any]:
        return self.details
