import pytest
from decimal import Decimal
from tecnofact.config import Config
from tecnofact.enums import Environment
from tecnofact.models import Emisor, Receptor, Concepto


@pytest.fixture
def sample_config():
    return Config(
        email="test@example.com",
        password="test_password",
        environment=Environment.PRODUCTION,
        timeout=30,
        retries=3,
    )


@pytest.fixture
def sample_emisor():
    return Emisor(
        rfc="XAXX010101000",
        nombre="EMPRESA EMISORA SA DE CV",
        regimen_fiscal="601",
        cp="06300",
    )


@pytest.fixture
def sample_receptor():
    return Receptor(
        rfc="XAXX010101001",
        nombre="CLIENTE RECEPTOR",
        uso_cfdi="G03",
        domicilio_fiscal_receptor="06300",
        regimen_fiscal_receptor="612",
    )


@pytest.fixture
def sample_concepto():
    return Concepto(
        clave_prod_serv="01010101",
        cantidad=Decimal("1"),
        clave_unidad="E48",
        descripcion="Servicio de desarrollo de software",
        valor_unitario=Decimal("10000.00"),
        importe=Decimal("10000.00"),
        objeto_imp="02",
    )
