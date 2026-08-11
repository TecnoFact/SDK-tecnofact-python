from typing import Dict, Any, Optional
from ..http.http_client import HttpClient
from ..exceptions import CancelacionException


class CancelacionService:
    """Skeleton for CFDI cancellation operations.

    .. note::
        This service is a placeholder. Cancellation endpoints and payload
        shapes will be defined once the Tecnofact API documentation for
        cancellation is available.

    Usage::

        config = Config(email="user@example.com", password="secret")
        auth = AuthService(config)
        auth.login()

        cancelacion = CancelacionService(auth.get_http_client())
        result = cancelacion.cancelar(uuid="...", rfc_emisor="AAA010101AAA", motivo="02")
    """

    _ENDPOINT = "api/v1/cancel-cfdi"

    def __init__(self, http_client: HttpClient):
        self._http = http_client

    def cancelar(
        self,
        uuid: str,
        rfc_emisor: str,
        motivo: str,
        folio_sustitucion: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Request cancellation for a stamped CFDI.

        :param uuid: UUID of the CFDI to cancel.
        :param rfc_emisor: RFC of the issuing taxpayer.
        :param motivo: Cancellation motive code (e.g. "01", "02", "03", "04").
        :param folio_sustitucion: Required when motivo is "01" (replaced by
            another CFDI); UUID of the replacement document.
        :returns: PAC JSON response with the cancellation acknowledgment.
        :raises CancelacionException: When the PAC returns an error.
        """
        payload: Dict[str, Any] = {
            "uuid": uuid,
            "rfc_emisor": rfc_emisor,
            "motivo": motivo,
        }
        if folio_sustitucion:
            payload["folio_sustitucion"] = folio_sustitucion

        return self._http.post(self._ENDPOINT, payload)
