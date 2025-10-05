"""Core PngMeta class for reading and writing PNG metadata."""

import struct
import zlib
from pathlib import Path
from typing import Dict, Optional, Union

from .exceptions import InvalidPngError

PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"


class PngMeta:
    """
    Read and write PNG metadata chunks (tEXt, iTXt, zTXt).

    Usage:
        # Read metadata
        meta = PngMeta('image.png')
        title = meta.get('Title')

        # Write metadata
        meta.set('Author', 'John Doe')
        meta.set('Copyright', 'Copyright 2025')
        meta.save()

        # Access XMP
        xmp = meta.get_xmp()
        meta.set_xmp(xmp_string)
    """

    def __init__(self, filename: Union[str, Path]):
        """
        Initialize PngMeta with a PNG file.

        Args:
            filename: Path to the PNG file

        Raises:
            InvalidPngError: If the file is not a valid PNG
            FileNotFoundError: If the file doesn't exist
        """
        self.filename = Path(filename)
        self._metadata: Dict[str, str] = {}
        self._chunks = []
        self._xmp: Optional[str] = None

        if not self.filename.exists():
            raise FileNotFoundError(f"File not found: {filename}")

        self._read_file()

    def _read_file(self):
        """Read and parse the PNG file."""
        with open(self.filename, "rb") as f:
            # Verify PNG signature
            signature = f.read(8)
            if signature != PNG_SIGNATURE:
                raise InvalidPngError(f"Not a valid PNG file: {self.filename}")

            # Read all chunks
            while True:
                chunk = self._read_chunk(f)
                if chunk is None:
                    break

                self._chunks.append(chunk)

                # Parse text chunks
                chunk_type = chunk["type"]
                if chunk_type == b"tEXt":
                    self._parse_text_chunk(chunk["data"])
                elif chunk_type == b"iTXt":
                    self._parse_itxt_chunk(chunk["data"])
                elif chunk_type == b"zTXt":
                    self._parse_ztxt_chunk(chunk["data"])

                # Stop after IEND
                if chunk_type == b"IEND":
                    break

    def _read_chunk(self, f) -> Optional[Dict]:
        """Read a single PNG chunk."""
        # Read length (4 bytes)
        length_bytes = f.read(4)
        if len(length_bytes) < 4:
            return None

        length = struct.unpack(">I", length_bytes)[0]

        # Read chunk type (4 bytes)
        chunk_type = f.read(4)
        if len(chunk_type) < 4:
            return None

        # Read chunk data
        data = f.read(length)

        # Read CRC (4 bytes)
        crc = f.read(4)

        return {"length": length, "type": chunk_type, "data": data, "crc": crc}

    def _parse_text_chunk(self, data: bytes):
        """Parse a tEXt chunk."""
        # Format: Keyword\0Text
        null_pos = data.find(b"\x00")
        if null_pos == -1:
            return

        keyword = data[:null_pos].decode("latin-1")
        text = data[null_pos + 1 :].decode("latin-1")
        self._metadata[keyword] = text

    def _parse_itxt_chunk(self, data: bytes):
        """Parse an iTXt chunk."""
        # Format: Keyword\0Compression flag\0Compression method\0Language tag\0
        # Translated keyword\0Text
        null_pos = data.find(b"\x00")
        if null_pos == -1:
            return

        keyword = data[:null_pos].decode("latin-1")
        pos = null_pos + 1

        compression_flag = data[pos]
        pos += 1

        _compression_method = data[pos]
        pos += 1

        # Language tag
        null_pos = data.find(b"\x00", pos)
        if null_pos == -1:
            return
        pos = null_pos + 1

        # Translated keyword
        null_pos = data.find(b"\x00", pos)
        if null_pos == -1:
            return
        pos = null_pos + 1

        # Text (UTF-8)
        text_data = data[pos:]
        if compression_flag == 1:
            text_data = zlib.decompress(text_data)

        text = text_data.decode("utf-8", errors="replace")
        self._metadata[keyword] = text

        # Special handling for XMP
        if keyword == "XML:com.adobe.xmp":
            self._xmp = text

    def _parse_ztxt_chunk(self, data: bytes):
        """Parse a zTXt chunk."""
        # Format: Keyword\0Compression method\0Compressed text
        null_pos = data.find(b"\x00")
        if null_pos == -1:
            return

        keyword = data[:null_pos].decode("latin-1")
        # Skip compression method byte
        compressed_text = data[null_pos + 2 :]

        try:
            text = zlib.decompress(compressed_text).decode("latin-1")
            self._metadata[keyword] = text
        except Exception:
            pass

    def get(self, key: str, default=None) -> Optional[str]:
        """
        Get a metadata value by key.

        Args:
            key: The metadata key (e.g., 'Title', 'Author', 'Copyright')
            default: Default value if key doesn't exist

        Returns:
            The metadata value or default
        """
        return self._metadata.get(key, default)

    def set(self, key: str, value: str):
        """
        Set a metadata value.

        Args:
            key: The metadata key
            value: The metadata value
        """
        self._metadata[key] = value

    def get_xmp(self) -> Optional[str]:
        """Get the XMP metadata as a string."""
        return self._xmp

    def set_xmp(self, xmp: str):
        """
        Set the XMP metadata.

        Args:
            xmp: XMP metadata as an XML string
        """
        self._xmp = xmp
        self._metadata["XML:com.adobe.xmp"] = xmp

    def keys(self):
        """Return all metadata keys."""
        return self._metadata.keys()

    def items(self):
        """Return all metadata key-value pairs."""
        return self._metadata.items()

    def __getitem__(self, key: str) -> str:
        """Allow dictionary-style access."""
        return self._metadata[key]

    def __setitem__(self, key: str, value: str):
        """Allow dictionary-style assignment."""
        self._metadata[key] = value

    def __contains__(self, key: str) -> bool:
        """Check if a key exists."""
        return key in self._metadata

    def _create_text_chunk(self, keyword: str, text: str) -> bytes:
        """Create a tEXt chunk."""
        data = keyword.encode("latin-1") + b"\x00" + text.encode("latin-1")
        return self._create_chunk(b"tEXt", data)

    def _create_itxt_chunk(self, keyword: str, text: str, compress: bool = False) -> bytes:
        """Create an iTXt chunk."""
        compression_flag = 1 if compress else 0
        compression_method = 0

        text_data = text.encode("utf-8")
        if compress:
            text_data = zlib.compress(text_data)

        data = (
            keyword.encode("latin-1")
            + b"\x00"
            + bytes([compression_flag, compression_method])
            + b"\x00"  # Language tag
            + b"\x00"  # Translated keyword
            + text_data
        )
        return self._create_chunk(b"iTXt", data)

    def _create_chunk(self, chunk_type: bytes, data: bytes) -> bytes:
        """Create a complete PNG chunk with CRC."""
        length = struct.pack(">I", len(data))
        crc = struct.pack(">I", zlib.crc32(chunk_type + data) & 0xFFFFFFFF)
        return length + chunk_type + data + crc

    def save(self, filename: Optional[Union[str, Path]] = None):
        """
        Save the PNG file with updated metadata.

        Args:
            filename: Optional new filename. If None, overwrites the original file.
        """
        if filename is None:
            filename = self.filename
        else:
            filename = Path(filename)

        # Read original file
        with open(self.filename, "rb") as f:
            # Write signature
            output = bytearray(PNG_SIGNATURE)
            f.read(8)  # Skip signature

            # Track if we've inserted metadata chunks
            metadata_inserted = False

            while True:
                chunk = self._read_chunk(f)
                if chunk is None:
                    break

                chunk_type = chunk["type"]

                # Insert metadata chunks after IHDR, before IDAT
                if not metadata_inserted and chunk_type == b"IDAT":
                    # Remove old text chunks from output
                    # Add new metadata chunks
                    for key, value in self._metadata.items():
                        if key == "XML:com.adobe.xmp":
                            # Use iTXt for XMP
                            output += self._create_itxt_chunk(key, value)
                        elif any(ord(c) > 127 for c in value):
                            # Use iTXt for non-ASCII
                            output += self._create_itxt_chunk(key, value)
                        else:
                            # Use tEXt for ASCII
                            output += self._create_text_chunk(key, value)

                    metadata_inserted = True

                # Skip old text chunks
                if chunk_type in (b"tEXt", b"iTXt", b"zTXt"):
                    continue

                # Write chunk
                output += struct.pack(">I", chunk["length"])
                output += chunk["type"]
                output += chunk["data"]
                output += chunk["crc"]

                if chunk_type == b"IEND":
                    break

        # Write to file
        with open(filename, "wb") as f:
            f.write(output)

    def __repr__(self):
        return f"PngMeta('{self.filename}', {len(self._metadata)} metadata keys)"
