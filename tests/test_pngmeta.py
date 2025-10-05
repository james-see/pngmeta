"""Tests for PngMeta class."""

import tempfile
from pathlib import Path

import pytest

from pngmeta import InvalidPngError, PngMeta


def create_minimal_png() -> bytes:
    """Create a minimal valid PNG file."""
    import struct
    import zlib

    # PNG signature
    png = b"\x89PNG\r\n\x1a\n"

    # IHDR chunk (1x1 grayscale image)
    width, height = 1, 1
    bit_depth = 8
    color_type = 0  # grayscale
    compression = 0
    filter_method = 0
    interlace = 0

    ihdr_data = struct.pack(
        ">IIBBBBB", width, height, bit_depth, color_type, compression, filter_method, interlace
    )
    ihdr_crc = zlib.crc32(b"IHDR" + ihdr_data) & 0xFFFFFFFF
    png += struct.pack(">I", len(ihdr_data)) + b"IHDR" + ihdr_data + struct.pack(">I", ihdr_crc)

    # IDAT chunk (minimal image data)
    idat_data = zlib.compress(b"\x00\x00")  # Filter method + pixel
    idat_crc = zlib.crc32(b"IDAT" + idat_data) & 0xFFFFFFFF
    png += struct.pack(">I", len(idat_data)) + b"IDAT" + idat_data + struct.pack(">I", idat_crc)

    # IEND chunk
    iend_crc = zlib.crc32(b"IEND") & 0xFFFFFFFF
    png += struct.pack(">I", 0) + b"IEND" + struct.pack(">I", iend_crc)

    return png


class TestPngMeta:
    """Test PngMeta functionality."""

    def test_invalid_file(self):
        """Test that non-PNG files raise InvalidPngError."""
        with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as f:
            f.write(b"not a png file")
            temp_path = f.name

        try:
            with pytest.raises(InvalidPngError):
                PngMeta(temp_path)
        finally:
            Path(temp_path).unlink()

    def test_nonexistent_file(self):
        """Test that missing files raise FileNotFoundError."""
        with pytest.raises(FileNotFoundError):
            PngMeta("nonexistent.png")

    def test_read_empty_png(self):
        """Test reading a PNG with no metadata."""
        png_data = create_minimal_png()

        with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as f:
            f.write(png_data)
            temp_path = f.name

        try:
            meta = PngMeta(temp_path)
            assert len(list(meta.keys())) == 0
            assert meta.get("Title") is None
            assert meta.get("Author", "default") == "default"
        finally:
            Path(temp_path).unlink()

    def test_write_and_read_metadata(self):
        """Test writing and reading metadata."""
        png_data = create_minimal_png()

        with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as f:
            f.write(png_data)
            temp_path = f.name

        try:
            # Write metadata
            meta = PngMeta(temp_path)
            meta.set("Title", "Test Image")
            meta.set("Author", "Test Author")
            meta.set("Copyright", "Copyright 2025")
            meta.save()

            # Read it back
            meta2 = PngMeta(temp_path)
            assert meta2.get("Title") == "Test Image"
            assert meta2.get("Author") == "Test Author"
            assert meta2.get("Copyright") == "Copyright 2025"
        finally:
            Path(temp_path).unlink()

    def test_dictionary_interface(self):
        """Test dictionary-style access."""
        png_data = create_minimal_png()

        with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as f:
            f.write(png_data)
            temp_path = f.name

        try:
            meta = PngMeta(temp_path)
            meta["Title"] = "Dict Test"
            meta.save()

            meta2 = PngMeta(temp_path)
            assert meta2["Title"] == "Dict Test"
            assert "Title" in meta2
            assert "Nonexistent" not in meta2
        finally:
            Path(temp_path).unlink()

    def test_save_to_new_file(self):
        """Test saving to a different file."""
        png_data = create_minimal_png()

        with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as f:
            f.write(png_data)
            temp_path1 = f.name

        with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as f:
            temp_path2 = f.name

        try:
            meta = PngMeta(temp_path1)
            meta.set("Title", "New File Test")
            meta.save(temp_path2)

            # Original file should not have metadata
            meta_orig = PngMeta(temp_path1)
            assert meta_orig.get("Title") is None

            # New file should have metadata
            meta_new = PngMeta(temp_path2)
            assert meta_new.get("Title") == "New File Test"
        finally:
            Path(temp_path1).unlink()
            Path(temp_path2).unlink(missing_ok=True)

    def test_xmp_metadata(self):
        """Test XMP metadata handling."""
        png_data = create_minimal_png()

        with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as f:
            f.write(png_data)
            temp_path = f.name

        try:
            xmp_data = '<?xml version="1.0"?><x:xmpmeta xmlns:x="adobe:ns:meta/"></x:xmpmeta>'

            meta = PngMeta(temp_path)
            meta.set_xmp(xmp_data)
            meta.save()

            meta2 = PngMeta(temp_path)
            assert meta2.get_xmp() == xmp_data
            assert meta2.get("XML:com.adobe.xmp") == xmp_data
        finally:
            Path(temp_path).unlink()

    def test_repr(self):
        """Test __repr__ method."""
        png_data = create_minimal_png()

        with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as f:
            f.write(png_data)
            temp_path = f.name

        try:
            meta = PngMeta(temp_path)
            meta.set("Title", "Test")
            repr_str = repr(meta)
            assert "PngMeta" in repr_str
            assert "1 metadata keys" in repr_str
        finally:
            Path(temp_path).unlink()
