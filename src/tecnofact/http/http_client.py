import requests
from typing import Dict, Any, Optional
from ..config.config import Config
from ..contracts.http_client_interface import HttpClientInterface
from ..exceptions import (
    AuthenticationException,
    ValidationException,
    NotFoundException,
    RateLimitException,
    ServerException,
    TecnoFactException,
)


class HttpClient(HttpClientInterface):
    def __init__(self, config: Config):
        self.config = config
        self.base_url = config.get_base_url()
        self.timeout = config.get_timeout()
        self.session = requests.Session()
        self.session.headers.update({
            "Content-Type": "application/json",
            "Accept": "application/json",
        })
        self._token: Optional[str] = None

    def set_token(self, token: str) -> None:
        """Set the Bearer token obtained from AuthService.login()."""
        self._token = token
        self.session.headers.update({
            "Authorization": f"Bearer {token}",
        })

    def _handle_response(self, response: requests.Response) -> Dict[str, Any]:
        try:
            data = response.json()
        except ValueError:
            data = {"message": response.text}

        if response.status_code == 401:
            raise AuthenticationException(
                message=data.get("message", "Authentication failed"),
                code=response.status_code,
                details=data,
            )
        elif response.status_code == 400:
            raise ValidationException(
                message=data.get("message", "Validation error"),
                code=response.status_code,
                details=data,
            )
        elif response.status_code == 404:
            raise NotFoundException(
                message=data.get("message", "Resource not found"),
                code=response.status_code,
                details=data,
            )
        elif response.status_code == 429:
            raise RateLimitException(
                message=data.get("message", "Rate limit exceeded"),
                code=response.status_code,
                details=data,
            )
        elif response.status_code >= 500:
            raise ServerException(
                message=data.get("message", "Server error"),
                code=response.status_code,
                details=data,
            )
        elif not response.ok:
            raise TecnoFactException(
                message=data.get("message", "Request failed"),
                code=response.status_code,
                details=data,
            )

        return data

    def post(
        self,
        endpoint: str,
        data: Dict[str, Any],
        headers: Optional[Dict[str, str]] = None,
    ) -> Dict[str, Any]:
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        request_headers = dict(self.session.headers)
        if headers:
            request_headers.update(headers)

        response = self.session.post(
            url,
            json=data,
            headers=request_headers,
            timeout=self.timeout,
        )
        return self._handle_response(response)

    def get(
        self,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
    ) -> Dict[str, Any]:
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        request_headers = dict(self.session.headers)
        if headers:
            request_headers.update(headers)

        response = self.session.get(
            url,
            params=params,
            headers=request_headers,
            timeout=self.timeout,
        )
        return self._handle_response(response)

    def put(
        self,
        endpoint: str,
        data: Dict[str, Any],
        headers: Optional[Dict[str, str]] = None,
    ) -> Dict[str, Any]:
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        request_headers = dict(self.session.headers)
        if headers:
            request_headers.update(headers)

        response = self.session.put(
            url,
            json=data,
            headers=request_headers,
            timeout=self.timeout,
        )
        return self._handle_response(response)

    def delete(
        self,
        endpoint: str,
        headers: Optional[Dict[str, str]] = None,
    ) -> Dict[str, Any]:
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        request_headers = dict(self.session.headers)
        if headers:
            request_headers.update(headers)

        response = self.session.delete(
            url,
            headers=request_headers,
            timeout=self.timeout,
        )
        return self._handle_response(response)
