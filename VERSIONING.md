# Guía de Versionado

Este proyecto utiliza [Semantic Versioning](https://semver.org/lang/es/) y automatización con GitHub Actions para gestionar versiones y releases.

## 📋 Semantic Versioning

El formato de versión es: `MAJOR.MINOR.PATCH`

- **MAJOR** (X.0.0): Cambios incompatibles con versiones anteriores
- **MINOR** (0.X.0): Nueva funcionalidad compatible con versiones anteriores
- **PATCH** (0.0.X): Correcciones de bugs compatibles con versiones anteriores

## 🤖 Versionado Automático

El proyecto usa **Python Semantic Release** para generar versiones automáticamente basándose en los mensajes de commit.

### Conventional Commits

Los commits deben seguir el formato [Conventional Commits](https://www.conventionalcommits.org/):

```
<tipo>[alcance opcional]: <descripción>

[cuerpo opcional]

[nota(s) al pie opcional(es)]
```

### Tipos de Commit y su Impacto

| Tipo | Incremento de Versión | Ejemplo |
|------|----------------------|---------|
| `feat:` | MINOR (0.X.0) | `feat(models): agregar modelo de pago` |
| `fix:` | PATCH (0.0.X) | `fix(http): corregir timeout en requests` |
| `perf:` | PATCH (0.0.X) | `perf(config): optimizar carga de configuración` |
| `BREAKING CHANGE:` | MAJOR (X.0.0) | Ver ejemplo abajo |
| `docs:`, `style:`, `refactor:`, `test:`, `build:`, `ci:` | PATCH (0.0.X) | `docs(readme): actualizar ejemplos` |
| `chore:` | No genera release | `chore: actualizar dependencias` |

### Ejemplos de Commits

#### Feature (MINOR)
```bash
git commit -m "feat(models): agregar soporte para complemento de pago

- Implementar modelo ComplementoPago
- Agregar validaciones SAT
- Incluir tests completos"
```

#### Fix (PATCH)
```bash
git commit -m "fix(http): corregir manejo de timeout

Fixes #123"
```

#### Breaking Change (MAJOR)
```bash
git commit -m "feat(config)!: cambiar estructura de configuración

BREAKING CHANGE: Config ahora requiere api_version como parámetro obligatorio.
Migración: agregar api_version='4.0' al constructor de Config."
```

O alternativamente:
```bash
git commit -m "feat(config): cambiar estructura de configuración

BREAKING CHANGE: Config ahora requiere api_version como parámetro obligatorio.
Migración: agregar api_version='4.0' al constructor de Config."
```

## 🔄 Flujo de Trabajo

### 1. Desarrollo Normal

```bash
# Hacer cambios
git add .

# Commit con conventional commits
git commit -m "feat(models): agregar nuevo modelo"

# Push a main
git push origin main
```

### 2. GitHub Actions Automático

Cuando haces push a `main`:

1. **Analiza commits** desde el último release
2. **Determina el tipo de versión** (major, minor, patch)
3. **Actualiza archivos**:
   - `pyproject.toml`
   - `src/tecnofact/__init__.py`
   - `CHANGELOG.md`
4. **Crea commit de release** con `[skip ci]`
5. **Crea tag de git** (ej: `v1.2.0`)
6. **Crea GitHub Release** con notas automáticas
7. **Publica en PyPI** (si está configurado)

### 3. Verificación

```bash
# Ver el nuevo tag
git fetch --tags
git tag -l

# Ver el changelog actualizado
cat CHANGELOG.md

# Verificar en GitHub
# https://github.com/TecnoFact/SDK-tecnofact-python/releases
```

## 📝 CHANGELOG Automático

El `CHANGELOG.md` se genera automáticamente con:

- **✨ Features**: Nuevas funcionalidades (`feat:`)
- **🐛 Bug Fixes**: Correcciones (`fix:`)
- **⚡ Performance**: Mejoras de rendimiento (`perf:`)
- **📚 Documentation**: Cambios en docs (`docs:`)
- **♻️ Refactoring**: Refactorizaciones (`refactor:`)
- **✅ Tests**: Cambios en tests (`test:`)
- **🔧 Build**: Cambios en build (`build:`)
- **👷 CI/CD**: Cambios en CI (`ci:`)

### Ejemplo de CHANGELOG Generado

```markdown
## [1.2.0] - 2024-01-15

### ✨ Features
- **models**: agregar soporte para complemento de pago ([a1b2c3d](link))
- **http**: implementar retry automático ([e4f5g6h](link))

### 🐛 Bug Fixes
- **config**: corregir validación de timeout ([i7j8k9l](link))

### 📚 Documentation
- **readme**: actualizar ejemplos de uso ([m0n1o2p](link))
```

## 🚫 Saltar CI

Para commits que no deben generar release:

```bash
git commit -m "chore: actualizar dependencias [skip ci]"
```

O usar tipo `chore:` que no genera release automáticamente.

## 🔧 Versionado Manual (No Recomendado)

Si necesitas hacer un release manual:

1. **Actualizar versión manualmente**:
   ```bash
   # Editar pyproject.toml
   version = "1.2.0"
   
   # Editar src/tecnofact/__init__.py
   __version__ = "1.2.0"
   ```

2. **Actualizar CHANGELOG.md**

3. **Commit y tag**:
   ```bash
   git add .
   git commit -m "chore(release): 1.2.0 [skip ci]"
   git tag -a v1.2.0 -m "Release 1.2.0"
   git push origin main --tags
   ```

4. **Crear release en GitHub manualmente**

## 🐛 Solución de Problemas

### El release no se generó

- Verifica que los commits usen conventional commits
- Revisa que haya commits de tipo `feat:` o `fix:` desde el último release
- Verifica los logs de GitHub Actions

### Versión incorrecta

- El versionado es automático basado en commits
- Para forzar una versión específica, usa release manual

### CHANGELOG no se actualiza

- Verifica que el workflow de release tenga permisos de escritura
- Revisa que `GITHUB_TOKEN` tenga permisos correctos

## 📚 Referencias

- [Semantic Versioning](https://semver.org/lang/es/)
- [Conventional Commits](https://www.conventionalcommits.org/)
- [Python Semantic Release](https://python-semantic-release.readthedocs.io/)
- [Keep a Changelog](https://keepachangelog.com/es-ES/1.0.0/)

## ✅ Checklist de Release

Antes de cada release importante:

- [ ] Todos los tests pasan
- [ ] Documentación actualizada
- [ ] Ejemplos funcionan correctamente
- [ ] BREAKING CHANGES documentados (si aplica)
- [ ] Guía de migración incluida (si aplica)
- [ ] Commits siguen conventional commits
- [ ] CI/CD pasa correctamente
