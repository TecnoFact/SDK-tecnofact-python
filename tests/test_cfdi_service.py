import pytest
from unittest.mock import MagicMock, patch
from decimal import Decimal
from tecnofact.services import CfdiService
from tecnofact.xml import CfdiXmlBuilder
from tecnofact.http import HttpClient
from tecnofact.models import Cfdi4Request, Emisor, Receptor, Concepto


@pytest.fixture
def sample_request(sample_emisor, sample_receptor, sample_concepto):
    return Cfdi4Request(
        emisor=sample_emisor,
        receptor=sample_receptor,
        conceptos=[sample_concepto],
        tipo_comprobante="I",
        forma_pago="01",
        metodo_pago="PUE",
        moneda="MXN",
        subtotal=Decimal("10000.00"),
        total=Decimal("10000.00"),
        lugar_expedicion="06300",
    )


class TestCfdiService:
    def test_timbrar_posts_xml_to_endpoint(self, sample_request):
        mock_http = MagicMock(spec=HttpClient)
        mock_http.post.return_value = {"xml": "<cfdi:Comprobante .../>"}

        mock_builder = MagicMock(spec=CfdiXmlBuilder)
        mock_builder.build.return_value = "<cfdi:Comprobante .../>"

        service = CfdiService(mock_http, xml_builder=mock_builder)
        result = service.timbrar(sample_request)

        mock_builder.build.assert_called_once_with(sample_request)
        mock_http.post.assert_called_once_with(
            "api/v1/stamp-cfdi",
            {"xml": "<cfdi:Comprobante .../>"},
        )
        assert result["xml"] == "<cfdi:Comprobante .../>"

    def test_timbrar_xml_posts_raw_xml(self):
        mock_http = MagicMock(spec=HttpClient)
        mock_http.post.return_value = {"xml": "<tfd:TimbreFiscalDigital .../>"}

        service = CfdiService(mock_http)
        result = service.timbrar_xml("<cfdi:Comprobante .../>")

        mock_http.post.assert_called_once_with(
            "api/v1/stamp-cfdi",
            {"xml": "<cfdi:Comprobante .../>"},
        )

    def test_timbrar_uses_default_xml_builder_when_none_given(self, sample_request):
        mock_http = MagicMock(spec=HttpClient)
        mock_http.post.return_value = {"xml": "..."}

        service = CfdiService(mock_http)
        # should not raise — default builder is instantiated internally
        service.timbrar(sample_request)

        assert mock_http.post.called


class TestCfdiXmlBuilder:
    def test_build_ingreso_returns_xml_string(self, sample_request):
        builder = CfdiXmlBuilder()
        xml = builder.build(sample_request)

        assert isinstance(xml, str)
        assert "cfdi:Comprobante" in xml
        assert 'TipoDeComprobante="I"' in xml
        assert 'Version="4.0"' in xml

    def test_build_egreso_comprobante(self, sample_emisor, sample_receptor, sample_concepto):
        request = Cfdi4Request(
            emisor=sample_emisor,
            receptor=sample_receptor,
            conceptos=[sample_concepto],
            tipo_comprobante="E",
            forma_pago="01",
            metodo_pago="PUE",
            moneda="MXN",
            subtotal=Decimal("10000.00"),
            total=Decimal("10000.00"),
            lugar_expedicion="06300",
        )
        builder = CfdiXmlBuilder()
        xml = builder.build(request)

        assert 'TipoDeComprobante="E"' in xml

    def test_build_raises_for_unsupported_tipo(self, sample_emisor, sample_receptor, sample_concepto):
        request = Cfdi4Request(
            emisor=sample_emisor,
            receptor=sample_receptor,
            conceptos=[sample_concepto],
            tipo_comprobante="T",
            forma_pago="01",
            metodo_pago="PUE",
            moneda="MXN",
            subtotal=Decimal("0.00"),
            total=Decimal("0.00"),
            lugar_expedicion="06300",
        )
        builder = CfdiXmlBuilder()

        with pytest.raises(ValueError, match="only supports TipoDeComprobante I and E"):
            builder.build(request)

    def test_build_includes_emisor_rfc(self, sample_request):
        builder = CfdiXmlBuilder()
        xml = builder.build(sample_request)

        assert 'Rfc="XAXX010101000"' in xml

    def test_build_includes_receptor_uso_cfdi(self, sample_request):
        builder = CfdiXmlBuilder()
        xml = builder.build(sample_request)

        assert 'UsoCFDI="G03"' in xml

    def test_build_includes_concepto_descripcion(self, sample_request):
        builder = CfdiXmlBuilder()
        xml = builder.build(sample_request)

        assert "Servicio de desarrollo de software" in xml

    def test_build_uses_provided_fecha(self, sample_emisor, sample_receptor, sample_concepto):
        request = Cfdi4Request(
            emisor=sample_emisor,
            receptor=sample_receptor,
            conceptos=[sample_concepto],
            tipo_comprobante="I",
            forma_pago="01",
            metodo_pago="PUE",
            moneda="MXN",
            subtotal=Decimal("10000.00"),
            total=Decimal("10000.00"),
            lugar_expedicion="06300",
            fecha="2024-01-15T12:00:00",
        )
        builder = CfdiXmlBuilder()
        xml = builder.build(request)

        assert 'Fecha="2024-01-15T12:00:00"' in xml
