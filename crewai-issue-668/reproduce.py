#!/usr/bin/env python3
"""Minimal reproduction for crewAI issue #668.

The reported error is a `NoneType` attribute failure on `startswith`. This
script models the unsafe string handling that triggers that exception.
"""

from __future__ import annotations


def buggy_tool_name_check(tool_name: str | None) -> bool:
    # BUG: calling string methods on a missing tool name crashes immediately.
    return tool_name.startswith("search")  # type: ignore[union-attr]


def fixed_tool_name_check(tool_name: str | None) -> bool:
    # Correct behavior: guard against None before checking the prefix.
    return bool(tool_name) and tool_name.startswith("search")


def main() -> int:
    tool_name = None

    print("Tool name:")
    print(tool_name)
    print()

    try:
        buggy_tool_name_check(tool_name)
    except AttributeError as exc:
        print("Buggy tool-name check error:")
        print(exc)
        print()
        assert "'NoneType' object has no attribute 'startswith'" in str(exc)

    print("Fixed tool-name check result:")
    print(fixed_tool_name_check(tool_name))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
