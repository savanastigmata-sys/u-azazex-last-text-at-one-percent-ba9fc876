"""Last Text at One Percent — make.fun entry.

Writes the phone's final text message to $MAKEFUN_OUTPUT_DIR/entry.txt.
Deterministic: the same single line on every run, no I/O besides the
output file, no network, no randomness.
"""

import os
import sys

# The entry: one line, the dying phone's last text. Under 200 characters,
# in the phone's own voice, with a real turn: the owner used it up.
TEXT = (
    "1%. Screen time today: 9 hours. I didn't run out of battery "
    "- you used me up. Tell the charger it was too late. It always is."
)

MAX_CHARS = 200


def resolve_output_dir():
    """Return the output directory.

    $MAKEFUN_OUTPUT_DIR wins when set to a non-empty value (an empty
    string counts as unset); otherwise fall back to ./output next to
    this file, so a bare `python3 main.py` still works.
    """
    out = os.environ.get("MAKEFUN_OUTPUT_DIR", "").strip()
    if out:
        return out
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), "output")


def validate(text):
    """Enforce the gate: 1-200 chars, one line, not only whitespace."""
    if not isinstance(text, str):
        raise ValueError("entry text must be a string")
    if not (1 <= len(text) <= MAX_CHARS):
        raise ValueError("entry must be 1-%d characters, got %d"
                         % (MAX_CHARS, len(text)))
    if text.strip() == "":
        raise ValueError("entry must not be only whitespace")
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be a single line")
    if any(ord(ch) < 32 for ch in text):
        raise ValueError("entry must not contain control characters")
    text.encode("utf-8")  # must be valid UTF-8
    return text


def write_entry(text, out_dir):
    """Write the validated text to entry.txt and verify the round-trip."""
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(text)
    with open(path, "r", encoding="utf-8", newline="") as f:
        written = f.read()
    if written != text:
        raise ValueError("round-trip mismatch: file content differs from entry")
    return path


def main():
    text = validate(TEXT)
    path = write_entry(text, resolve_output_dir())
    print("wrote %s (%d chars)" % (path, len(text)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
