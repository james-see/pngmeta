"""
pngmeta - A Python library for reading and writing PNG metadata.

Similar to iptcinfo3 for JPEG files, but designed for PNG text chunks
(tEXt, iTXt, zTXt) and XMP metadata.
"""

from .exceptions import InvalidPngError, PngMetaError
from .pngmeta import PngMeta

__version__ = "0.1.0"
__all__ = ["PngMeta", "PngMetaError", "InvalidPngError"]
