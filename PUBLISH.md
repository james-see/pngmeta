# Publishing pngmeta to PyPI

## Pre-publish Checklist

- [ ] Update version in `pyproject.toml`
- [ ] Update `CHANGELOG.md` (if you create one)
- [ ] Update `README.md` with any new features
- [ ] Run tests: `pytest`
- [ ] Format code: `black pngmeta tests examples`
- [ ] Lint code: `ruff check pngmeta tests examples`
- [ ] Update author info in `pyproject.toml`
- [ ] Update GitHub URL in `pyproject.toml`

## Build System

This project uses **hatchling** as the build backend (PEP 517 compliant). You can publish using any modern Python publishing tool.

## Publishing Options

Choose your preferred method:

### Option 1: uv publish (Recommended - Integrated)

Most seamless with your uv workflow:

```bash
# Build
uv build

# Publish to TestPyPI
uv publish --publish-url https://test.pypi.org/legacy/

# Publish to PyPI
uv publish
```

**Note**: The `/legacy/` path is PyPI's standard upload endpoint name (not actually legacy).

### Option 2: hatch publish (Native to build backend)

```bash
# Install hatch
uv pip install hatch

# Build and publish together
hatch publish

# Or step by step
hatch build
hatch publish

# For TestPyPI
hatch publish -r test
```

Configure repositories in `~/.pypirc` if using hatch:
```ini
[distutils]
index-servers =
    pypi
    test

[pypi]
username = __token__
password = pypi-YOUR-TOKEN

[test]
repository = https://test.pypi.org/legacy/
username = __token__
password = pypi-YOUR-TESTPYPI-TOKEN
```

### Option 3: twine (Traditional standard)

```bash
# Install twine
uv pip install twine

# Build
uv build

# Upload to TestPyPI
twine upload --repository testpypi dist/*

# Upload to PyPI
twine upload dist/*
```

## First Time Setup

### For PyPI API Tokens

1. Create a PyPI account at https://pypi.org/account/register/
2. Create API token at https://pypi.org/manage/account/token/
3. Configure credentials:

**For uv/twine** (~/.pypirc):
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

**For hatch** (uses same ~/.pypirc or environment variables):
```bash
export HATCH_INDEX_USER="__token__"
export HATCH_INDEX_AUTH="pypi-YOUR-TOKEN-HERE"
```

## Complete Publishing Workflow

```bash
# 1. Clean and test
rm -rf dist/ build/ *.egg-info
pytest
black pngmeta tests examples
ruff check pngmeta tests examples

# 2. Build
uv build

# 3. Check the distribution
ls -lh dist/
# Should see: pngmeta-X.Y.Z-py3-none-any.whl and pngmeta-X.Y.Z.tar.gz

# 4. Test on TestPyPI (choose one method)
uv publish --publish-url https://test.pypi.org/legacy/
# OR
hatch publish -r test
# OR
twine upload --repository testpypi dist/*

# 5. Test installation from TestPyPI
uv venv test-env
source test-env/bin/activate
uv pip install --index-url https://test.pypi.org/simple/ pngmeta
python -c "from pngmeta import PngMeta; print('Success!')"
deactivate
rm -rf test-env

# 6. Publish to PyPI (choose one method)
uv publish
# OR
hatch publish
# OR
twine upload dist/*
```

## After Publishing

1. Tag the release:
   ```bash
   git tag -a v0.1.0 -m "Release version 0.1.0"
   git push origin v0.1.0
   ```

2. Create GitHub release with notes

3. Verify on PyPI:
   - https://pypi.org/project/pngmeta/

4. Test installation:
   ```bash
   uv pip install pngmeta
   ```

## Version Bumping

Update version in `pyproject.toml`:
```toml
[project]
version = "0.2.0"  # Update this
```

Or use `hatch version`:
```bash
hatch version patch  # 0.1.0 -> 0.1.1
hatch version minor  # 0.1.0 -> 0.2.0
hatch version major  # 0.1.0 -> 1.0.0
```

## Why This Setup is Modern

✅ **PEP 517/518 compliant** - Uses `pyproject.toml` only  
✅ **hatchling** - Modern, fast build backend  
✅ **Zero setup.py** - No legacy setup files  
✅ **Declarative metadata** - Everything in pyproject.toml  
✅ **Standards-based** - Works with any PEP 517 tool

All three publishing methods (uv, hatch, twine) use the same modern PyPI upload API.