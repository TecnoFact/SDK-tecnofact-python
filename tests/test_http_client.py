import pytest
from unittest.mock import Mock, patch
import requests
from tecnofact.config import Config
from tecnofact.enums import Environment
from tecnofact.http import HttpClient
from tecnofact.exceptions import (
    AuthenticationException,
    ValidationException,
    NotFoundException,
    RateLimitException,
    ServerException,
    TecnoFactException
)


class TestHttpClient:
    @pytest.fixture
    def config(self):
        return Config(
            api_key="test_key",
            api_secret="test_secret",
            environment=Environment.SANDBOX
        )

    @pytest.fixture
    def http_client(self, config):
        return HttpClient(config)

    def test_http_client_initialization(self, http_client, config):
        assert http_client.config == config
        assert http_client.base_url == "https://sandbox.tecnofact.com/api"
        assert http_client.timeout == 30
        assert http_client.session.headers["X-API-Key"] == "test_key"
        assert http_client.session.headers["X-API-Secret"] == "test_secret"

    @patch('requests.Session.post')
    def test_post_success(self, mock_post, http_client):
        mock_response = Mock()
        mock_response.ok = True
        mock_response.status_code = 200
        mock_response.json.return_value = {"success": True}
        mock_post.return_value = mock_response

        result = http_client.post("/test", {"data": "value"})

        assert result == {"success": True}
        mock_post.assert_called_once()

    @patch('requests.Session.get')
    def test_get_success(self, mock_get, http_client):
        mock_response = Mock()
        mock_response.ok = True
        mock_response.status_code = 200
        mock_response.json.return_value = {"data": "value"}
        mock_get.return_value = mock_response

        result = http_client.get("/test")

        assert result == {"data": "value"}
        mock_get.assert_called_once()

    @patch('requests.Session.put')
    def test_put_success(self, mock_put, http_client):
        mock_response = Mock()
        mock_response.ok = True
        mock_response.status_code = 200
        mock_response.json.return_value = {"updated": True}
        mock_put.return_value = mock_response

        result = http_client.put("/test", {"data": "value"})

        assert result == {"updated": True}
        mock_put.assert_called_once()

    @patch('requests.Session.delete')
    def test_delete_success(self, mock_delete, http_client):
        mock_response = Mock()
        mock_response.ok = True
        mock_response.status_code = 200
        mock_response.json.return_value = {"deleted": True}
        mock_delete.return_value = mock_response

        result = http_client.delete("/test")

        assert result == {"deleted": True}
        mock_delete.assert_called_once()

    @patch('requests.Session.post')
    def test_authentication_exception(self, mock_post, http_client):
        mock_response = Mock()
        mock_response.ok = False
        mock_response.status_code = 401
        mock_response.json.return_value = {"message": "Unauthorized"}
        mock_post.return_value = mock_response

        with pytest.raises(AuthenticationException) as exc_info:
            http_client.post("/test", {})

        assert exc_info.value.code == 401
        assert "Unauthorized" in str(exc_info.value)

    @patch('requests.Session.post')
    def test_validation_exception(self, mock_post, http_client):
        mock_response = Mock()
        mock_response.ok = False
        mock_response.status_code = 400
        mock_response.json.return_value = {"message": "Invalid data"}
        mock_post.return_value = mock_response

        with pytest.raises(ValidationException) as exc_info:
            http_client.post("/test", {})

        assert exc_info.value.code == 400
        assert "Invalid data" in str(exc_info.value)

    @patch('requests.Session.get')
    def test_not_found_exception(self, mock_get, http_client):
        mock_response = Mock()
        mock_response.ok = False
        mock_response.status_code = 404
        mock_response.json.return_value = {"message": "Not found"}
        mock_get.return_value = mock_response

        with pytest.raises(NotFoundException) as exc_info:
            http_client.get("/test")

        assert exc_info.value.code == 404
        assert "Not found" in str(exc_info.value)

    @patch('requests.Session.post')
    def test_rate_limit_exception(self, mock_post, http_client):
        mock_response = Mock()
        mock_response.ok = False
        mock_response.status_code = 429
        mock_response.json.return_value = {"message": "Too many requests"}
        mock_post.return_value = mock_response

        with pytest.raises(RateLimitException) as exc_info:
            http_client.post("/test", {})

        assert exc_info.value.code == 429
        assert "Too many requests" in str(exc_info.value)

    @patch('requests.Session.post')
    def test_server_exception(self, mock_post, http_client):
        mock_response = Mock()
        mock_response.ok = False
        mock_response.status_code = 500
        mock_response.json.return_value = {"message": "Internal server error"}
        mock_post.return_value = mock_response

        with pytest.raises(ServerException) as exc_info:
            http_client.post("/test", {})

        assert exc_info.value.code == 500
        assert "Internal server error" in str(exc_info.value)

    @patch('requests.Session.post')
    def test_generic_exception(self, mock_post, http_client):
        mock_response = Mock()
        mock_response.ok = False
        mock_response.status_code = 418
        mock_response.json.return_value = {"message": "I'm a teapot"}
        mock_post.return_value = mock_response

        with pytest.raises(TecnoFactException) as exc_info:
            http_client.post("/test", {})

        assert exc_info.value.code == 418

    @patch('requests.Session.post')
    def test_post_with_custom_headers(self, mock_post, http_client):
        mock_response = Mock()
        mock_response.ok = True
        mock_response.status_code = 200
        mock_response.json.return_value = {"success": True}
        mock_post.return_value = mock_response

        custom_headers = {"X-Custom-Header": "value"}
        http_client.post("/test", {}, headers=custom_headers)

        call_args = mock_post.call_args
        assert "X-Custom-Header" in call_args[1]["headers"]
        assert call_args[1]["headers"]["X-Custom-Header"] == "value"

    @patch('requests.Session.get')
    def test_get_with_params(self, mock_get, http_client):
        mock_response = Mock()
        mock_response.ok = True
        mock_response.status_code = 200
        mock_response.json.return_value = {"data": "value"}
        mock_get.return_value = mock_response

        params = {"page": 1, "limit": 10}
        http_client.get("/test", params=params)

        call_args = mock_get.call_args
        assert call_args[1]["params"] == params

    @patch('requests.Session.post')
    def test_handle_non_json_response(self, mock_post, http_client):
        mock_response = Mock()
        mock_response.ok = False
        mock_response.status_code = 500
        mock_response.json.side_effect = ValueError("No JSON")
        mock_response.text = "Plain text error"
        mock_post.return_value = mock_response

        with pytest.raises(ServerException) as exc_info:
            http_client.post("/test", {})

        assert exc_info.value.code == 500
