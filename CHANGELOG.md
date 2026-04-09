# Changelog

Todos los cambios notables en este proyecto serán documentados en este archivo.

El formato está basado en [Keep a Changelog](https://keepachangelog.com/es-ES/1.0.0/),
y este proyecto adhiere a [Semantic Versioning](https://semver.org/lang/es/).

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

[1.0.0]: https://github.com/TecnoFact/SDK-tecnofact-python/releases/tag/v1.0.0
