# pngmeta

A Python library for reading and writing PNG metadata, similar to [iptcinfo3](https://github.com/james-see/iptcinfo3) for JPEG files.

[![PyPI version](https://img.shields.io/pypi/v/pngmeta?style=for-the-badge)](https://pypi.org/project/pngmeta/)
[![GitHub stars](https://img.shields.io/github/stars/yourusername/pngmeta?style=for-the-badge)](https://github.com/yourusername/pngmeta)
[![Downloads](https://img.shields.io/pypi/dm/pngmeta?style=for-the-badge)](https://pypi.org/project/pngmeta/)
[![License](https://img.shields.io/badge/license-Unlicense-blue?style=for-the-badge)](LICENSE)

📖 **[View Full Documentation Site](https://yourusername.github.io/pngmeta/)** - Complete guide with live examples and API reference

---

Ever wish you could add information to your PNG images like a caption, author, copyright, and keywords? You already can! PNG files support metadata through text chunks (tEXt, iTXt, zTXt) and XMP. This module makes it easy to read and write that metadata in your Python programs.

## Installation

Install from PyPI:

```bash
pip install pngmeta
```

Or with `uv`:

```bash
uv pip install pngmeta
```

## Requirements

- Python 3.8 or higher
- No external dependencies required

## Usage

```python
from pngmeta import PngMeta
```

**Create new info object**
```python
meta = PngMeta('photo.png')
```

**Access metadata**
```python
# Get specific attributes
title = meta['Title']
author = meta['Author']
copyright_text = meta.get('Copyright')
```

**Modify metadata**
```python
# Add/change attributes
meta['Title'] = 'Sunset Over Mountains'
meta['Author'] = 'Jane Photographer'
meta['Copyright'] = '© 2025 Jane Photographer. All rights reserved.'
meta['Description'] = 'A stunning sunset over the mountains'
```

**Common metadata fields**
```python
meta['Creation Time'] = '2025-10-05T12:00:00'
meta['Software'] = 'pngmeta 0.1.0'
meta['Comment'] = 'What a beautiful day!'
```

**Work with XMP metadata**
```python
# Get XMP
xmp = meta.get_xmp()

# Set XMP
meta.set_xmp('<?xml version="1.0"?><x:xmpmeta>...</x:xmpmeta>')
```

**Check if metadata exists**
```python
if 'Author' in meta:
    print(f"Photo by {meta['Author']}")
```

**Iterate over all metadata**
```python
for key, value in meta.items():
    print(f"{key}: {value}")
```

**Save changes**
```python
# Save back to the same file
meta.save()

# Or save to a new file
meta.save('photo_with_metadata.png')
```

**Create object for file that may not have metadata**
```python
# Reads existing file, ready to add metadata
meta = PngMeta('new_photo.png')
meta['Title'] = 'My First Metadata'
meta.save()
```

## Complete Example

```python
from pngmeta import PngMeta

# Open an image
meta = PngMeta('photo.png')

# Add comprehensive metadata
meta['Title'] = 'Golden Gate Bridge at Sunset'
meta['Author'] = 'Jane Photographer'
meta['Copyright'] = '© 2025 Jane Photographer. All rights reserved.'
meta['Description'] = 'A stunning view of the Golden Gate Bridge during golden hour'
meta['Creation Time'] = '2025-10-05T18:30:00'
meta['Software'] = 'pngmeta 0.1.0'
meta['Comment'] = 'Shot with telephoto lens'

# Save the changes
meta.save()

# Read it back to verify
meta2 = PngMeta('photo.png')
print(f"Title: {meta2['Title']}")
print(f"Author: {meta2['Author']}")
```

## Common PNG Metadata Fields

| Field | Description | Example |
|-------|-------------|---------|
| `Title` | Short title or caption | "Golden Gate Bridge" |
| `Author` | Image creator | "Jane Photographer" |
| `Description` | Longer description | "A stunning sunset view..." |
| `Copyright` | Copyright notice | "© 2025 Jane Photographer" |
| `Creation Time` | When image was created | "2025-10-05T18:30:00" |
| `Software` | Software used | "pngmeta 0.1.0" |
| `Comment` | Miscellaneous comment | "Shot with telephoto lens" |
| `XML:com.adobe.xmp` | XMP metadata | (use `set_xmp()` method) |

## PNG Metadata Background

PNG files store metadata in "ancillary chunks":
- **tEXt** - Latin-1 text (uncompressed)
- **iTXt** - UTF-8 text (optionally compressed), used for XMP
- **zTXt** - Compressed Latin-1 text

Unlike JPEG, PNG doesn't natively use IPTC, but XMP can be embedded in iTXt chunks for cross-format compatibility.

## Examples

### Interactive Demo

Run the comprehensive demo to see all features in action with colored output:

```bash
python examples/demo_all_operations.py
```

This demo shows:
- Reading existing metadata
- Adding/modifying fields
- Working with XMP
- Dictionary operations
- Saving and verifying
- Complete colored reporting

### Basic Usage Script

See `examples/basic_usage.py` for additional examples including:
- Reading metadata from files
- Batch operations
- Copying metadata between images
- XMP handling

## Development

```bash
# Clone the repository
git clone https://github.com/yourusername/pngmeta.git
cd pngmeta

# Install with uv
uv venv
source .venv/bin/activate  # or `.venv\Scripts\activate` on Windows
uv pip install -e ".[dev]"

# Run tests
pytest

# Format code
black pngmeta tests

# Run the demo
python examples/demo_all_operations.py
```

## License

This is free and unencumbered software released into the public domain (Unlicense).

## API Compatibility with iptcinfo3

If you're familiar with [iptcinfo3](https://github.com/james-see/iptcinfo3), pngmeta follows a similar pattern:

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

Both use dictionary-style access and similar save patterns for a consistent experience.

## See Also

- [iptcinfo3](https://github.com/james-see/iptcinfo3) - IPTC metadata for JPEG files (inspiration for this library)
- [PNG Specification](http://www.libpng.org/pub/png/spec/1.2/PNG-Contents.html) - Technical details on PNG format
- [Exiv2 PNG Metadata](https://exiv2.org/metadata.html) - How other tools handle PNG metadata
