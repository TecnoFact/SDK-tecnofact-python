# Guía de Contribución

¡Gracias por tu interés en contribuir al SDK de TecnoFact para Python! 🎉

## 📋 Tabla de Contenidos

- [Código de Conducta](#código-de-conducta)
- [Cómo Contribuir](#cómo-contribuir)
- [Configuración del Entorno](#configuración-del-entorno)
- [Estándares de Código](#estándares-de-código)
- [Proceso de Pull Request](#proceso-de-pull-request)
- [Reportar Bugs](#reportar-bugs)
- [Solicitar Features](#solicitar-features)

## 📜 Código de Conducta

Este proyecto se adhiere a un código de conducta. Al participar, se espera que mantengas este código.

## 🤝 Cómo Contribuir

1. **Fork** el repositorio
2. **Crea** una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. **Commit** tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. **Push** a la rama (`git push origin feature/AmazingFeature`)
5. **Abre** un Pull Request

## 🛠️ Configuración del Entorno

### Requisitos Previos

- Python >= 3.8
- pip
- git

### Instalación

```bash
# Clonar el repositorio
git clone https://github.com/TecnoFact/SDK-tecnofact-python.git
cd SDK-tecnofact-python

# Crear entorno virtual
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# Instalar dependencias de desarrollo
pip install -r requirements-dev.txt
pip install -e .
```

## 📏 Estándares de Código

### Estilo de Código

- Seguir **PEP 8**
- Usar **type hints** en todas las funciones
- Longitud máxima de línea: **100 caracteres**
- Usar **snake_case** para variables y funciones
- Usar **PascalCase** para clases

### Formateo

```bash
# Formatear código con black
black src/tecnofact tests examples

# Ordenar imports con isort
isort src/tecnofact tests examples
```

### Linting

```bash
# Ejecutar flake8
flake8 src/tecnofact tests

# Ejecutar mypy para type checking
mypy src/tecnofact
```

### Testing

```bash
# Ejecutar todos los tests
pytest

# Con cobertura
pytest --cov=tecnofact --cov-report=html

# Tests específicos
pytest tests/test_config.py -v
```

**Requisitos de Testing:**
- Todos los nuevos features deben incluir tests
- La cobertura de código debe mantenerse > 80%
- Todos los tests deben pasar antes de hacer merge

### Documentación

- Agregar **docstrings** a todas las clases y funciones públicas
- Usar formato **Google Style** para docstrings
- Actualizar el README.md si es necesario

Ejemplo de docstring:

```python
def calcular_total(subtotal: Decimal, iva: Decimal) -> Decimal:
    """
    Calcula el total sumando subtotal e IVA.

    Args:
        subtotal: El subtotal de la factura
        iva: El monto del IVA

    Returns:
        El total calculado

    Raises:
        ValueError: Si algún valor es negativo
    """
    if subtotal < 0 or iva < 0:
        raise ValueError("Los valores no pueden ser negativos")
    return subtotal + iva
```

## 🔄 Proceso de Pull Request

1. **Actualiza** tu fork con la rama main más reciente
2. **Asegúrate** de que todos los tests pasen
3. **Ejecuta** los linters y formateadores
4. **Escribe** una descripción clara del PR
5. **Referencia** cualquier issue relacionado

### Checklist del PR

- [ ] Los tests pasan (`pytest`)
- [ ] El código está formateado (`black`, `isort`)
- [ ] El linting pasa (`flake8`, `mypy`)
- [ ] Se agregaron tests para nuevas funcionalidades
- [ ] La documentación está actualizada
- [ ] El CHANGELOG.md está actualizado (si aplica)

## 🐛 Reportar Bugs

Usa el sistema de Issues de GitHub para reportar bugs. Incluye:

- **Descripción clara** del problema
- **Pasos para reproducir** el bug
- **Comportamiento esperado** vs **comportamiento actual**
- **Versión** de Python y del SDK
- **Logs o mensajes de error** relevantes

## ✨ Solicitar Features

Para solicitar nuevas funcionalidades:

1. **Verifica** que no exista un issue similar
2. **Describe** claramente el feature y su caso de uso
3. **Explica** por qué sería útil para otros usuarios
4. **Proporciona** ejemplos de uso si es posible

## 📝 Commits

### Formato de Mensajes de Commit

Usa mensajes de commit descriptivos siguiendo este formato:

```
tipo(alcance): descripción breve

Descripción más detallada si es necesaria.

Fixes #123
```

**Tipos:**
- `feat`: Nueva funcionalidad
- `fix`: Corrección de bug
- `docs`: Cambios en documentación
- `style`: Formateo, punto y coma faltante, etc.
- `refactor`: Refactorización de código
- `test`: Agregar o modificar tests
- `chore`: Mantenimiento, dependencias, etc.

**Ejemplos:**

```
feat(models): agregar modelo para complemento de pago

fix(http): corregir manejo de timeout en requests

docs(readme): actualizar ejemplos de uso

test(config): agregar tests para validación de timeout
```

## 🏗️ Estructura del Proyecto

```
src/tecnofact/
├── config/          # Configuración
├── contracts/       # Interfaces
├── enums/          # Enumeraciones
├── exceptions/     # Excepciones personalizadas
├── http/           # Cliente HTTP
└── models/         # Modelos de datos

tests/              # Tests unitarios
examples/           # Ejemplos de uso
```

## 🔍 Revisión de Código

Los mantenedores revisarán tu PR y pueden:

- Solicitar cambios
- Hacer sugerencias
- Aprobar y hacer merge

Por favor, sé paciente y receptivo al feedback.

## 📞 Contacto

- **Email**: soporte@tecnofact.com
- **Issues**: https://github.com/TecnoFact/SDK-tecnofact-python/issues

---

¡Gracias por contribuir! 🙏
