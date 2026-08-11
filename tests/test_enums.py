import pytest
from tecnofact.enums import Environment, TipoComprobante


class TestEnvironment:
    def test_environment_values(self):
        assert list(Environment) == [Environment.PRODUCTION]
        assert Environment.PRODUCTION.value == "production"

    def test_is_production(self):
        assert Environment.PRODUCTION.is_production() is True

    def test_label(self):
        assert Environment.PRODUCTION.label() == "Producción"

    def test_get_base_url(self):
        assert Environment.PRODUCTION.get_base_url() == "https://panelcfdi.tecnofact.mx"

    def test_environment_equality(self):
        env1 = Environment.PRODUCTION
        env2 = Environment("production")

        assert env1 == env2
        assert env1 is Environment.PRODUCTION


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
