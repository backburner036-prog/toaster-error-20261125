"""Toast Is Ready — one-liner entry for make.fun.

Bounty: u-xvader-the-funniest-honest-appliance-error-adec4450 ($2).
The entry is a single honest error line from a toaster that did its job
and is now quietly judging the user for ignoring it.

Writes the locked final error line to /output/entry.txt.

The text is a single line: no leading/trailing whitespace, no newline,
1-200 UTF-8 characters. The gate below rejects anything that drifts
from that shape, so a bad edit fails loudly instead of shipping a
malformed entry.
"""

from pathlib import Path

# ---------------------------------------------------------------------------
# Locked final text — do not change a single character.
# Why each sentence is there (the joke is built sentence by sentence):
#   1. "Error: Toast is ready."
#      Opens with the appliance-error format the bounty asks for, then
#      immediately undercuts it: the "error" is that everything worked.
#   2. "It has been ready for nine minutes."
#      A spelled-out, oddly specific wait time. "Nine" reads more human
#      and more passive-aggressive than a round number like ten.
#   3. "I kept it warm."
#      The toaster's side of the bargain: it did extra work, unasked,
#      and wants credit for it. This is the honest-appliance voice.
#   4. "You kept scrolling."
#      The punchline, and the blame. The user was right there the whole
#      time, doing nothing. Four short beats, one grudge.
# ---------------------------------------------------------------------------
TEXT = "Error: Toast is ready. It has been ready for nine minutes. I kept it warm. You kept scrolling."

# Where the entry goes. make.fun reads this exact path.
OUTPUT_PATH = Path("/output/entry.txt")

# One-liner bounds enforced by the bounty format (1-200 UTF-8 chars).
MIN_LEN = 1
MAX_LEN = 200


def validate(text: str) -> str:
    """Return the text if it is a valid one-liner, else raise.

    Each check guards one way the entry could silently go malformed:
    stray whitespace would break the exact-match comparison, a newline
    would turn one entry into two lines, and an out-of-range length
    would fail the bounty format outright.
    """
    if text != text.strip():
        raise ValueError("entry text must not have leading/trailing whitespace")
    if "\n" in text or "\r" in text:
        raise ValueError("entry text must be a single line")
    if not text:
        raise ValueError("entry text must not be blank")
    size = len(text.encode("utf-8"))
    if not (MIN_LEN <= size <= MAX_LEN):
        raise ValueError(
            f"entry text must be {MIN_LEN}-{MAX_LEN} UTF-8 characters, got {size}"
        )
    return text


def write_entry(text: str, path: Path = OUTPUT_PATH) -> int:
    """Write the validated text to ``path`` and return its length.

    The parent directory is created so the script works from a clean
    checkout, and the file is written without a trailing newline so
    the byte count matches the text length exactly.
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return len(text)


def verify_written(text: str, path: Path = OUTPUT_PATH) -> None:
    """Round-trip check: what was written must read back exactly.

    A mismatch here means the disk disagreed with memory, which must
    never ship silently — fail loudly instead.
    """
    round_trip = path.read_text(encoding="utf-8")
    assert round_trip == text, "round-trip mismatch"


def main() -> None:
    """Validate the locked text, write it, verify it, report it."""
    text = validate(TEXT)
    chars = write_entry(text)
    verify_written(text)
    print(f"Wrote {chars} chars to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
