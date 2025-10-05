# pngmeta Project Summary

## Overview

A PyPI-ready Python library for reading and writing PNG metadata, inspired by `iptcinfo3` for JPEG files.

## Features Implemented

✅ **Core Functionality**
- Read PNG text chunks (tEXt, iTXt, zTXt)
- Write metadata to PNG files
- XMP support via iTXt chunks
- Dictionary-style API
- Zero dependencies (pure Python)

✅ **Project Structure**
- Modern `pyproject.toml` using hatchling build backend
- Configured for `uv` package manager
- Comprehensive test suite (8 tests, all passing)
- Example scripts
- Complete documentation

✅ **Code Quality**
- Type hints throughout
- Black formatting configured
- Ruff linting configured
- pytest test framework
- Python 3.8+ compatibility

## Project Files

```
pngmeta/
├── pngmeta/                 # Main package
│   ├── __init__.py          # Package exports
│   ├── pngmeta.py           # Core PngMeta class (~350 lines)
│   └── exceptions.py        # Exception classes
├── tests/                   # Test suite
│   ├── __init__.py
│   └── test_pngmeta.py      # 8 comprehensive tests
├── examples/                # Usage examples
│   └── basic_usage.py       # Real-world examples
├── dist/                    # Built packages (ready for PyPI)
│   ├── pngmeta-0.1.0-py3-none-any.whl
│   └── pngmeta-0.1.0.tar.gz
├── pyproject.toml           # Package configuration (uv-compatible)
├── README.md                # User documentation
├── QUICKSTART.md            # Quick reference
├── CONTRIBUTING.md          # Development guide
├── PUBLISH.md               # PyPI publishing guide
├── LICENSE                  # Unlicense (public domain)
├── .gitignore               # Git ignore rules
├── .python-version          # Python version (3.11)
└── MANIFEST.in              # Distribution manifest
```

## API Design

Simple, intuitive API modeled after `iptcinfo3`:

```python
from pngmeta import PngMeta

meta = PngMeta('image.png')
meta.set('Title', 'My Image')
meta.set('Author', 'John Doe')
meta.set_xmp('<xml>...</xml>')
meta.save()

# Dictionary-style access
meta['Copyright'] = '© 2025'
print(meta['Author'])
```

## Technical Implementation

**PNG Chunk Handling**
- Correctly reads/writes PNG chunk structure (length, type, data, CRC)
- Parses tEXt (Latin-1, uncompressed)
- Parses iTXt (UTF-8, optionally compressed)
- Parses zTXt (Latin-1, compressed)
- Generates proper CRC32 checksums

**Metadata Storage**
- Stores metadata in standard PNG text chunks
- XMP stored in iTXt with keyword `XML:com.adobe.xmp`
- Preserves non-text chunks (IHDR, IDAT, IEND, etc.)
- Properly inserts metadata chunks before IDAT

## Next Steps for PyPI Publishing

1. **Update Project URLs**
   - Set your GitHub repo URL in `pyproject.toml`
   - Update author name and email

2. **Test on TestPyPI**
   ```bash
   uv publish --publish-url https://test.pypi.org/legacy/
   ```

3. **Publish to PyPI**
   ```bash
   uv publish
   ```

See `PUBLISH.md` for detailed instructions.

## Testing

All tests pass:
```
8 passed in 0.01s
- test_invalid_file
- test_nonexistent_file
- test_read_empty_png
- test_write_and_read_metadata
- test_dictionary_interface
- test_save_to_new_file
- test_xmp_metadata
- test_repr
```

## Build Status

✅ Package builds successfully:
```
dist/pngmeta-0.1.0.tar.gz
dist/pngmeta-0.1.0-py3-none-any.whl
```

Ready for upload to PyPI!

## Development Commands

```bash
# Setup
uv venv
source .venv/bin/activate
uv pip install -e ".[dev]"

# Test
pytest

# Format & Lint
black pngmeta tests examples
ruff check pngmeta tests examples

# Build
uv build

# Publish
uv publish  # to PyPI
```

## Why pngmeta?

- **PNG Metadata Gap**: While `iptcinfo3` handles JPEG IPTC data well, PNG metadata needs different handling
- **Pure Python**: No dependencies, works everywhere
- **Standards-Compliant**: Follows PNG specification for text chunks
- **XMP Ready**: Supports modern XMP metadata for cross-format compatibility
- **Simple API**: Easy to learn if you know iptcinfo3

## License

Public domain (Unlicense) - use freely for any purpose.
