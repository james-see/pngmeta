# Build System Architecture

## Why This Setup is Modern (Not Legacy)

### ✅ Standards-Based (PEP 517/518)
```toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"
```
- **No setup.py** - Pure declarative metadata
- **PEP 517** compliant - Works with any modern tool
- **PEP 518** compliant - Build requirements in pyproject.toml

### ✅ Modern Build Backend: hatchling

**hatchling** is Hatch's build backend, chosen for:
- Fast builds (written in pure Python)
- Zero configuration needed for simple packages
- Maintained by PyPA member (Python Packaging Authority)
- Used by major projects (pytest, black, ruff, etc.)

Alternative modern backends you could use:
- `setuptools>=61` with PEP 621 metadata
- `flit-core` - Simpler, for pure Python
- `pdm-backend` - Another modern option

### ✅ Modern Publishing Tools

All three publishing options are **modern and standards-compliant**:

| Tool | Status | Notes |
|------|--------|-------|
| `uv publish` | Modern (2024+) | Integrated with uv's fast toolchain |
| `hatch publish` | Modern (2022+) | Native to build backend |
| `twine` | Standard (2013+) | PyPA-official, battle-tested |

**Why `/legacy/` in URL?** It's just PyPI's endpoint name. The upload API itself is modern and current.

## Build System Comparison

### This Project (Modern)
```toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "pngmeta"
version = "0.1.0"
# ... all metadata declarative
```

✅ PEP 517/518 compliant  
✅ No setup.py needed  
✅ Works with any tool (pip, uv, hatch, poetry, pdm)  
✅ Fast, reproducible builds

### Legacy Approach (Avoid)
```python
# setup.py
from setuptools import setup

setup(
    name="pngmeta",
    version="0.1.0",
    # ... imperative code
)
```

❌ Executes Python code during build  
❌ Less reproducible  
❌ Harder to parse/validate  
❌ Security concerns (arbitrary code execution)

## Publishing Architecture

```
┌─────────────────┐
│  pyproject.toml │  ← Single source of truth
└────────┬────────┘
         │
    ┌────▼────┐
    │ hatchling│  ← Build backend (PEP 517)
    └────┬────┘
         │
    ┌────▼─────────────┐
    │  dist/           │  ← Build artifacts
    │  ├── *.whl       │  ← Wheel (binary distribution)
    │  └── *.tar.gz    │  ← Sdist (source distribution)
    └────┬─────────────┘
         │
    ┌────▼──────────────┐
    │ Publishing Tool   │  ← Choose any:
    │ • uv publish      │     - uv publish (fast, integrated)
    │ • hatch publish   │     - hatch publish (native)
    │ • twine          │     - twine (standard)
    └────┬──────────────┘
         │
    ┌────▼────┐
    │  PyPI   │  ← Standard upload API
    └─────────┘
```

## Tool Feature Matrix

| Feature | uv | hatch | twine |
|---------|----|----|-------|
| Build packages | ✅ | ✅ | ❌ |
| Upload to PyPI | ✅ | ✅ | ✅ |
| Version management | ❌ | ✅ | ❌ |
| Virtual envs | ✅ | ✅ | ❌ |
| Speed | ⚡️ Fastest | Fast | Fast |
| Integration | uv ecosystem | hatch ecosystem | Universal |

## Version Management

### Manual (Current)
Edit `pyproject.toml`:
```toml
version = "0.1.0"  # Change this
```

### Using hatch (Optional)
```bash
# Install hatch
uv pip install hatch

# Bump versions
hatch version patch  # 0.1.0 → 0.1.1
hatch version minor  # 0.1.0 → 0.2.0  
hatch version major  # 0.1.0 → 1.0.0

# Check current version
hatch version
```

Hatch automatically updates `pyproject.toml` for you.

## Recommended Workflow

### For uv users (Recommended)
```bash
uv venv
source .venv/bin/activate
uv pip install -e ".[dev]"
uv build
uv publish
```
**Why**: Fastest, most integrated with uv ecosystem

### For hatch users
```bash
hatch env create
hatch version patch
hatch build
hatch publish
```
**Why**: Native to build backend, includes version management

### For traditional users
```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
python -m build
twine upload dist/*
```
**Why**: Most widely documented, PyPA standard

## Migration from Legacy

If you had an old `setup.py` project:

```bash
# Old way
python setup.py sdist bdist_wheel
python setup.py upload

# New way (choose one)
uv build && uv publish
# OR
hatch build && hatch publish
# OR
python -m build && twine upload dist/*
```

## Summary

Your current setup is **fully modern**:
- ✅ PEP 517/518 compliant (pyproject.toml only)
- ✅ Modern build backend (hatchling)
- ✅ Modern publishing tools (uv/hatch/twine)
- ✅ Zero legacy files (no setup.py, setup.cfg, etc.)
- ✅ Works with all modern Python packaging tools

The `/legacy/` in PyPI URLs is just an endpoint name from historical reasons - the API itself is modern and current.
