#!/usr/bin/env python3
"""Minimal reproduction for crewAI issue #4788.

The reported regression happens when an assistant message contains both:

- normal text content
- native `tool_calls`

The buggy control flow in `llm.py` checks the text branch first and returns
early. Once that happens, the tool calls are ignored, so the tool is never
invoked even though the model asked for it.
"""

from __future__ import annotations


def llm_buggy_branch_order(response: dict[str, object], available_functions: object) -> dict[str, object]:
    """Model the buggy `llm.py` branch order."""

    content = response.get("content")
    tool_calls = response.get("tool_calls") or []

    if content is not None:
        return {
            "path": "text",
            "content": content,
            "tool_calls_seen": 0,
            "available_functions": available_functions,
        }

    if tool_calls:
        return {
            "path": "tool_calls",
            "content": None,
            "tool_calls_seen": len(tool_calls),
            "available_functions": available_functions,
        }

    return {
        "path": "empty",
        "content": None,
        "tool_calls_seen": 0,
        "available_functions": available_functions,
    }


def llm_fixed_branch_order(response: dict[str, object], available_functions: object) -> dict[str, object]:
    """Show the intended behavior."""

    content = response.get("content")
    tool_calls = response.get("tool_calls") or []

    if tool_calls:
        return {
            "path": "tool_calls",
            "content": content,
            "tool_calls_seen": len(tool_calls),
            "available_functions": available_functions,
        }

    if content is not None:
        return {
            "path": "text",
            "content": content,
            "tool_calls_seen": 0,
            "available_functions": available_functions,
        }

    return {
        "path": "empty",
        "content": None,
        "tool_calls_seen": 0,
        "available_functions": available_functions,
    }


def main() -> int:
    response = {
        "content": "I can help with that, and I will call the tool now.",
        "tool_calls": [
            {
                "name": "lookup_weather",
                "arguments": {"city": "Paris"},
            }
        ],
    }

    available_functions = None

    buggy_result = llm_buggy_branch_order(response, available_functions)
    fixed_result = llm_fixed_branch_order(response, available_functions)

    print("Incoming response:")
    print(response)
    print()

    print("Buggy llm.py branch order:")
    print(buggy_result)
    print()

    print("Fixed llm.py branch order:")
    print(fixed_result)
    print()

    assert buggy_result["path"] == "text"
    assert buggy_result["tool_calls_seen"] == 0
    assert fixed_result["path"] == "tool_calls"
    assert fixed_result["tool_calls_seen"] == 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
