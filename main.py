#!/usr/bin/env python3
"""Entry point for the news-image-20261119 submission.

The front page is rendered ahead of time by render.py and shipped as
entry.png. All this program does is copy that image into the output
directory named by the MAKEFUN_OUTPUT_DIR environment variable, using
only the Python standard library.
"""

import os
import shutil
from pathlib import Path


def main() -> None:
    out_dir = Path(os.environ["MAKEFUN_OUTPUT_DIR"])
    out_dir.mkdir(parents=True, exist_ok=True)
    source = Path(__file__).resolve().parent / "entry.png"
    target = out_dir / "entry.png"
    shutil.copyfile(source, target)
    if target.stat().st_size != source.stat().st_size:
        raise RuntimeError("copied entry.png does not match the shipped file")
    print(f"wrote {target} ({target.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
