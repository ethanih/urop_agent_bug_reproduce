#!/usr/bin/env python3
"""Minimal reproduction for openai/codex issue #666.

The issue reports that Codex can produce a patch-like suggestion in the
assistant message, but the change is not actually applied.

This MRE models that exact failure mode:
- create a temporary file
- generate a patch suggestion
- display the suggestion
- intentionally do not apply it
- verify that the file on disk is unchanged
"""

from __future__ import annotations

from pathlib import Path
from tempfile import TemporaryDirectory


def generate_patch_suggestion(original: str) -> str:
    """Return the content we would apply if the workflow were correct."""

    return original.replace("before", "after")


def suggest_without_applying(path: Path) -> str:
    """Simulate the broken Codex flow from the issue.

    The assistant has produced a patch suggestion, but the workflow stops
    before calling any apply function. That is the bug we want to show.
    """

    original = path.read_text()
    suggestion = generate_patch_suggestion(original)

    # Intentional bug reproduction:
    # we print the patch-like suggestion, but we never write it to disk.
    print("Suggested patch content:")
    print(suggestion, end="")
    return suggestion


def main() -> int:
    with TemporaryDirectory() as tmpdir:
        sample_file = Path(tmpdir) / "example.txt"
        sample_file.write_text("before\n")

        print("Original file content:")
        print(sample_file.read_text(), end="")
        print()

        suggestion = suggest_without_applying(sample_file)

        print("Actual file content after suggestion-only flow:")
        print(sample_file.read_text(), end="")
        print()

        # This is the observable failure: the file still has the original text.
        assert sample_file.read_text() == "before\n"
        assert suggestion == "after\n"

        # A correct implementation would have called:
        # sample_file.write_text(suggestion)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
