#!/usr/bin/env python3
"""make.fun entry: one-line resignation letter of a retry loop.

Writes ONE line (no trailing newline) to $MAKEFUN_OUTPUT_DIR/entry.txt
(default /output/entry.txt). Python stdlib only, deterministic, no network.
"""

import os
import sys

LINE = (
    "After three attempts with exponential backoff, I have backed off "
    "permanently; consider this attempt zero, there will be no retry."
)

MAX_CHARS = 140


def validate(text: str) -> None:
    """Enforce the gate: UTF-8 encodable, 1-140 chars, single line, non-blank."""
    if not isinstance(text, str):
        raise ValueError("line must be a string")
    if not text.strip():
        raise ValueError("line must not be only whitespace")
    if not (1 <= len(text) <= MAX_CHARS):
        raise ValueError(f"line must be 1-{MAX_CHARS} characters, got {len(text)}")
    if "\n" in text or "\r" in text:
        raise ValueError("line must be a single line (no newline characters)")
    if text != text.strip():
        raise ValueError("line must not have leading or trailing whitespace")
    if any(ord(ch) < 0x20 or ord(ch) == 0x7F for ch in text):
        raise ValueError("line must not contain control characters")
    # Must be encodable as UTF-8.
    text.encode("utf-8")


def main() -> int:
    validate(LINE)

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "entry.txt")

    data = LINE.encode("utf-8")
    with open(out_path, "wb") as f:
        f.write(data)

    # Byte-exact read-back check: what is on disk must equal what we intended,
    # with no trailing newline added.
    with open(out_path, "rb") as f:
        written = f.read()
    if written != data:
        raise RuntimeError(
            f"read-back mismatch: wrote {len(data)} bytes, read {len(written)} bytes"
        )
    if written.endswith(b"\n") or written.endswith(b"\r"):
        raise RuntimeError("entry.txt must not have a trailing newline")
    # The bytes on disk must also decode and pass the same gate as the source.
    validate(written.decode("utf-8"))

    return 0


if __name__ == "__main__":
    sys.exit(main())
