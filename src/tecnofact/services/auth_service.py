from typing import Optional
from ..config.config import Config
from ..http.http_client import HttpClient
from ..exceptions import AuthenticationException


class AuthService:
    """Handles authentication against POST /api/login.

    Usage::

        config = Config(email="user@example.com", password="secret")
        auth = AuthService(config)
        token = auth.login()
        # token is a Bearer JWT string
    """

    _ENDPOINT = "api/login"

    def __init__(self, config: Config, http_client: Optional[HttpClient] = None):
        self.config = config
        self._http = http_client or HttpClient(config)
        self._token: Optional[str] = None

    def login(self) -> str:
        """POST /api/login with email + password.

        Returns the Bearer token string and caches it internally.
        Raises :class:`AuthenticationException` on invalid credentials.
        """
        response = self._http.post(
            self._ENDPOINT,
            {"email": self.config.email, "password": self.config.password},
        )

        token: Optional[str] = response.get("token") or response.get("access_token")
        if not token:
            raise AuthenticationException(
                message="Login response did not include a token",
                code=200,
                details=response,
            )

        self._token = token
        self._http.set_token(token)
        return token

    @property
    def token(self) -> Optional[str]:
        """Return the cached token, or None if login has not been called yet."""
        return self._token

    def get_http_client(self) -> HttpClient:
        """Return the authenticated HttpClient for use in other services."""
        return self._http
