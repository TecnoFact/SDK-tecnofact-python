# TecnoFact SDK para Facturación Electrónica CFDI 4.0

SDK oficial de Python para la integración con el servicio de Timbrado CFDI 4.0 de TecnoFact. Facilita la emisión, cancelación y consulta de facturas electrónicas cumpliendo con los requisitos del SAT mexicano.

## 📋 Tabla de Contenidos

- [Características](#características)
- [Requisitos](#requisitos)
- [Instalación](#instalación)
- [Configuración](#configuración)
- [Estructura del SDK](#estructura-del-sdk)
- [Uso Básico](#uso-básico)
- [Modelos de Datos](#modelos-de-datos)
- [Manejo de Errores](#manejo-de-errores)
- [Testing](#testing)
- [Contribuciones](#contribuciones)
- [Soporte](#soporte)
- [Licencia](#licencia)

## ✨ Características

- **Timbrado CFDI 4.0**: Emisión de facturas electrónicas cumpliendo con la versión 4.0 del CFDI
- **Timbrado CFDI 3.3**: Soporte retroactivo para facturación CFDI 3.3
- **Cancelación**: Cancelación de CFDIs con diferentes motivos
- **Consultas**: Búsqueda y recuperación de CFDIs timbrados
- **Reportes**: Generación de reportes y estadísticas
- **Validaciones**: Validación de RFCs y catálogos del SAT
- **Health Checks**: Verificación del estado de servicios
- **Tipado Estricto**: Compatible con Python 3.8+ con type hints
- **Manejo de Errores**: Sistema robusto de excepciones personalizadas

## 🔧 Requisitos

- **Python**: >= 3.8
- **Dependencias**: requests, python-dotenv

## 📦 Instalación

### Usando pip

```bash
pip install tecnofact-sdk
```

### Desde el código fuente

```bash
git clone https://github.com/TecnoFact/SDK-tecnofact-python.git
cd SDK-tecnofact-python
pip install -e .
```

### Para desarrollo

```bash
pip install -e ".[dev]"
```

## ⚙️ Configuración

### Constructor Directo

```python
from tecnofact import Config, Environment

config = Config(
    api_key="TU_API_KEY",
    api_secret="TU_API_SECRET",
    environment=Environment.SANDBOX,
    timeout=30,
    retries=3
)

print(f"Entorno: {config.get_environment().label()}")
print(f"URL Base: {config.get_base_url()}")
print(f"Timeout: {config.get_timeout()} segundos")
```

### Variables de Entorno

Crea un archivo `.env`:

```env
TECNOFACT_API_KEY=tu_api_key
TECNOFACT_API_SECRET=tu_api_secret
TECNOFACT_ENVIRONMENT=sandbox
TECNOFACT_TIMEOUT=30
```

```python
import os
from dotenv import load_dotenv
from tecnofact import Config, Environment

load_dotenv()

config = Config(
    api_key=os.getenv("TECNOFACT_API_KEY"),
    api_secret=os.getenv("TECNOFACT_API_SECRET"),
    environment=Environment[os.getenv("TECNOFACT_ENVIRONMENT", "SANDBOX").upper()],
    timeout=int(os.getenv("TECNOFACT_TIMEOUT", "30"))
)
```

## 🏗️ Estructura del SDK

```
src/tecnofact/
├── config/
│   └── config.py              # Configuración inmutable del SDK
├── contracts/
│   └── http_client_interface.py  # Interfaz para el cliente HTTP
├── enums/
│   ├── environment.py         # Entornos (Sandbox/Production)
│   └── tipo_comprobante.py    # Tipos de CFDI
├── exceptions/
│   ├── tecnofact_exception.py      # Excepción base
│   ├── authentication_exception.py # Error de autenticación
│   ├── validation_exception.py     # Error de validación
│   ├── timbrado_exception.py       # Error de timbrado
│   ├── cancelacion_exception.py    # Error de cancelación
│   ├── not_found_exception.py      # Recurso no encontrado
│   ├── rate_limit_exception.py     # Límite de peticiones
│   └── server_exception.py         # Error del servidor
├── http/
│   └── http_client.py         # Cliente HTTP con requests
└── models/
    ├── emisor.py              # Datos del emisor
    ├── receptor.py            # Datos del receptor
    ├── concepto.py            # Conceptos de factura
    ├── cfdi4_request.py       # Solicitud CFDI 4.0
    ├── cfdi_relacionados.py   # CFDIs relacionados
    ├── impuestos.py           # Impuestos globales
    ├── impuestos_concepto.py  # Impuestos por concepto
    ├── traslado.py            # Traslado de impuestos
    ├── traslado_global.py     # Traslado global
    ├── retencion.py           # Retención de impuestos
    ├── retencion_global.py    # Retención global
    ├── cuenta_predial.py      # Cuenta predial
    ├── informacion_aduanera.py # Información aduanera
    └── parte.py               # Partes/componentes
```

## 💻 Uso Básico

### Ejemplo: Crear Configuración

```python
from tecnofact import Config, Environment

config = Config(
    api_key="TU_API_KEY",
    api_secret="TU_API_SECRET",
    environment=Environment.SANDBOX,
    timeout=30,
    retries=3
)

print(f"Entorno: {config.get_environment().label()}")
print(f"URL Base: {config.get_base_url()}")
print(f"Timeout: {config.get_timeout()} segundos")

# Convertir a diccionario
data = config.to_dict()
print(data)
```

### Ejemplo: Enum Environment

```python
from tecnofact.enums import Environment

# Usar enum con autocompletado
env = Environment.PRODUCTION

if env == Environment.PRODUCTION:
    print("Entorno de producción")

# Métodos del enum
print(env.value)           # 'production'
print(env.is_production()) # True
print(env.is_sandbox())    # False
print(env.label())         # 'Producción'
```

## 📋 Modelos de Datos

### Emisor

```python
from tecnofact.models import Emisor

emisor = Emisor(
    rfc="XAXX010101000",
    nombre="EMPRESA EMISORA SA DE CV",
    regimen_fiscal="601",
    cp="06300"
)

print(emisor.get_rfc())     # XAXX010101000
print(emisor.get_nombre())  # EMPRESA EMISORA SA DE CV
print(emisor.to_dict())
```

### Receptor

```python
from tecnofact.models import Receptor

receptor = Receptor(
    rfc="XAXX010101001",
    nombre="CLIENTE RECEPTOR",
    uso_cfdi="G03",
    domicilio_fiscal_receptor="06300",
    regimen_fiscal_receptor="612"
)
```

### Concepto con Impuestos

```python
from decimal import Decimal
from tecnofact.models import Concepto, ImpuestosConcepto, Traslado

concepto = Concepto(
    clave_prod_serv="01010101",
    cantidad=Decimal("1"),
    clave_unidad="E48",
    descripcion="Servicio de desarrollo de software",
    valor_unitario=Decimal("10000.00"),
    importe=Decimal("10000.00"),
    objeto_imp="02",  # Sí objeto de impuesto
    impuestos=ImpuestosConcepto(
        traslados=[
            Traslado(
                base=Decimal("10000.00"),
                impuesto="002",  # IVA
                tipo_factor="Tasa",
                tasa_o_cuota=Decimal("0.160000"),
                importe=Decimal("1600.00")
            )
        ]
    )
)
```

## ⚠️ Manejo de Errores

El SDK proporciona excepciones específicas para diferentes tipos de errores:

```python
from tecnofact.exceptions import (
    TecnoFactException,
    AuthenticationException,
    ValidationException,
    TimbradoException,
    NotFoundException,
    RateLimitException,
    ServerException
)

try:
    # Tu código aquí
    pass
except AuthenticationException as e:
    print(f"Error de autenticación: {e}")
    print(f"Detalles: {e.get_details()}")
except ValidationException as e:
    print(f"Error de validación: {e}")
except TimbradoException as e:
    print(f"Error en timbrado: {e}")
except NotFoundException as e:
    print(f"Recurso no encontrado: {e}")
except RateLimitException as e:
    print(f"Límite de peticiones excedido: {e}")
except ServerException as e:
    print(f"Error del servidor: {e}")
except TecnoFactException as e:
    print(f"Error general: {e}")
```

## 🧪 Testing

### Ejecutar Tests

```bash
# Instalar dependencias de desarrollo
pip install -e ".[dev]"

# Ejecutar todos los tests
pytest

# Ejecutar con cobertura
pytest --cov=tecnofact --cov-report=html

# Ejecutar tests específicos
pytest tests/test_config.py
```

### Análisis Estático

```bash
# Type checking con mypy
mypy src/tecnofact

# Linting con flake8
flake8 src/tecnofact

# Formateo con black
black src/tecnofact

# Ordenar imports con isort
isort src/tecnofact
```

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor:

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

### Estándares de Código

- Seguir PEP 8
- Usar type hints
- Escribir docstrings
- Mantener cobertura de tests > 80%
- Pasar todos los checks de linting y type checking

## 💬 Soporte

- **Email**: soporte@tecnofact.com
- **Documentación**: https://docs.tecnofact.com
- **Issues**: https://github.com/TecnoFact/SDK-tecnofact-python/issues

## 📄 Licencia

Este proyecto está licenciado bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para más detalles.

## 🏢 Sobre TecnoFact

TecnoFact es un proveedor autorizado de certificación (PAC) que ofrece servicios de timbrado de CFDI cumpliendo con todos los requisitos del SAT mexicano.

### Características del Servicio

- ✅ PAC Autorizado por el SAT
- ✅ Disponibilidad 99.9%
- ✅ Soporte técnico especializado
- ✅ Precios competitivos
- ✅ API REST moderna
- ✅ Documentación completa
- ✅ SDKs en múltiples lenguajes

---

Desarrollado con ❤️ por TecnoFact
