#!/usr/bin/env python3
"""Minimal reproduction for openai/codex issue #802.

The bug being modeled here is simple:
- a change suggestion is generated
- the suggestion is shown to the user
- but the suggestion is never actually applied to disk

This script reproduces that failure mode without depending on Codex itself.
It deliberately separates "propose a change" from "apply the change" and then
omits the apply step.
"""

from __future__ import annotations

from pathlib import Path
from tempfile import TemporaryDirectory


def generate_suggested_change(original: str) -> str:
    """Return the text we would *like* to write."""

    return original.replace("before", "after")


def propose_change_only(path: Path) -> str:
    """Simulate the broken behavior from the issue."""

    original = path.read_text()
    suggestion = generate_suggested_change(original)

    # Intentionally no `path.write_text(...)` here.
    # The bug is that the workflow stops at "suggested changes" instead of
    # applying the patch to the file system.
    print("Suggested content:")
    print(suggestion)
    return suggestion


def apply_change(path: Path, suggestion: str) -> None:
    """The behavior that should have happened."""

    path.write_text(suggestion)


def main() -> int:
    with TemporaryDirectory() as tmpdir:
        sample_file = Path(tmpdir) / "example.txt"
        sample_file.write_text("before\n")

        print("Original file content:")
        print(sample_file.read_text(), end="")
        print()

        suggestion = propose_change_only(sample_file)

        # This confirms the regression: the file still has the old content.
        actual_after_suggestion = sample_file.read_text()
        print("Actual file content after suggestion-only flow:")
        print(actual_after_suggestion, end="")
        print()

        assert actual_after_suggestion == "before\n"
        assert suggestion == "after\n"

        # Uncommenting the next line would fix the reproduction, but we keep it
        # disabled so the script continues to demonstrate the bug.
        # apply_change(sample_file, suggestion)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
