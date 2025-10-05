# Makefile for pngmeta

.PHONY: help install test lint format clean build publish release

help:
	@echo "pngmeta - Development Commands"
	@echo ""
	@echo "Setup:"
	@echo "  make install       Install package with dev dependencies"
	@echo ""
	@echo "Development:"
	@echo "  make test          Run tests"
	@echo "  make lint          Check code with ruff"
	@echo "  make format        Format code with black"
	@echo "  make demo          Run the demo script"
	@echo ""
	@echo "Release:"
	@echo "  make version-patch Bump patch version (0.1.0 → 0.1.1)"
	@echo "  make version-minor Bump minor version (0.1.0 → 0.2.0)"
	@echo "  make version-major Bump major version (0.1.0 → 1.0.0)"
	@echo "  make build         Build distribution packages"
	@echo "  make publish-test  Publish to TestPyPI"
	@echo "  make publish       Publish to PyPI"
	@echo ""
	@echo "Utilities:"
	@echo "  make clean         Remove build artifacts"
	@echo "  make docs          Preview documentation site"

install:
	uv pip install -e ".[dev,publish]"

test:
	pytest -v

lint:
	ruff check pngmeta tests examples

format:
	black pngmeta tests examples

demo:
	python examples/demo_all_operations.py

version-patch:
	hatch version patch
	@echo "New version: $$(hatch version)"

version-minor:
	hatch version minor
	@echo "New version: $$(hatch version)"

version-major:
	hatch version major
	@echo "New version: $$(hatch version)"

clean:
	rm -rf dist/
	rm -rf build/
	rm -rf *.egg-info
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

build: clean
	uv build
	@echo "Built packages:"
	@ls -lh dist/

publish-test: build
	@echo "Publishing to TestPyPI..."
	uv publish --publish-url https://test.pypi.org/legacy/

publish: build
	@echo "Publishing to PyPI..."
	@echo "Press Ctrl+C to cancel, or Enter to continue..."
	@read confirm
	uv publish

release: test lint
	@echo "Release checklist:"
	@echo "1. Tests passed ✓"
	@echo "2. Code linted ✓"
	@echo ""
	@echo "Next steps:"
	@echo "  make version-patch  (or minor/major)"
	@echo "  make build"
	@echo "  make publish-test   (optional)"
	@echo "  make publish"
	@echo ""
	@echo "Then commit and tag:"
	@echo "  git add ."
	@echo "  git commit -m 'Release vX.X.X'"
	@echo "  git tag -a vX.X.X -m 'Release X.X.X'"
	@echo "  git push origin main --tags"

docs:
	@echo "Starting documentation server..."
	@echo "Visit: http://localhost:8000"
	cd docs && python3 -m http.server 8000
