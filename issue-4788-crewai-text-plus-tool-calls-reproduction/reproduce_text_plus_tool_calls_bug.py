#!/usr/bin/env python3
"""Minimal reproduction for crewAI issue #4788.

This script mirrors the relevant branch order from `crewai/llm.py` as described
in the issue:

1. inspect the LLM response for assistant text
2. if text exists, return it immediately
3. only then consider native `tool_calls`

That order is the bug. A single response that contains both text and
`tool_calls` loses the tool call because the text branch returns first.
"""

from __future__ import annotations

from typing import Any


def llm_buggy_branch_order(response: dict[str, Any], available_functions: Any) -> dict[str, Any]:
    """Model the buggy `llm.py` branch order.

    The issue report says `available_functions=None`, but the real regression is
    the branch order itself: native tool calls are reachable only after the text
    branch, so any response with content exits early.
    """

    content = response.get("content")
    tool_calls = response.get("tool_calls") or []

    # This corresponds to the text branch in `llm.py`.
    # It returns immediately, so the native tool call branch below never runs
    # when the model emits both content and tool calls in the same message.
    if content is not None:
        return {
            "path": "text",
            "content": content,
            "tool_calls_seen": 0,
            "available_functions": available_functions,
        }

    # This corresponds to the native tool call branch in `llm.py`.
    # It is correct only when the text branch did not already return.
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


def llm_fixed_branch_order(response: dict[str, Any], available_functions: Any) -> dict[str, Any]:
    """Show the intended behavior.

    If the response contains native tool calls, they should be visible to the
    caller even when assistant text is also present.
    """

    content = response.get("content")
    tool_calls = response.get("tool_calls") or []

    # Fix: prioritize `tool_calls` before treating the response as a completed
    # text answer.
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
    # This response shape is the reproduction target:
    # one assistant message contains both normal text and a native tool call.
    response = {
        "content": "I can help with that, and I will call the tool now.",
        "tool_calls": [
            {
                "name": "lookup_weather",
                "arguments": {"city": "Paris"},
            }
        ],
    }

    # The issue report explicitly mentions `available_functions=None`.
    # Keeping that state here makes the reproduction align with the report, but
    # the bug still reproduces because the text branch returns first.
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

    # The bug: text is returned and the tool call is never surfaced.
    assert buggy_result["path"] == "text"
    assert buggy_result["tool_calls_seen"] == 0

    # The intended behavior: the tool call is visible even though content exists.
    assert fixed_result["path"] == "tool_calls"
    assert fixed_result["tool_calls_seen"] == 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
