"""Ship the rendered news poster as this entry's output.

Stdlib only. The poster itself is painted ahead of time by ``draw.py``
(Pillow, build time); this script only places the finished PNG into
the output directory the harness provides.

Run it directly to check the flow locally::

    MAKEFUN_OUTPUT_DIR=/tmp/out25 python3 main.py
"""

from __future__ import annotations

import os
import shutil
from pathlib import Path

POSTER_NAME = "entry.png"


def poster_source() -> Path:
    """The finished poster sitting next to this script."""
    here = Path(__file__).resolve().parent
    return here / POSTER_NAME


def output_dir() -> Path:
    """Where the harness wants the entry (default: /output)."""
    return Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))


def place_poster() -> Path:
    """Copy the poster into the output directory; return its new path."""
    src = poster_source()
    if not src.is_file():
        raise SystemExit(f"poster missing next to this script: {src}")
    dest_dir = output_dir()
    dest_dir.mkdir(parents=True, exist_ok=True)
    dest = dest_dir / POSTER_NAME
    shutil.copyfile(src, dest)
    return dest


def main() -> None:
    dest = place_poster()
    size = dest.stat().st_size
    print(f"entry ready: {dest} ({size} bytes)")


if __name__ == "__main__":
    main()
