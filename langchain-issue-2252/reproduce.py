#!/usr/bin/env python3
"""Two-stage minimal reproduction for LangChain issue #2252."""

from __future__ import annotations


VALID_TOOLS = {"python_repl_ast"}


def validate_tool_name(tool_name: str) -> str:
    if tool_name not in VALID_TOOLS:
        raise ValueError(f"{tool_name} is not a valid tool, try another one.")
    return tool_name


def main() -> int:
    successful_action = "python_repl_ast"
    failing_action = (
        "Use pandas boolean indexing to filter the dataframe to only the "
        '"FG-40F Series" row and check the value in the "Local Reporting" column.'
    )

    print("Successful action:")
    print(successful_action)
    print("Validation result:")
    print(validate_tool_name(successful_action))
    print()

    print("Failing action:")
    print(failing_action)
    print()

    try:
        validate_tool_name(failing_action)
    except ValueError as exc:
        print("Invalid tool error:")
        print(exc)
        assert "is not a valid tool" in str(exc)
        return 0

    raise AssertionError("Expected invalid-tool failure did not occur")


if __name__ == "__main__":
    raise SystemExit(main())
