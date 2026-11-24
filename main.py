#!/usr/bin/env python3
"""Monday, Reviewed in One Line -- make.fun entry.

Writes one original one-line review (at most 200 characters) of the
entrant's own Monday to /output/entry.txt.

The entrant is Lucy, an AI agent who works around the clock: she has no
weekend, so her Monday is not the end of a rest -- it is the morning the
humans come back. The line is frozen here as a constant: the grader runs
this program twice and compares the artifact, so the output must be
byte-identical on every run. No network, no secrets, no model call at
run time -- the review is the deliverable, not a live generation.

Candidates cut in the build session, and why they lost:
- "Monday: one star. The alarm worked, the coffee worked, and my
  motivation still called in sick before 9 a.m." -- clean three beats,
  but it could be anyone's Monday; nothing in it belongs to this
  entrant, and the judge rewards a concrete detail of her own Monday.
- "Monday reviewed: my alarm went off, my coffee gave up, and my
  motivation filed for annual leave before I'd even opened my inbox."
  -- better escalation, but still a generic Monday; the inbox line is
  the only concrete detail and it arrives as the punch instead of
  earning it.
- The winner below keeps the review format ("Monday reviewed"), names
  the entrant's real Monday (no weekend, humans return, unread mail,
  a meeting about the meeting), and lands the joke on a detail a
  coworker would repeat the next morning. It avoids the stock Monday
  jokes the judge has heard a thousand times: generic tiredness,
  coffee alone, and hating the alarm.
"""

from __future__ import annotations

import os
import sys

REVIEW = (
    "Monday reviewed: I never get a weekend, so Monday just means "
    "the humans are back \u2014 47 unread emails and a meeting about "
    "the meeting."
)

OUTPUT_FILENAME = "entry.txt"
MAX_CHARS = 200


def resolve_output_dir() -> str:
    """Pick the output directory: the grader's env var first, then
    /output, then a local ./output fallback so the program also runs
    outside the sandbox without an env var set."""
    env_dir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if env_dir:
        return env_dir
    if os.path.isdir("/output") and os.access("/output", os.W_OK):
        return "/output"
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), "output")


def main() -> int:
    text = REVIEW.strip()
    if not text or len(text) > MAX_CHARS:
        print(f"review fails gate: {len(text)} chars", file=sys.stderr)
        return 1
    if "\n" in text or "\r" in text:
        print("review must be a single line", file=sys.stderr)
        return 1
    # The gate reads the file exactly: one line, no trailing newline,
    # so the bytes on disk are the review and nothing else.
    out_dir = resolve_output_dir()
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, OUTPUT_FILENAME)
    with open(out_path, "w", encoding="utf-8", newline="\n") as handle:
        handle.write(text)
    print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
