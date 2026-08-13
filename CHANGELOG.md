# Changelog

Todos los cambios notables en este proyecto serán documentados en este archivo.

El formato está basado en [Keep a Changelog](https://keepachangelog.com/es-ES/1.0.0/),
y este proyecto adhiere a [Semantic Versioning](https://semver.org/lang/es/).

## [Unreleased]

## [1.1.1] - 2026-08-13

### Corregido
- Renombrado el proyecto en PyPI de `tecnofact-sdk` a `sdk-tecnofact-python` para coincidir con el proyecto existente en PyPI.
- Corregida la cadena de workflows de GitHub Actions para que `create-release.yml` dispare explícitamente `publish.yml` después de crear un release.

## [1.1.0] - 2026-08-13

### Agregado

#### Complemento de Pagos 2.0 (TipoDeComprobante = "P")
- `PagoRequest` — entrada simplificada; el SDK genera automáticamente `Moneda=XXX`, `SubTotal=0`, `Total=0`, el `Concepto` fijo (84111506/ACT/Pago/0/0/01) y `pago20:Totales.MontoTotalPagos`.
- `Pago` — representa un nodo `pago20:Pago` (FechaPago, FormaDePagoP, MonedaP, TipoCambioP, Monto).
- `DoctoRelacionado` — representa `pago20:DoctoRelacionado` (IdDocumento, MonedaDR, EquivalenciaDR, NumParcialidad, ImpSaldoAnt, ImpPagado, ImpSaldoInsoluto, ObjetoImpDR, Serie?, Folio?).
- `CfdiXmlBuilder.build_pago(pago_request)` — construye el XML Pagos 2.0 completo con declaración `xmlns:pago20` correcta en el `Comprobante` raíz, `schemaLocation` extendido con Pagos20.xsd, y `cfdi:Complemento > pago20:Pagos`.
- `CfdiService.timbrar_pago(pago_request) -> ResultadoTimbrado` — nuevo método para timbrar comprobantes de pago.

#### CFDI XML Builder — nodos a nivel concepto
- El builder emite `cfdi:InformacionAduanera` (NumeroPedimento), `cfdi:CuentaPredial` (Numero) y `cfdi:Parte` dentro de `cfdi:Concepto`, respetando el orden del XSD (Impuestos → InformacionAduanera → CuentaPredial → Parte).
- `Concepto`: campo opcional `descuento` agregado.

#### CFDI XML Builder (núcleo)
- `CfdiXmlBuilder.build(cfdi4_request)` — construye XML CFDI 4.0 para tipos `I` (Ingreso) y `E` (Egreso) usando `xml.etree.ElementTree` / `lxml`; fuerza el orden de elementos del XSD, formateo de decimales por campo (TasaOCuota 6 decimales, importes 2), y reglas condicionales por TipoDeComprobante.
- `InformacionGlobal` — `Periodicidad`, `Meses`, `Año` para facturas globales (público en general).
- `CfdiService.timbrar(cfdi4_request) -> ResultadoTimbrado` — construye el XML internamente y envía `{"xml": "..."}` a `/api/v1/stamp-cfdi`; el panel maneja el sellado (CSD) y el timbrado. El SDK nunca toca la llave privada.

#### Nuevos endpoints API
- `CfdiService.validar(xml: str) -> EstatusCfdi` — POST `/api/v1/validation-cfdi` como `multipart/form-data` con campo `xml`; devuelve `EstatusCfdi` tipado.
- `CancelacionService.cancelar(rfc: str, uuid: str, motivo: str) -> AcuseCancelacion` — POST `/api/v1/cancelled-cfdi` con JSON `{rfc, uuid, motivo}`; devuelve `AcuseCancelacion` tipado.

#### Objetos de respuesta tipados (`tecno_fact/responses/`)
- `ResultadoTimbrado` — devuelto por `timbrar()`, `timbrar_xml()`, `timbrar_pago()`; expone `is_success()`, `get_xml_timbrado()`, `get_uuid()`, `get_code()`, `get_message()`, `get_raw()`.
- `EstatusCfdi` — devuelto por `validar()`; expone `is_vigente()`, `get_estado()`, `get_codigo()`, `get_es_cancelable()`, `get_efos()`, `get_raw()`.
- `AcuseCancelacion` — devuelto por `cancelar()`; expone `is_aceptada_por_sat()`, `get_uuid()`, `get_xml()`, `get_pdf_base64()`, `get_pdf_binario()` (decodifica base64 a bytes crudos), `get_raw()`.

#### Cliente HTTP
- `HttpClient.post_multipart()` — soporte para POST `multipart/form-data`; permite enviar archivos y campos mixtos.

#### Configuración TLS
- `Config.verify_ssl` (`bool | str`, default `True`) — pasa `True` para el CA bundle del sistema, una ruta de archivo para un bundle PEM personalizado (p. ej. cuando el servidor tiene cadena incompleta), o `False` para deshabilitar la verificación (solo desarrollo).
- Variable de entorno `TECN_FACT_VERIFY_SSL` soportada por `Config.from_environment()`.

### Cambiado

#### Config
- Credenciales de autenticación cambiadas de `api_key`/`api_secret` a `email`/`password` (corresponde a la API real del panel).
- Variables de entorno renombradas: `TECN_FACT_API_KEY` → `TECN_FACT_EMAIL`, `TECN_FACT_API_SECRET` → `TECN_FACT_PASSWORD`.
- `Environment.SANDBOX` eliminado (solo `PRODUCTION` disponible); método `is_sandbox()` eliminado.
- `Cfdi4Request`: reemplazado `sub_total_con_descuento` (campo inválido) por `informacion_global: InformacionGlobal | None`.
- `Emisor`: campo `cp` mantenido en el modelo por compatibilidad; el builder XML no lo emite (no es un atributo válido de Emisor en CFDI 4.0). `fac_atr_adm` mapea al atributo XML correcto `FacAtrAdquirente`.
- `CancelacionService.cancelar()` — firma actualizada a `(rfc, uuid, motivo)` y endpoint cambiado de `/cancelacion/cancelar` a `/api/v1/cancelled-cfdi`.
- `TrasladoGlobal`: atributo requerido `base` agregado (CFDI 4.0); `importe` ahora es nullable para casos Exento.
- `RetencionGlobal`: simplificado a `(impuesto, importe)` únicamente — el nodo `Retencion` a nivel comprobante no debe incluir `TipoFactor` ni `TasaOCuota`.
- `baseUrl` fija a `https://panelcfdi.tecnofact.mx` (sin sufijo `/v1`; solo el timbrado usa `/api/v1/`).
- Login apunta a `POST /api/login` con `{email, password}`; la respuesta devuelve `access_token` (formato `NNN|...`). Autenticación vía `Authorization: Bearer <token>`. Headers `X-API-Key` / `X-API-Secret` eliminados.
- La `Fecha` del CFDI la provee el caller (usuario del SDK); el builder no la genera ni la sobreescribe.

### Corregido
- `HttpClient` ahora lee los campos `error` y `mensaje` además de `message` al parsear errores, de modo que los mensajes reales del panel (p. ej. códigos de validación del SAT) se propagan en lugar del genérico "Error desconocido".

### Seguridad
- `verify_ssl` nunca tiene default `False`; deshabilitar la verificación TLS requiere opt-in explícito.

---

## [1.0.0] - 2024-01-01

### Agregado
- Configuración inmutable del SDK con validaciones
- Soporte para entornos Sandbox y Production
- Enumeraciones para Environment y TipoComprobante
- Sistema completo de excepciones personalizadas:
  - TecnoFactException (base)
  - AuthenticationException
  - ValidationException
  - TimbradoException
  - CancelacionException
  - NotFoundException
  - RateLimitException
  - ServerException
- Cliente HTTP con manejo automático de errores
- Modelos de datos completos para CFDI 4.0:
  - Emisor
  - Receptor
  - Concepto
  - Impuestos (concepto y globales)
  - Traslados y Retenciones
  - CfdiRelacionados
  - Cfdi4Request
  - CuentaPredial
  - InformacionAduanera
  - Parte
- Suite completa de tests unitarios
- Documentación en español
- Ejemplos de uso
- Soporte para type hints
- Configuración via variables de entorno

### Características
- Compatible con Python 3.8+
- Type hints completos
- Cobertura de tests > 80%
- Documentación completa
- Ejemplos funcionales
- Manejo robusto de errores
- Serialización a diccionarios

[1.1.1]: https://github.com/TecnoFact/SDK-tecnofact-python/releases/tag/v1.1.1
[1.1.0]: https://github.com/TecnoFact/SDK-tecnofact-python/releases/tag/v1.1.0
[1.0.0]: https://github.com/TecnoFact/SDK-tecnofact-python/releases/tag/v1.0.0
