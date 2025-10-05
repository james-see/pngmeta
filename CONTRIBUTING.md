# Contributing to pngmeta

## Development Setup with uv

1. Install [uv](https://github.com/astral-sh/uv) if you haven't already:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

2. Clone the repository:
```bash
git clone https://github.com/yourusername/pngmeta.git
cd pngmeta
```

3. Create a virtual environment and install dependencies:
```bash
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
uv pip install -e ".[dev]"
```

## Running Tests

```bash
pytest
```

With coverage:
```bash
pytest --cov=pngmeta --cov-report=html
```

## Code Quality

Format code with black:
```bash
black pngmeta tests examples
```

Lint with ruff:
```bash
ruff check pngmeta tests examples
```

## Building the Package

Using uv (recommended):
```bash
uv build
```

Or using hatch:
```bash
uv pip install hatch
hatch build
```

This creates wheel and source distributions in `dist/`.

## Publishing to PyPI

This project uses **hatchling** as the build backend (modern, PEP 517 compliant).

### Method 1: uv publish (Recommended)
```bash
uv build
uv publish --publish-url https://test.pypi.org/legacy/  # Test first
uv publish  # Then real PyPI
```

### Method 2: hatch publish
```bash
uv pip install hatch
hatch publish -r test  # TestPyPI
hatch publish          # PyPI
```

### Method 3: twine
```bash
uv pip install twine
uv build
twine upload --repository testpypi dist/*  # Test
twine upload dist/*                         # PyPI
```

See `PUBLISH.md` for detailed instructions and credential setup.

## Project Structure

```
pngmeta/
├── pngmeta/           # Main package
│   ├── __init__.py    # Package exports
│   ├── pngmeta.py     # Core PngMeta class
│   └── exceptions.py  # Exception classes
├── tests/             # Test suite
├── examples/          # Usage examples
├── pyproject.toml     # Package configuration
├── README.md          # User documentation
└── LICENSE            # Unlicense
```

## Guidelines

- Keep the API simple and similar to iptcinfo3
- Maintain Python 3.8+ compatibility
- Add tests for new features
- Update README.md with examples
- Follow PEP 8 (enforced by black and ruff)
