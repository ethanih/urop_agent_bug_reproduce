#!/usr/bin/env python3
"""Minimal reproduction for crewAI issue #2288.

The issue reports that a tool input can arrive in the wrong shape, sometimes as
an extra list wrapper instead of the expected input dict. This script shows the
bad extraction path and the corrected one.
"""

from __future__ import annotations


def buggy_extract_tool_input(step_callback_payload: dict[str, object]) -> object:
    # BUG: the raw payload is passed through unchanged, including extra nesting.
    return step_callback_payload["tool_input"]


def fixed_extract_tool_input(step_callback_payload: dict[str, object]) -> dict[str, str]:
    # Correct behavior: normalize to the actual tool arguments dict.
    raw = step_callback_payload["tool_input"]
    if isinstance(raw, list) and raw:
        last_item = raw[-1]
        if isinstance(last_item, dict) and "tool_input" in last_item:
            return last_item["tool_input"]  # type: ignore[return-value]
    if isinstance(raw, dict):
        return raw  # type: ignore[return-value]
    raise TypeError("Unexpected tool_input shape")


def main() -> int:
    payload = {
        "tool_name": "Stock Info",
        "tool_input": [
            {"ticker": "VST"},
            {"tool_code": "Stock Info", "tool_input": {"ticker": "VST"}},
        ],
    }

    print("Step callback payload:")
    print(payload)
    print()

    buggy_value = buggy_extract_tool_input(payload)
    print("Buggy extracted tool input:")
    print(buggy_value)
    print()

    fixed_value = fixed_extract_tool_input(payload)
    print("Fixed extracted tool input:")
    print(fixed_value)

    assert isinstance(buggy_value, list)
    assert fixed_value == {"ticker": "VST"}
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
