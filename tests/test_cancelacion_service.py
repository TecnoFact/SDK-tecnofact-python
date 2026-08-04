import pytest
from unittest.mock import MagicMock
from tecnofact.services import CancelacionService
from tecnofact.http import HttpClient


class TestCancelacionService:
    def test_cancelar_posts_to_endpoint(self):
        mock_http = MagicMock(spec=HttpClient)
        mock_http.post.return_value = {"status": "cancelled"}

        service = CancelacionService(mock_http)
        result = service.cancelar(
            uuid="6128396f-c09b-4ec6-8699-43c5f7e3b230",
            rfc_emisor="AAA010101AAA",
            motivo="02",
        )

        mock_http.post.assert_called_once_with(
            "api/v1/cancel-cfdi",
            {
                "uuid": "6128396f-c09b-4ec6-8699-43c5f7e3b230",
                "rfc_emisor": "AAA010101AAA",
                "motivo": "02",
            },
        )
        assert result["status"] == "cancelled"

    def test_cancelar_includes_folio_sustitucion_when_provided(self):
        mock_http = MagicMock(spec=HttpClient)
        mock_http.post.return_value = {"status": "cancelled"}

        service = CancelacionService(mock_http)
        service.cancelar(
            uuid="6128396f-c09b-4ec6-8699-43c5f7e3b230",
            rfc_emisor="AAA010101AAA",
            motivo="01",
            folio_sustitucion="aaaa396f-c09b-4ec6-8699-43c5f7e3b999",
        )

        call_args = mock_http.post.call_args
        payload = call_args[0][1]
        assert payload["folio_sustitucion"] == "aaaa396f-c09b-4ec6-8699-43c5f7e3b999"

    def test_cancelar_omits_folio_sustitucion_when_not_given(self):
        mock_http = MagicMock(spec=HttpClient)
        mock_http.post.return_value = {}

        service = CancelacionService(mock_http)
        service.cancelar(
            uuid="6128396f-c09b-4ec6-8699-43c5f7e3b230",
            rfc_emisor="AAA010101AAA",
            motivo="02",
        )

        call_args = mock_http.post.call_args
        payload = call_args[0][1]
        assert "folio_sustitucion" not in payload
