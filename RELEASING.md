# Release Guide for pngmeta

Quick reference for publishing new versions to PyPI.

## Quick Release (3 Steps)

```bash
# 1. Update version
hatch version patch  # 0.1.0 → 0.1.1

# 2. Build
uv build

# 3. Publish
uv publish
```

## Detailed Steps

### 1. Update Version Number

Choose your version bump:

```bash
# Patch release (0.1.0 → 0.1.1) - Bug fixes
hatch version patch

# Minor release (0.1.0 → 0.2.0) - New features
hatch version minor

# Major release (0.1.0 → 1.0.0) - Breaking changes
hatch version major

# Check current version
hatch version
```

Or manually edit `pyproject.toml`:
```toml
[project]
version = "0.1.1"  # Update this line
```

### 2. Update Changelog (Optional)

Create/update `CHANGELOG.md`:
```markdown
## [0.1.1] - 2025-10-XX

### Added
- New feature description

### Fixed
- Bug fix description

### Changed
- Change description
```

### 3. Test Everything

```bash
# Run tests
pytest

# Format and lint
black pngmeta tests examples
ruff check pngmeta tests examples

# Test demo
python examples/demo_all_operations.py
```

### 4. Commit Changes

```bash
git add .
git commit -m "Release v0.1.1"
git tag -a v0.1.1 -m "Release version 0.1.1"
git push origin main
git push origin v0.1.1
```

### 5. Build Package

```bash
# Clean old builds
rm -rf dist/

# Build new package
uv build
```

This creates:
- `dist/pngmeta-0.1.1-py3-none-any.whl`
- `dist/pngmeta-0.1.1.tar.gz`

### 6. Test on TestPyPI (Optional but Recommended)

```bash
# Upload to TestPyPI
uv publish --publish-url https://test.pypi.org/legacy/

# Test installation
pip install --index-url https://test.pypi.org/simple/ pngmeta==0.1.1

# Try it
python -c "from pngmeta import PngMeta; print('Works!')"
```

### 7. Publish to PyPI

```bash
uv publish
```

That's it! Your new version is live.

### 8. Create GitHub Release

1. Go to: https://github.com/james-see/pngmeta/releases/new
2. Tag: `v0.1.1`
3. Title: `v0.1.1`
4. Description: Copy from CHANGELOG.md
5. Click "Publish release"

## Version Numbering Guide

Use [Semantic Versioning](https://semver.org/):

- **MAJOR** (1.0.0): Breaking changes, incompatible API changes
- **MINOR** (0.2.0): New features, backward compatible
- **PATCH** (0.1.1): Bug fixes, backward compatible

Examples:
```bash
# Bug fix: 0.1.0 → 0.1.1
hatch version patch

# New feature: 0.1.1 → 0.2.0
hatch version minor

# Breaking change: 0.2.0 → 1.0.0
hatch version major
```

## Complete Release Checklist

Before releasing:
- [ ] All tests pass (`pytest`)
- [ ] Code formatted (`black pngmeta tests examples`)
- [ ] Linting clean (`ruff check pngmeta tests examples`)
- [ ] Version bumped (`hatch version X`)
- [ ] CHANGELOG.md updated
- [ ] README.md updated (if needed)
- [ ] Examples tested
- [ ] Committed and tagged

After releasing:
- [ ] Verify on PyPI: https://pypi.org/project/pngmeta/
- [ ] Test install: `pip install pngmeta==X.X.X`
- [ ] Create GitHub release
- [ ] Update documentation site (if needed)
- [ ] Wait 2-6 hours for badges to update

## Troubleshooting

### "File already exists"

You're trying to upload a version that already exists on PyPI.

**Fix**: Bump the version number and rebuild.

### Authentication failed

**Fix**: Ensure your `~/.pypirc` has correct tokens:
```ini
[pypi]
username = __token__
password = pypi-YOUR-TOKEN-HERE
```

### Wrong package contents

**Fix**: Check what's in the wheel:
```bash
unzip -l dist/pngmeta-0.1.1-py3-none-any.whl
```

## Quick Commands Reference

```bash
# Version management
hatch version          # Show current
hatch version patch    # Bump patch
hatch version minor    # Bump minor  
hatch version major    # Bump major

# Build
rm -rf dist/
uv build

# Publish
uv publish --publish-url https://test.pypi.org/legacy/  # Test
uv publish                                              # Production

# Git
git tag -a v0.1.1 -m "Release 0.1.1"
git push origin main
git push origin v0.1.1

# Verify
pip install --upgrade pngmeta
python -c "from pngmeta import PngMeta; print(PngMeta.__module__)"
```

## Automated Release (Future)

Consider setting up GitHub Actions for automated releases:
1. Push a tag
2. Actions builds and tests
3. Publishes to PyPI automatically
4. Creates GitHub release

See `.github/workflows/release.yml` (to be created).
