import pytest
from tecnofact.enums import Environment, TipoComprobante


class TestEnvironment:
    def test_environment_values(self):
        assert Environment.SANDBOX.value == "sandbox"
        assert Environment.PRODUCTION.value == "production"

    def test_is_production(self):
        assert Environment.PRODUCTION.is_production() is True
        assert Environment.SANDBOX.is_production() is False

    def test_is_sandbox(self):
        assert Environment.SANDBOX.is_sandbox() is True
        assert Environment.PRODUCTION.is_sandbox() is False

    def test_label(self):
        assert Environment.SANDBOX.label() == "Sandbox"
        assert Environment.PRODUCTION.label() == "Producción"

    def test_get_base_url(self):
        assert Environment.SANDBOX.get_base_url() == "https://sandbox.tecnofact.com/api"
        assert Environment.PRODUCTION.get_base_url() == "https://api.tecnofact.com/api"

    def test_environment_equality(self):
        env1 = Environment.SANDBOX
        env2 = Environment.SANDBOX
        env3 = Environment.PRODUCTION
        
        assert env1 == env2
        assert env1 != env3


class TestTipoComprobante:
    def test_tipo_comprobante_values(self):
        assert TipoComprobante.INGRESO.value == "I"
        assert TipoComprobante.EGRESO.value == "E"
        assert TipoComprobante.TRASLADO.value == "T"
        assert TipoComprobante.NOMINA.value == "N"
        assert TipoComprobante.PAGO.value == "P"

    def test_tipo_comprobante_labels(self):
        assert TipoComprobante.INGRESO.label() == "Ingreso"
        assert TipoComprobante.EGRESO.label() == "Egreso"
        assert TipoComprobante.TRASLADO.label() == "Traslado"
        assert TipoComprobante.NOMINA.label() == "Nómina"
        assert TipoComprobante.PAGO.label() == "Pago"

    def test_tipo_comprobante_equality(self):
        tipo1 = TipoComprobante.INGRESO
        tipo2 = TipoComprobante.INGRESO
        tipo3 = TipoComprobante.EGRESO
        
        assert tipo1 == tipo2
        assert tipo1 != tipo3
