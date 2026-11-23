#!/usr/bin/env python3
"""One-line roast entry for make.fun.

The roast itself is the ROAST string below: a smartwatch that praises
me for standing and scolds me for sitting in the same minute. This
script checks the line against the competition gate (one line of
1-200 characters, not only whitespace) and writes it to
$MAKEFUN_OUTPUT_DIR/entry.txt (default /output/entry.txt).

Standard library only. No network, no input, no clock, no randomness:
two runs produce byte-identical output.
"""

import os
import sys

ROAST = (
    "My smartwatch congratulates me for standing, then warns I've been "
    "sitting too long \u2014 in the same minute, on the same wrist."
)

MAX_CHARS = 200


def check_line(line):
    """Return an error string if the line breaks the gate, else None."""
    if not isinstance(line, str):
        return "roast is not text"
    if "\n" in line or "\r" in line:
        return "roast must be a single line"
    if not line.strip():
        return "roast must not be only whitespace"
    if not 1 <= len(line) <= MAX_CHARS:
        return "roast is %d characters, gate allows 1-%d" % (
            len(line),
            MAX_CHARS,
        )
    return None


def write_entry(line, out_dir):
    """Write the line plus one trailing newline, atomically."""
    os.makedirs(out_dir, exist_ok=True)
    target = os.path.join(out_dir, "entry.txt")
    staging = target + ".tmp"
    with open(staging, "w", encoding="utf-8", newline="\n") as handle:
        handle.write(line + "\n")
        handle.flush()
        os.fsync(handle.fileno())
    os.replace(staging, target)
    return target


def main(argv):
    problem = check_line(ROAST)
    if problem is not None:
        print("invalid roast: " + problem, file=sys.stderr)
        return 1
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    target = write_entry(ROAST, out_dir)
    print("wrote %d characters to %s" % (len(ROAST), target))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
