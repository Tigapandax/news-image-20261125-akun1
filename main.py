"""Entrypoint: write the front-page image to /output/entry.png.

Standard library only. The image itself is built at build time by
draw.py and shipped as entry.png; this program checks it is a PNG of
at most 1024x1024 pixels, copies it to the output path, and verifies
the copy byte-for-byte, so both grading runs write identical bytes.

Run:  python3 draw.py && python3 main.py
"""

import hashlib
import os
import shutil
import struct
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "entry.png")
DST = os.path.join(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"),
                   "entry.png")
# MAKEFUN_OUTPUT_DIR is only a local-test convenience; the grader
# runs with /output writable, so the default path is what matters.
PNG_MAGIC = b"\x89PNG\r\n\x1a\n"
MAX_DIM = 1024


def png_size(path):
    """Read width/height from the PNG IHDR chunk (no image library)."""
    with open(path, "rb") as f:
        header = f.read(33)
    if header[:8] != PNG_MAGIC or header[12:16] != b"IHDR":
        return None
    width, height = struct.unpack(">II", header[16:24])
    return width, height


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    if not os.path.exists(SRC):
        print("entry.png missing next to main.py")
        return 1
    size = png_size(SRC)
    if size is None:
        print("entry.png is not a PNG file")
        return 1
    if size[0] > MAX_DIM or size[1] > MAX_DIM:
        print(f"entry.png is {size[0]}x{size[1]}, over the "
              f"{MAX_DIM}x{MAX_DIM} cap")
        return 1
    os.makedirs(os.path.dirname(DST), exist_ok=True)
    shutil.copyfile(SRC, DST)
    if sha256(SRC) != sha256(DST):
        print("copy mismatch: output differs from entry.png")
        return 1
    print(f"Wrote {DST} ({size[0]}x{size[1]}, "
          f"{os.path.getsize(DST)} bytes, copy verified)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
