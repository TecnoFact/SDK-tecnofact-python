.PHONY: install install-dev test coverage lint format clean build upload check verify docker-build docker-test docker-dev help

help:
	@echo "Comandos disponibles:"
	@echo "  make install       - Instalar el paquete"
	@echo "  make install-dev   - Instalar dependencias de desarrollo"
	@echo "  make test          - Ejecutar tests"
	@echo "  make coverage      - Ejecutar tests con cobertura"
	@echo "  make lint          - Ejecutar linters (flake8, mypy)"
	@echo "  make format        - Formatear código (black, isort)"
	@echo "  make check         - Verificar el paquete antes de publicar"
	@echo "  make verify        - Verificar todo (lint + test + check)"
	@echo "  make clean         - Limpiar archivos generados"
	@echo "  make build         - Construir el paquete"
	@echo "  make upload        - Subir a PyPI"
	@echo "  make upload-test   - Subir a TestPyPI (prueba)"
	@echo "  make docker-build  - Construir imagen Docker"
	@echo "  make docker-test   - Ejecutar tests en Docker"
	@echo "  make docker-dev    - Entorno de desarrollo en Docker"

install:
	pip install -e .

install-dev:
	pip install -r requirements-dev.txt
	pip install -e .

test:
	pytest

coverage:
	pytest --cov=tecnofact --cov-report=html --cov-report=term-missing

lint:
	flake8 src/tecnofact tests
	mypy src/tecnofact

format:
	black src/tecnofact tests examples
	isort src/tecnofact tests examples

clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info
	rm -rf .pytest_cache
	rm -rf .coverage
	rm -rf htmlcov/
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

check:
	@echo "Verificando MANIFEST.in..."
	check-manifest
	@echo "Verificando metadata del paquete..."
	python -m build --sdist --wheel
	twine check dist/*

verify: lint test check
	@echo "✓ Todas las verificaciones pasaron"

build: clean
	@echo "Construyendo el paquete..."
	python -m build

upload: verify build
	@echo "Subiendo a PyPI..."
	twine upload dist/*

upload-test: verify build
	@echo "Subiendo a TestPyPI..."
	twine upload --repository testpypi dist/*

docker-build:
	docker-compose build

docker-test:
	docker-compose run --rm sdk

docker-dev:
	docker-compose run --rm dev
