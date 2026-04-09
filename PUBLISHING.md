# Guía de Publicación en PyPI

Esta guía explica cómo publicar el SDK de TecnoFact en PyPI.

## 📋 Pre-requisitos

1. **Cuenta en PyPI**
   - Crear cuenta en https://pypi.org/account/register/
   - Crear cuenta en https://test.pypi.org/account/register/ (para pruebas)

2. **API Tokens**
   - Generar token en https://pypi.org/manage/account/token/
   - Generar token en https://test.pypi.org/manage/account/token/

3. **Configurar credenciales**
   ```bash
   # Copiar el archivo de ejemplo
   cp .pypirc.example ~/.pypirc
   
   # Editar y agregar tus tokens
   nano ~/.pypirc
   ```

## 🔍 Verificación Pre-publicación

Antes de publicar, ejecutar todas las verificaciones:

```bash
# Verificar todo (linting, tests, manifest, metadata)
make verify

# O paso por paso:
make lint      # Verificar estilo de código
make test      # Ejecutar tests
make check     # Verificar MANIFEST.in y metadata
```

## 🧪 Publicar en TestPyPI (Recomendado primero)

TestPyPI es un entorno de prueba para practicar la publicación:

```bash
# 1. Limpiar builds anteriores
make clean

# 2. Construir el paquete
make build

# 3. Subir a TestPyPI
make upload-test
```

### Probar la instalación desde TestPyPI

```bash
# Crear un entorno virtual de prueba
python -m venv test-env
source test-env/bin/activate  # En Windows: test-env\Scripts\activate

# Instalar desde TestPyPI
pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ tecnofact-sdk

# Probar que funciona
python -c "from tecnofact import Config, Environment; print('OK')"
```

## 🚀 Publicar en PyPI (Producción)

Una vez verificado en TestPyPI:

```bash
# 1. Asegurar que la versión en pyproject.toml es correcta
# 2. Actualizar CHANGELOG.md
# 3. Crear un tag de git

git tag -a v1.0.0 -m "Release version 1.0.0"
git push origin v1.0.0

# 4. Publicar
make upload
```

## 📦 Verificar la publicación

1. Visitar https://pypi.org/project/tecnofact-sdk/
2. Verificar que la metadata se muestra correctamente
3. Probar instalación:
   ```bash
   pip install tecnofact-sdk
   ```

## 🔄 Publicar una nueva versión

1. **Actualizar versión**
   - Editar `pyproject.toml` → cambiar `version`
   - Editar `src/tecnofact/__init__.py` → cambiar `__version__`

2. **Actualizar CHANGELOG.md**
   ```markdown
   ## [1.1.0] - 2024-XX-XX
   ### Added
   - Nueva funcionalidad X
   ### Fixed
   - Corrección de bug Y
   ```

3. **Commit y tag**
   ```bash
   git add .
   git commit -m "chore: bump version to 1.1.0"
   git tag -a v1.1.0 -m "Release version 1.1.0"
   git push origin main
   git push origin v1.1.0
   ```

4. **Publicar**
   ```bash
   make clean
   make verify
   make upload
   ```

## 🤖 Publicación Automática con GitHub Actions

El proyecto ya tiene configurado GitHub Actions para publicación automática:

1. **Crear un Release en GitHub**
   - Ir a https://github.com/TecnoFact/SDK-tecnofact-python/releases/new
   - Tag: `v1.0.0`
   - Title: `Release 1.0.0`
   - Description: Copiar desde CHANGELOG.md
   - Publicar release

2. **Configurar secreto en GitHub**
   - Ir a Settings → Secrets → Actions
   - Agregar `PYPI_API_TOKEN` con tu token de PyPI

3. **El workflow se ejecutará automáticamente**
   - Construirá el paquete
   - Lo publicará en PyPI

## ✅ Checklist de Publicación

Antes de cada publicación, verificar:

- [ ] Tests pasan (`make test`)
- [ ] Linting pasa (`make lint`)
- [ ] MANIFEST.in está actualizado (`make check`)
- [ ] Versión actualizada en `pyproject.toml` y `__init__.py`
- [ ] CHANGELOG.md actualizado
- [ ] README.md actualizado si es necesario
- [ ] Commit y push de todos los cambios
- [ ] Tag de git creado
- [ ] Probado en TestPyPI
- [ ] Verificación final (`make verify`)

## 🔧 Solución de Problemas

### Error: "File already exists"
- Ya existe esa versión en PyPI
- Incrementar el número de versión

### Error: "Invalid distribution"
- Ejecutar `make check` para ver detalles
- Verificar que README.md es válido Markdown
- Verificar que todos los archivos necesarios están en MANIFEST.in

### Error: "Authentication failed"
- Verificar que el token en `~/.pypirc` es correcto
- Verificar que el token no ha expirado

### Archivos faltantes en el paquete
- Actualizar MANIFEST.in
- Ejecutar `check-manifest` para verificar

## 📚 Referencias

- [PyPI Documentation](https://docs.pypi.org/)
- [Python Packaging Guide](https://packaging.python.org/)
- [Twine Documentation](https://twine.readthedocs.io/)
- [Semantic Versioning](https://semver.org/)
