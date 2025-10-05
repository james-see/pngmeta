# pngmeta Examples

This directory contains example scripts demonstrating how to use pngmeta.

## Files

### demo_all_operations.py ⭐

**Comprehensive interactive demo with colored output**

Run this first to see all pngmeta features in action:

```bash
python examples/demo_all_operations.py
```

Features demonstrated:
- ✅ Reading existing metadata
- ✅ Adding/modifying metadata fields
- ✅ Working with XMP data
- ✅ Dictionary-style operations (get, set, contains, iterate)
- ✅ Saving to new files
- ✅ Verifying saved metadata
- ✅ Beautiful colored terminal output
- ✅ Step-by-step explanations
- ✅ File size comparison

**Output includes:**
- Color-coded success/warning/error messages
- Formatted metadata tables
- Progress through 9 demonstration steps
- Verification of all operations
- Summary and next steps

### basic_usage.py

Collection of simple functions showing common operations:

- `read_metadata(filename)` - Display all metadata
- `write_metadata(input, output)` - Add standard fields
- `add_xmp_metadata(filename)` - Add XMP data
- `copy_metadata(source, dest)` - Copy between files

Run standalone:
```bash
python examples/basic_usage.py image.png
```

Or import functions:
```python
from examples.basic_usage import read_metadata, write_metadata
```

### test-image.png

Sample PNG image for testing. The demo script uses this image to demonstrate all operations.

## Quick Start

1. **Run the comprehensive demo:**
   ```bash
   python examples/demo_all_operations.py
   ```

2. **Try basic operations:**
   ```bash
   python examples/basic_usage.py test-image.png
   ```

3. **Write your own:**
   ```python
   from pngmeta import PngMeta
   
   meta = PngMeta('your-image.png')
   meta['Title'] = 'My Photo'
   meta.save()
   ```

## What to Try

After running the demos:

1. **Inspect the output:**
   ```bash
   # View the image
   open examples/test-image-with-metadata.png
   
   # Inspect with ImageMagick
   identify -verbose examples/test-image-with-metadata.png
   ```

2. **Modify the demo:**
   - Change the metadata being added
   - Add your own custom fields
   - Try different XMP structures

3. **Test with your images:**
   - Copy your PNG to `examples/my-image.png`
   - Modify the scripts to use your image
   - Experiment with different metadata

## Tips

- PNG text chunks support any keyword you want
- Common keywords: Title, Author, Description, Copyright, Comment, Software
- XMP provides structured metadata (use `set_xmp()`)
- Metadata typically adds 100-2000 bytes to file size
- Original files are never modified unless you save over them

## Troubleshooting

**"File not found" error?**
- Make sure you're in the project root directory
- Use full paths: `python examples/demo_all_operations.py`

**Import errors?**
- Install pngmeta: `pip install -e .`
- Or add to path: `export PYTHONPATH=.`

**Colors not showing?**
- Some terminals don't support ANSI colors
- Output still works, just without colors
- Try a modern terminal (iTerm2, Windows Terminal, etc.)
