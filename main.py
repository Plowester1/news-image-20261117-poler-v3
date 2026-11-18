"""news-image-20261117-poler-v3 entry: emit /output/entry.png.

The infographic (entry.png, next to this file) is a 1024x1024 neon-cyber
front page summing up Tuesday 17 November 2026 in eight verified stories,
composed programmatically with PIL (see build_image.py). This program only
copies that file to the output directory: no network, no randomness, so
two runs write byte-identical output.
"""
import hashlib
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SOURCE = os.path.join(HERE, "entry.png")
OUT_DIR = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")


def digest(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        while True:
            chunk = fh.read(1 << 20)
            if not chunk:
                break
            h.update(chunk)
    return h.hexdigest()


def main():
    if not os.path.isfile(SOURCE):
        print("missing bundled image: %s" % SOURCE, file=sys.stderr)
        return 1
    if os.path.exists(OUT_DIR) and not os.path.isdir(OUT_DIR):
        print("output path is not a directory: %s" % OUT_DIR, file=sys.stderr)
        return 1
    os.makedirs(OUT_DIR, exist_ok=True)
    dest = os.path.join(OUT_DIR, "entry.png")
    shutil.copyfile(SOURCE, dest)
    # Flush to disk before verifying, so the digest reads the final bytes.
    with open(dest, "rb") as fh:
        os.fsync(fh.fileno())
    # The harness runs this program twice and compares bytes, so refuse to
    # hand over a copy that differs from the bundled source.
    if digest(dest) != digest(SOURCE):
        print("copy verification failed: output differs from source",
              file=sys.stderr)
        return 1
    print("wrote %s (%d bytes)" % (dest, os.path.getsize(dest)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
