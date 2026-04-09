import pytest
from tecnofact.config import Config
from tecnofact.enums import Environment


class TestConfig:
    def test_config_creation_with_defaults(self):
        config = Config(
            api_key="test_key",
            api_secret="test_secret"
        )
        
        assert config.api_key == "test_key"
        assert config.api_secret == "test_secret"
        assert config.environment == Environment.SANDBOX
        assert config.timeout == 30
        assert config.retries == 3

    def test_config_creation_with_custom_values(self):
        config = Config(
            api_key="test_key",
            api_secret="test_secret",
            environment=Environment.PRODUCTION,
            timeout=60,
            retries=5
        )
        
        assert config.api_key == "test_key"
        assert config.api_secret == "test_secret"
        assert config.environment == Environment.PRODUCTION
        assert config.timeout == 60
        assert config.retries == 5

    def test_config_requires_api_key(self):
        with pytest.raises(ValueError, match="api_key is required"):
            Config(
                api_key="",
                api_secret="test_secret"
            )

    def test_config_requires_api_secret(self):
        with pytest.raises(ValueError, match="api_secret is required"):
            Config(
                api_key="test_key",
                api_secret=""
            )

    def test_config_timeout_must_be_positive(self):
        with pytest.raises(ValueError, match="timeout must be greater than 0"):
            Config(
                api_key="test_key",
                api_secret="test_secret",
                timeout=0
            )

    def test_config_retries_must_be_non_negative(self):
        with pytest.raises(ValueError, match="retries must be non-negative"):
            Config(
                api_key="test_key",
                api_secret="test_secret",
                retries=-1
            )

    def test_get_base_url_sandbox(self):
        config = Config(
            api_key="test_key",
            api_secret="test_secret",
            environment=Environment.SANDBOX
        )
        
        assert config.get_base_url() == "https://sandbox.tecnofact.com/api"

    def test_get_base_url_production(self):
        config = Config(
            api_key="test_key",
            api_secret="test_secret",
            environment=Environment.PRODUCTION
        )
        
        assert config.get_base_url() == "https://api.tecnofact.com/api"

    def test_get_environment(self):
        config = Config(
            api_key="test_key",
            api_secret="test_secret",
            environment=Environment.PRODUCTION
        )
        
        assert config.get_environment() == Environment.PRODUCTION

    def test_get_timeout(self):
        config = Config(
            api_key="test_key",
            api_secret="test_secret",
            timeout=45
        )
        
        assert config.get_timeout() == 45

    def test_get_retries(self):
        config = Config(
            api_key="test_key",
            api_secret="test_secret",
            retries=10
        )
        
        assert config.get_retries() == 10

    def test_to_dict(self):
        config = Config(
            api_key="test_key",
            api_secret="test_secret",
            environment=Environment.SANDBOX,
            timeout=30,
            retries=3
        )
        
        data = config.to_dict()
        
        assert data["api_key"] == "test_key"
        assert data["api_secret"] == "test_secret"
        assert data["environment"] == "sandbox"
        assert data["base_url"] == "https://sandbox.tecnofact.com/api"
        assert data["timeout"] == 30
        assert data["retries"] == 3

    def test_config_is_immutable(self):
        config = Config(
            api_key="test_key",
            api_secret="test_secret"
        )
        
        with pytest.raises(Exception):
            config.api_key = "new_key"
