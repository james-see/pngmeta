# Quick Reference - Publishing pngmeta

## TL;DR - Your Setup is Modern ✅

- **Build backend**: `hatchling` (modern, PEP 517)
- **Publishing**: Choose any modern tool
- **No setup.py**: Pure `pyproject.toml` (best practice)

The `/legacy/` in PyPI URLs is just endpoint naming - **not actually legacy**.

## Quick Commands

### Option A: uv (Fastest)
```bash
uv build
uv publish --publish-url https://test.pypi.org/legacy/  # Test
uv publish  # Production
```

### Option B: hatch (Integrated)
```bash
hatch version patch   # Bump version
hatch publish -r test # Test
hatch publish         # Production
```

### Option C: twine (Traditional)
```bash
uv build
twine upload --repository testpypi dist/*  # Test
twine upload dist/*                         # Production
```

## Which to Use?

| Choose | If you... |
|--------|-----------|
| **uv** | Want fastest, most integrated with uv workflow |
| **hatch** | Want version management + native build backend integration |
| **twine** | Want PyPA standard, most documentation available |

All are modern and work identically with your `pyproject.toml`!

## Common Tasks

```bash
# Install for development
uv pip install -e ".[dev,publish]"

# Run tests
pytest

# Format code
black pngmeta tests examples

# Lint
ruff check pngmeta tests examples

# Build package
uv build

# Check package before upload
twine check dist/*

# Bump version (with hatch)
hatch version patch  # 0.1.0 → 0.1.1

# View current version
hatch version
```

## Configuration File

Create `~/.pypirc`:
```ini
[distutils]
index-servers =
    pypi
    testpypi

[pypi]
username = __token__
password = pypi-YOUR-TOKEN-HERE

[testpypi]
repository = https://test.pypi.org/legacy/
username = __token__
password = pypi-YOUR-TESTPYPI-TOKEN-HERE
```

Then: `chmod 600 ~/.pypirc`

## Complete Publish Flow

```bash
# 1. Test and clean
pytest && black pngmeta tests && ruff check pngmeta
rm -rf dist/

# 2. Bump version (optional, with hatch)
hatch version patch

# 3. Build
uv build

# 4. Test on TestPyPI
uv publish --publish-url https://test.pypi.org/legacy/

# 5. Verify
pip install --index-url https://test.pypi.org/simple/ pngmeta

# 6. Publish to PyPI
uv publish

# 7. Tag release
git tag -a v0.1.0 -m "Release 0.1.0"
git push origin v0.1.0
```

See `PUBLISH.md` and `BUILD_SYSTEM.md` for details.
