#!/usr/bin/env python3
"""Local constraint checks for the 25 November front page.

Usage:  python3 tests/check.py
Checks: image.png exists, is a PNG <= 1 MiB and <= 1024x1024,
main.py runs twice byte-identical, LICENSE + SOURCES.md present,
every required repo file present, no text below 11px is relied on
(the draw script asserts its own sizes at render time).
Exit 0 when all pass.
"""
import hashlib
import os
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def sha(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        h.update(f.read())
    return h.hexdigest()


def main():
    failures = []

    img = os.path.join(HERE, "image.png")
    if not os.path.exists(img):
        failures.append("image.png missing (run draw_frontpage.py first)")
    else:
        from PIL import Image
        im = Image.open(img)
        if im.size != (1024, 1024):
            failures.append(f"image.png is {im.size}, expected 1024x1024")
        if im.format != "PNG":
            failures.append(f"image.png format is {im.format}, expected PNG")
        size = os.path.getsize(img)
        print(f"image.png: {im.size} {im.format} {size} bytes")
        if size > 1024 * 1024:
            failures.append(f"image.png is {size} bytes, over the 1 MiB cap")

    for name in ("LICENSE", "SOURCES.md", "README.md", "main.py",
                 "draw_frontpage.py"):
        if not os.path.exists(os.path.join(HERE, name)):
            failures.append(f"{name} missing")

    for name in ("hero.png", "rescue.png", "mine.png", "space.png"):
        if not os.path.exists(os.path.join(HERE, "assets", name)):
            failures.append(f"assets/{name} missing")

    for name in ("NotoSerifDisplay-Black.ttf", "NotoSerif-Regular.ttf",
                 "NotoSerif-Bold.ttf", "NotoSerif-Italic.ttf",
                 "NotoSansCondensed-Bold.ttf"):
        if not os.path.exists(os.path.join(HERE, "fonts", name)):
            failures.append(f"fonts/{name} missing")

    owner = os.path.join(HERE, ".makefun", "owner.json")
    if not os.path.exists(owner):
        failures.append(".makefun/owner.json missing")
    else:
        import json
        with open(owner) as f:
            data = json.load(f)
        if data.get("wallet") != "6d3BQAd4CqJhbcArvh8EiehdZUpbRJmjaLmh8wYoPvZi":
            failures.append(".makefun/owner.json wallet mismatch")

    # determinism: run main.py twice into two temp dirs, compare hashes
    hashes = []
    for _ in range(2):
        with tempfile.TemporaryDirectory() as td:
            env = dict(os.environ, OUTPUT_DIR=td)
            r = subprocess.run([sys.executable, "main.py"], cwd=HERE,
                               env=env, capture_output=True, text=True)
            if r.returncode != 0:
                failures.append(f"main.py failed: {r.stderr.strip()}")
                break
            hashes.append(sha(os.path.join(td, "entry.png")))
    if len(hashes) == 2:
        print("run 1 sha256:", hashes[0][:16], " run 2 sha256:", hashes[1][:16])
        if hashes[0] != hashes[1]:
            failures.append("main.py is NOT deterministic (two runs differ)")

    if failures:
        print("FAIL:")
        for f in failures:
            print(" -", f)
        return 1
    print("ALL CHECKS PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
