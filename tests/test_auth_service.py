import pytest
from unittest.mock import MagicMock, patch
from tecnofact.config import Config
from tecnofact.enums import Environment
from tecnofact.services import AuthService
from tecnofact.http import HttpClient
from tecnofact.exceptions import AuthenticationException


@pytest.fixture
def config():
    return Config(
        email="user@example.com",
        password="secret123",
        environment=Environment.PRODUCTION,
    )


class TestAuthService:
    def test_login_returns_token(self, config):
        mock_http = MagicMock(spec=HttpClient)
        mock_http.post.return_value = {"token": "jwt.token.here"}

        auth = AuthService(config, http_client=mock_http)
        token = auth.login()

        assert token == "jwt.token.here"
        mock_http.post.assert_called_once_with(
            "api/login",
            {"email": "user@example.com", "password": "secret123"},
        )

    def test_login_accepts_access_token_key(self, config):
        mock_http = MagicMock(spec=HttpClient)
        mock_http.post.return_value = {"access_token": "bearer.access.token"}

        auth = AuthService(config, http_client=mock_http)
        token = auth.login()

        assert token == "bearer.access.token"

    def test_login_caches_token(self, config):
        mock_http = MagicMock(spec=HttpClient)
        mock_http.post.return_value = {"token": "cached.token"}

        auth = AuthService(config, http_client=mock_http)
        auth.login()

        assert auth.token == "cached.token"

    def test_login_sets_bearer_header_on_http_client(self, config):
        mock_http = MagicMock(spec=HttpClient)
        mock_http.post.return_value = {"token": "my.jwt"}

        auth = AuthService(config, http_client=mock_http)
        auth.login()

        mock_http.set_token.assert_called_once_with("my.jwt")

    def test_login_raises_when_response_has_no_token(self, config):
        mock_http = MagicMock(spec=HttpClient)
        mock_http.post.return_value = {"status": "ok"}  # no token field

        auth = AuthService(config, http_client=mock_http)

        with pytest.raises(AuthenticationException, match="did not include a token"):
            auth.login()

    def test_token_is_none_before_login(self, config):
        mock_http = MagicMock(spec=HttpClient)
        auth = AuthService(config, http_client=mock_http)

        assert auth.token is None

    def test_get_http_client_returns_same_instance(self, config):
        mock_http = MagicMock(spec=HttpClient)
        mock_http.post.return_value = {"token": "tok"}

        auth = AuthService(config, http_client=mock_http)
        auth.login()

        assert auth.get_http_client() is mock_http
