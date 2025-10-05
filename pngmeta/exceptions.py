"""Exception classes for pngmeta."""


class PngMetaError(Exception):
    """Base exception for pngmeta errors."""

    pass


class InvalidPngError(PngMetaError):
    """Raised when the file is not a valid PNG."""

    pass
