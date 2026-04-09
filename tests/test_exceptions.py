import pytest
from tecnofact.exceptions import (
    TecnoFactException,
    AuthenticationException,
    ValidationException,
    TimbradoException,
    CancelacionException,
    NotFoundException,
    RateLimitException,
    ServerException
)


class TestTecnoFactException:
    def test_exception_with_message_only(self):
        exc = TecnoFactException("Test error")
        
        assert str(exc) == "Test error"
        assert exc.message == "Test error"
        assert exc.code is None
        assert exc.details == {}

    def test_exception_with_code(self):
        exc = TecnoFactException("Test error", code=400)
        
        assert str(exc) == "[400] Test error"
        assert exc.message == "Test error"
        assert exc.code == 400

    def test_exception_with_details(self):
        details = {"field": "email", "error": "invalid"}
        exc = TecnoFactException("Test error", code=400, details=details)
        
        assert exc.get_details() == details

    def test_exception_inheritance(self):
        exc = TecnoFactException("Test error")
        assert isinstance(exc, Exception)


class TestAuthenticationException:
    def test_authentication_exception(self):
        exc = AuthenticationException("Invalid credentials", code=401)
        
        assert isinstance(exc, TecnoFactException)
        assert str(exc) == "[401] Invalid credentials"


class TestValidationException:
    def test_validation_exception(self):
        exc = ValidationException("Invalid data", code=400)
        
        assert isinstance(exc, TecnoFactException)
        assert str(exc) == "[400] Invalid data"


class TestTimbradoException:
    def test_timbrado_exception(self):
        exc = TimbradoException("Timbrado failed", code=422)
        
        assert isinstance(exc, TecnoFactException)
        assert str(exc) == "[422] Timbrado failed"


class TestCancelacionException:
    def test_cancelacion_exception(self):
        exc = CancelacionException("Cancelacion failed", code=422)
        
        assert isinstance(exc, TecnoFactException)
        assert str(exc) == "[422] Cancelacion failed"


class TestNotFoundException:
    def test_not_found_exception(self):
        exc = NotFoundException("Resource not found", code=404)
        
        assert isinstance(exc, TecnoFactException)
        assert str(exc) == "[404] Resource not found"


class TestRateLimitException:
    def test_rate_limit_exception(self):
        exc = RateLimitException("Too many requests", code=429)
        
        assert isinstance(exc, TecnoFactException)
        assert str(exc) == "[429] Too many requests"


class TestServerException:
    def test_server_exception(self):
        exc = ServerException("Internal server error", code=500)
        
        assert isinstance(exc, TecnoFactException)
        assert str(exc) == "[500] Internal server error"
