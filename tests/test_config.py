import pytest
from tecnofact.config import Config
from tecnofact.enums import Environment


class TestConfig:
    def test_config_creation_with_defaults(self):
        config = Config(email="test@example.com", password="secret")

        assert config.email == "test@example.com"
        assert config.password == "secret"
        assert config.environment == Environment.PRODUCTION
        assert config.timeout == 30
        assert config.retries == 3

    def test_config_creation_with_custom_values(self):
        config = Config(
            email="test@example.com",
            password="secret",
            environment=Environment.PRODUCTION,
            timeout=60,
            retries=5,
        )

        assert config.email == "test@example.com"
        assert config.password == "secret"
        assert config.environment == Environment.PRODUCTION
        assert config.timeout == 60
        assert config.retries == 5

    def test_config_requires_email(self):
        with pytest.raises(ValueError, match="email is required"):
            Config(email="", password="secret")

    def test_config_requires_password(self):
        with pytest.raises(ValueError, match="password is required"):
            Config(email="test@example.com", password="")

    def test_config_timeout_must_be_positive(self):
        with pytest.raises(ValueError, match="timeout must be greater than 0"):
            Config(email="test@example.com", password="secret", timeout=0)

    def test_config_retries_must_be_non_negative(self):
        with pytest.raises(ValueError, match="retries must be non-negative"):
            Config(email="test@example.com", password="secret", retries=-1)

    def test_get_base_url_production(self):
        config = Config(
            email="test@example.com",
            password="secret",
            environment=Environment.PRODUCTION,
        )

        assert config.get_base_url() == "https://panelcfdi.tecnofact.mx"

    def test_get_environment(self):
        config = Config(
            email="test@example.com",
            password="secret",
            environment=Environment.PRODUCTION,
        )

        assert config.get_environment() == Environment.PRODUCTION

    def test_get_timeout(self):
        config = Config(email="test@example.com", password="secret", timeout=45)

        assert config.get_timeout() == 45

    def test_get_retries(self):
        config = Config(email="test@example.com", password="secret", retries=10)

        assert config.get_retries() == 10

    def test_to_dict(self):
        config = Config(
            email="test@example.com",
            password="secret",
            environment=Environment.PRODUCTION,
            timeout=30,
            retries=3,
        )

        data = config.to_dict()

        assert data["email"] == "test@example.com"
        assert "password" not in data  # password is NOT serialized for security
        assert data["environment"] == "production"
        assert data["base_url"] == "https://panelcfdi.tecnofact.mx"
        assert data["timeout"] == 30
        assert data["retries"] == 3

    def test_config_is_immutable(self):
        config = Config(email="test@example.com", password="secret")

        with pytest.raises(Exception):
            config.email = "other@example.com"
