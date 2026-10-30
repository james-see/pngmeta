"""MCP server exposing pngmeta PNG metadata tools to goose and other MCP clients."""

from mcp.server.fastmcp import FastMCP

from pngmeta import InvalidPngError, PngMeta, PngMetaError

mcp = FastMCP("pngmeta")


@mcp.tool()
def read_metadata(file_path: str) -> str:
    """Read all text metadata (tEXt, iTXt, zTXt) from a PNG file.

    Returns a readable summary of all metadata key-value pairs, plus XMP if present.
    Useful for inspecting PNG metadata like Title, Author, Copyright, Description, etc.
    """
    try:
        meta = PngMeta(file_path)
    except (InvalidPngError, FileNotFoundError) as e:
        return f"Error: {e}"

    lines = [f"File: {file_path}"]
    keys = list(meta.keys())
    if not keys:
        lines.append("  (no text metadata found)")
    for key in keys:
        if key == "XML:com.adobe.xmp":
            xmp = meta.get_xmp()
            if xmp:
                preview = xmp[:500] + ("..." if len(xmp) > 500 else "")
                lines.append(f"  XMP: {preview}")
            continue
        val = meta.get(key, "")
        preview = val[:500] + ("..." if len(val) > 500 else "")
        lines.append(f"  {key}: {preview}")

    return "\n".join(lines)


@mcp.tool()
def write_metadata(file_path: str, key: str, value: str) -> str:
    """Write or update a single text metadata key in a PNG file.

    The file is modified in place. Common keys: Title, Author, Copyright,
    Description, Software, Comment. Non-ASCII values are stored as iTXt chunks.
    """
    try:
        meta = PngMeta(file_path)
        meta.set(key, value)
        meta.save()
    except (InvalidPngError, FileNotFoundError, PngMetaError) as e:
        return f"Error: {e}"
    return f"OK: wrote '{key}' to {file_path}"


@mcp.tool()
def write_metadata_batch(file_path: str, entries: dict[str, str]) -> str:
    """Write multiple metadata key-value pairs to a PNG file in one pass.

    The file is modified in place. Example:
    entries = {"Title": "My Photo", "Author": "Jane", "Copyright": "2025"}
    """
    try:
        meta = PngMeta(file_path)
        for key, value in entries.items():
            meta.set(key, value)
        meta.save()
    except (InvalidPngError, FileNotFoundError, PngMetaError) as e:
        return f"Error: {e}"
    return f"OK: wrote {len(entries)} metadata keys to {file_path}"


@mcp.tool()
def get_xmp(file_path: str) -> str:
    """Extract XMP metadata from a PNG file as an XML string."""
    try:
        meta = PngMeta(file_path)
    except (InvalidPngError, FileNotFoundError) as e:
        return f"Error: {e}"
    xmp = meta.get_xmp() or ""
    if not xmp:
        return "No XMP metadata found."
    return xmp


@mcp.tool()
def set_xmp(file_path: str, xmp: str) -> str:
    """Set XMP metadata in a PNG file from an XML string. File is modified in place."""
    try:
        meta = PngMeta(file_path)
        meta.set_xmp(xmp)
        meta.save()
    except (InvalidPngError, FileNotFoundError, PngMetaError) as e:
        return f"Error: {e}"
    return f"OK: set XMP in {file_path}"


@mcp.tool()
def remove_metadata(file_path: str, key: str) -> str:
    """Remove a metadata key from a PNG file. File is modified in place.

    Note: This removes the key from the in-memory metadata dict and rewrites
    the file. All text chunks are regenerated from the remaining keys.
    """
    try:
        meta = PngMeta(file_path)
        if key not in meta:
            return f"Key '{key}' not found in {file_path}"
        # Re-read all keys, drop the target, rewrite
        remaining = {k: v for k, v in meta.items() if k != key}
        if "XML:com.adobe.xmp" in remaining and key == "XML:com.adobe.xmp":
            meta.set_xmp("")
        # Clear and re-set
        for k in list(meta.keys()):
            if k != key:
                continue
        # Rebuild from remaining
        meta2 = PngMeta(file_path)
        for k, v in remaining.items():
            if k == "XML:com.adobe.xmp":
                meta2.set_xmp(v)
            else:
                meta2.set(k, v)
        meta2.save()
    except (InvalidPngError, FileNotFoundError, PngMetaError) as e:
        return f"Error: {e}"
    return f"OK: removed '{key}' from {file_path}"


def main():
    mcp.run()


if __name__ == "__main__":
    main()
