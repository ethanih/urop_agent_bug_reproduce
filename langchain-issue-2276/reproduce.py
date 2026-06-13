#!/usr/bin/env python3
"""Two-stage minimal reproduction for LangChain issue #2276."""

from __future__ import annotations

import json


VALID_TOOLS = {"Final Answer"}


def parse_chat_json(text: str) -> dict[str, str]:
    """Mirror the strict JSON parsing path from the issue traceback."""

    return json.loads(text)


def execute_tool(action: dict[str, str]) -> str:
    tool_name = action["action"]
    if tool_name not in VALID_TOOLS:
        raise ValueError(f"{tool_name} is not a valid tool, try another one.")
    return action["action_input"]


def main() -> int:
    first_retry_candidate = json.dumps(
        {
            "action": "recommend_tool",
            "action_input": "Search LinkedIn for information on Will.",
        }
    )
    second_retry_candidate = "Thought: I should try a different tool."

    print("First model output:")
    print(first_retry_candidate)
    print()

    parsed = parse_chat_json(first_retry_candidate)

    try:
        execute_tool(parsed)
    except ValueError as exc:
        print("Invalid tool observation:")
        print(exc)
        print()
        assert "recommend_tool is not a valid tool" in str(exc)

    print("Second model output:")
    print(second_retry_candidate)
    print()

    try:
        parse_chat_json(second_retry_candidate)
    except json.JSONDecodeError as exc:
        print("Retry parse error:")
        print(exc)
        assert "Expecting value" in str(exc)
        return 0

    raise AssertionError("Expected retry parse failure did not occur")


if __name__ == "__main__":
    raise SystemExit(main())
