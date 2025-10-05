# pngmeta Quick Start

## What is pngmeta?

A Python library for reading and writing PNG metadata, modeled after `iptcinfo3`. Handles PNG text chunks (tEXt, iTXt, zTXt) and XMP metadata with zero dependencies.

## Installation

```bash
# With pip
pip install pngmeta

# With uv
uv pip install pngmeta
```

## 30-Second Tutorial

```python
from pngmeta import PngMeta

# Read metadata
meta = PngMeta('photo.png')
print(meta.get('Title'))
print(meta.get('Author'))

# Write metadata
meta.set('Title', 'Sunset Over Mountains')
meta.set('Author', 'Jane Doe')
meta.set('Copyright', '© 2025 Jane Doe')
meta.save()

# Dictionary-style access
meta['Description'] = 'Beautiful landscape'
if 'Author' in meta:
    print(f"By {meta['Author']}")

# XMP support
meta.set_xmp('<?xml version="1.0"?>...')
xmp = meta.get_xmp()
```

## Common Metadata Fields

- `Title` - Short title
- `Author` - Creator name
- `Description` - Detailed description
- `Copyright` - Copyright notice
- `Creation Time` - When created (ISO 8601)
- `Software` - Software used
- `Comment` - Additional comments
- `XML:com.adobe.xmp` - XMP metadata (use `set_xmp()`)

## Development Setup (uv)

```bash
# Clone and setup
git clone https://github.com/yourusername/pngmeta.git
cd pngmeta
uv venv
source .venv/bin/activate
uv pip install -e ".[dev]"

# Run tests
pytest

# Format and lint
black pngmeta tests examples
ruff check pngmeta tests examples

# Build
uv build
```

## Publishing to PyPI

```bash
# Test on TestPyPI first
uv build
uv publish --publish-url https://test.pypi.org/legacy/

# Then publish to PyPI
uv publish
```

See `PUBLISH.md` for detailed instructions.

## Examples

See `examples/basic_usage.py` for comprehensive examples including:
- Reading metadata
- Writing metadata
- XMP handling
- Copying metadata between files

## API Compatibility with iptcinfo3

Similar patterns for easy migration:

```python
# iptcinfo3 (for JPEG)
from iptcinfo3 import IPTCInfo
info = IPTCInfo('photo.jpg')
info['caption/abstract'] = 'My photo'
info.save()

# pngmeta (for PNG)
from pngmeta import PngMeta
meta = PngMeta('photo.png')
meta['Description'] = 'My photo'
meta.save()
```

## Support

- GitHub: https://github.com/yourusername/pngmeta
- Issues: https://github.com/yourusername/pngmeta/issues
- PyPI: https://pypi.org/project/pngmeta/
