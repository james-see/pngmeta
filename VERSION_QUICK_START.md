# Quick Version Update Guide

Version is now managed dynamically by hatch!

## To Release a New Version

### Example: Bug fix release (0.1.0 → 0.1.1)

```bash
# 1. Bump version
make version-patch

# 2. Commit
git add .
git commit -m "Bump version to 0.1.1"

# 3. Build and publish
make build
make publish

# 4. Tag and push
git tag -a v0.1.1 -m "Release v0.1.1"
git push origin main --tags
```

## Version Commands

```bash
make version-patch    # 0.1.0 → 0.1.1 (bug fixes)
make version-minor    # 0.1.0 → 0.2.0 (new features)
make version-major    # 0.1.0 → 1.0.0 (breaking changes)
```

## Where Version is Stored

The version is in `pngmeta/__init__.py`:
```python
__version__ = "0.1.0"
```

Hatch automatically updates this file when you run version commands.

## Manual Version Update

If you prefer to update manually, just edit `pngmeta/__init__.py`:
```python
__version__ = "0.2.0"
```

Then build and publish normally.

## Check Current Version

```bash
hatch version
# or
make help
```

## Complete Release Example

```bash
# Make your changes...
git add .
git commit -m "Fix metadata parsing bug"

# Bump version
make version-patch  # Now 0.1.1

# Test
make test
make lint
make demo

# Build and publish
make build
make publish

# Git tag
git tag -a v0.1.1 -m "Release v0.1.1 - Fix metadata parsing"
git push origin main --tags

# Create GitHub release (optional)
open https://github.com/james-see/pngmeta/releases/new
```

Done! ✅
