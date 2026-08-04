from typing import Dict, Any
from ..http.http_client import HttpClient
from ..exceptions import TimbradoException
from ..xml.cfdi_xml_builder import CfdiXmlBuilder
from ..models.cfdi4_request import Cfdi4Request


class CfdiService:
    """Handles CFDI stamping (timbrado) via POST /api/v1/stamp-cfdi.

    Requires an authenticated :class:`~tecnofact.http.HttpClient` (i.e. one
    that already has a Bearer token set from :class:`AuthService`).

    Usage::

        config = Config(email="user@example.com", password="secret")
        auth = AuthService(config)
        auth.login()

        cfdi_service = CfdiService(auth.get_http_client())
        result = cfdi_service.timbrar(cfdi_request)
        tfd_xml = result["xml"]
    """

    _ENDPOINT = "api/v1/stamp-cfdi"

    def __init__(
        self,
        http_client: HttpClient,
        xml_builder: CfdiXmlBuilder | None = None,
    ):
        self._http = http_client
        self._builder = xml_builder or CfdiXmlBuilder()

    def timbrar(self, request: Cfdi4Request) -> Dict[str, Any]:
        """Build the CFDI 4.0 XML and POST it to /api/v1/stamp-cfdi.

        :param request: A fully populated :class:`~tecnofact.models.Cfdi4Request`.
        :returns: The JSON response from the PAC, typically containing
                  ``{"xml": "<cfdi:Comprobante ...>...</cfdi:Comprobante>"}``
                  with the timbrado (Timbre Fiscal Digital) embedded.
        :raises TimbradoException: When the PAC returns an error response.
        """
        xml_string = self._builder.build(request)
        return self._http.post(self._ENDPOINT, {"xml": xml_string})

    def timbrar_xml(self, xml: str) -> Dict[str, Any]:
        """POST a pre-built XML string directly to /api/v1/stamp-cfdi.

        Use this when the XML was built externally (e.g. by a third-party
        library) and you only need the timbrado step.

        :param xml: Raw CFDI 4.0 XML string.
        :returns: PAC JSON response.
        """
        return self._http.post(self._ENDPOINT, {"xml": xml})
