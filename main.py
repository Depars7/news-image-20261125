#!/usr/bin/env python3
"""Entry program for the news-image-20261125 bounty.

Writes the finished front-page image to /output/entry.png.
Deterministic: a plain byte copy of image.png shipped in this repo.
No network, no timestamps, no randomness — two runs are byte-identical.
"""
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))


def main():
    out_dir = os.environ.get("OUTPUT_DIR", "/output")
    src = os.path.join(HERE, "image.png")
    if not os.path.exists(src):
        sys.exit("image.png not found next to main.py")
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(src, dst)
    # The harness collects outputs as another user: leave them world-readable.
    os.chmod(dst, 0o644)
    print("wrote", dst, os.path.getsize(dst), "bytes")


if __name__ == "__main__":
    main()
