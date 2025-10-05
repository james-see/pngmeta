#!/usr/bin/env python3
"""
Basic usage examples for pngmeta.

For a comprehensive demonstration with colored output showing all features,
run: python examples/demo_all_operations.py
"""

import sys
from pathlib import Path

# Add parent directory to path for development
sys.path.insert(0, str(Path(__file__).parent.parent))

from pngmeta import PngMeta


# Example 1: Read metadata from a PNG
def read_metadata(filename):
    """Read and display all metadata from a PNG file."""
    meta = PngMeta(filename)

    print(f"Metadata in {filename}:")
    print(f"  Total keys: {len(list(meta.keys()))}")
    print()

    for key, value in meta.items():
        print(f"  {key}: {value}")

    # Check for XMP
    xmp = meta.get_xmp()
    if xmp:
        print(f"\n  XMP present: {len(xmp)} bytes")


# Example 2: Write metadata to a PNG
def write_metadata(input_file, output_file):
    """Add metadata to a PNG file."""
    meta = PngMeta(input_file)

    # Set standard fields
    meta.set("Title", "Beautiful Landscape")
    meta.set("Author", "Jane Photographer")
    meta.set("Copyright", "Copyright 2025 Jane Photographer. All rights reserved.")
    meta.set("Description", "A stunning sunset over the mountains")
    meta.set("Creation Time", "2025-10-05T12:00:00")
    meta.set("Software", "pngmeta 0.1.0")

    # Save changes
    meta.save(output_file)
    print(f"Metadata written to {output_file}")


# Example 3: Work with XMP
def add_xmp_metadata(filename):
    """Add XMP metadata to a PNG file."""
    meta = PngMeta(filename)

    xmp_data = """<?xml version="1.0" encoding="UTF-8"?>
<x:xmpmeta xmlns:x="adobe:ns:meta/">
  <rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
    <rdf:Description rdf:about=""
        xmlns:dc="http://purl.org/dc/elements/1.1/"
        xmlns:xmp="http://ns.adobe.com/xap/1.0/">
      <dc:title>
        <rdf:Alt>
          <rdf:li xml:lang="x-default">Sample Title</rdf:li>
        </rdf:Alt>
      </dc:title>
      <dc:creator>
        <rdf:Seq>
          <rdf:li>Sample Creator</rdf:li>
        </rdf:Seq>
      </dc:creator>
      <xmp:Rating>5</xmp:Rating>
    </rdf:Description>
  </rdf:RDF>
</x:xmpmeta>"""

    meta.set_xmp(xmp_data)
    meta.save()
    print(f"XMP metadata added to {filename}")


# Example 4: Copy metadata between files
def copy_metadata(source_file, dest_file):
    """Copy all metadata from one PNG to another."""
    source = PngMeta(source_file)
    dest = PngMeta(dest_file)

    # Copy all metadata
    for key, value in source.items():
        dest.set(key, value)

    dest.save()
    print(f"Copied metadata from {source_file} to {dest_file}")


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python basic_usage.py <image.png>")
        print("\nThis will read and display metadata from the PNG file.")
        sys.exit(1)

    filename = sys.argv[1]
    read_metadata(filename)
