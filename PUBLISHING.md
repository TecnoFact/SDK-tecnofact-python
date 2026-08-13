# Guía de Publicación en PyPI

Esta guía explica cómo publicar el SDK de TecnoFact en PyPI.

## 📋 Pre-requisitos

1. **Cuenta en PyPI**
   - Crear cuenta en https://pypi.org/account/register/
   - Crear cuenta en https://test.pypi.org/account/register/ (para pruebas)

2. **Configurar Trusted Publishing en PyPI**
   - Ir a https://pypi.org/manage/project/tecnofact-sdk/publishing/
   - Agregar un "Trusted Publisher" con estos datos:
     - **Owner:** `TecnoFact`
     - **Repository name:** `SDK-tecnofact-python`
     - **Workflow name:** `publish.yml`
     - **Environment name:** `pypi`

   Esto permite que GitHub Actions publique en PyPI sin necesidad de guardar tokens de API en los secretos del repositorio.

## 🔄 Flujo de publicación

El proyecto usa **releases manuales en GitHub** y **Trusted Publishing** para subir a PyPI.

### 1. Preparar el bump de versión

Crear una rama y actualizar la versión en ambos archivos:

- `pyproject.toml` → campo `version`
- `src/tecnofact/__init__.py` → variable `__version__`

También actualizar `CHANGELOG.md` con los cambios de la nueva versión.

```bash
git checkout -b bump/v1.1.0
git add pyproject.toml src/tecnofact/__init__.py CHANGELOG.md
git commit -m "chore: bump version to 1.1.0"
git push origin bump/v1.1.0
```

Abrir un pull request hacia `main`. El workflow `Version Check` verificará que ambas versiones coincidan y que se haya incrementado respecto a `main`.

### 2. Mergear a `main`

Una vez aprobado el PR, mergear a `main`. Los workflows `Tests` y `Version Check` deben estar en verde.

### 3. Crear el release en GitHub

Ir a https://github.com/TecnoFact/SDK-tecnofact-python/releases/new y crear un release:

- **Tag:** `v1.1.0`
- **Target:** `main`
- **Title:** `Release 1.1.0`
- **Description:** Copiar los cambios desde `CHANGELOG.md`

Publicar el release. Esto dispara automáticamente el workflow `.github/workflows/publish.yml`.

### 4. Verificar la publicación

El workflow `Publish to PyPI`:

1. Ejecuta los tests en Python 3.8, 3.9, 3.10, 3.11 y 3.12.
2. Construye el paquete con `python -m build`.
3. Publica los artefactos en PyPI usando Trusted Publishing.

Se puede ver el progreso en la pestaña **Actions** del repositorio.

### 5. Confirmar en PyPI

Visitar https://pypi.org/project/tecnofact-sdk/ y verificar que la nueva versión esté disponible.

Probar la instalación:

```bash
pip install tecnofact-sdk
```

## 🧪 Probar en TestPyPI (opcional)

Para validar la publicación antes de hacerla oficial, se puede construir e instalar localmente:

```bash
make clean
make verify
make build
make upload-test
```

O bien, crear un release de pre-release en GitHub (por ejemplo, `v1.1.0-rc.1`). El workflow `publish.yml` se dispara igual, pero PyPI no acepta versiones de pre-release a menos que el proyecto esté configurado para ello.

## 🔧 Solución de Problemas

### Error: "File already exists"

- Ya existe esa versión en PyPI.
- Incrementar el número de versión en `pyproject.toml` y `src/tecnofact/__init__.py`.

### Error: "Invalid distribution"

- Ejecutar `make check` para ver detalles.
- Verificar que `README.md` sea Markdown válido.
- Verificar que todos los archivos necesarios estén en `MANIFEST.in`.

### Error: "Authentication failed"

- Verificar que el Trusted Publisher esté configurado en PyPI con los datos correctos:
  - Owner: `TecnoFact`
  - Repository: `SDK-tecnofact-python`
  - Workflow: `publish.yml`
  - Environment: `pypi`
- Verificar que el job de publicación en `publish.yml` tenga `permissions: id-token: write`.

### El workflow no se ejecuta al crear el release

- Verificar que el release se haya publicado (no guardado como borrador).
- Revisar en **Actions** → **Publish to PyPI** si hay algún error.

## ✅ Checklist de Publicación

Antes de cada publicación, verificar:

- [ ] Tests pasan (`make test`)
- [ ] Linting pasa (`make lint`)
- [ ] `MANIFEST.in` está actualizado (`make check`)
- [ ] Versión actualizada en `pyproject.toml` y `src/tecnofact/__init__.py`
- [ ] `CHANGELOG.md` actualizado
- [ ] PR aprobado y mergeado a `main`
- [ ] Release creado en GitHub con el tag correcto
- [ ] Workflow `Publish to PyPI` finalizó correctamente
- [ ] Paquete disponible en https://pypi.org/project/tecnofact-sdk/

## 📚 Referencias

- [PyPI Documentation](https://docs.pypi.org/)
- [Python Packaging Guide](https://packaging.python.org/)
- [Trusted Publishing](https://docs.pypi.org/trusted-publishers/)
- [Semantic Versioning](https://semver.org/)
