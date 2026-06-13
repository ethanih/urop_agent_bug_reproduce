#!/usr/bin/env python3
"""Minimal reproduction for crewAI issue #2383.

The issue reports that some models do not call custom tools. The key failure
mode is that the agent receives text-only output instead of a tool call, so the
custom tool's `_run` method never executes.
"""

from __future__ import annotations


def buggy_should_call_tool(model_output: dict[str, object]) -> bool:
    # BUG: this branch only handles explicit tool calls and skips text-only
    # outputs, so some models never reach the custom tool.
    return bool(model_output.get("tool_calls"))


def fixed_should_call_tool(model_output: dict[str, object]) -> bool:
    # Correct behavior: detect the intent to use the tool even when the model
    # returns a plain assistant message that should be converted into a tool
    # invocation.
    return bool(model_output.get("tool_calls") or model_output.get("content"))


def main() -> int:
    model_output = {
        "content": "Thought: I should inspect the dataframe.\nAction: c_tool\nAction Input: {\"p\": \"value\"}",
        "tool_calls": None,
    }

    print("Model output:")
    print(model_output)
    print()

    buggy_result = buggy_should_call_tool(model_output)
    fixed_result = fixed_should_call_tool(model_output)

    print("Buggy tool-dispatch decision:")
    print(buggy_result)
    print()

    print("Fixed tool-dispatch decision:")
    print(fixed_result)

    assert buggy_result is False
    assert fixed_result is True
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
