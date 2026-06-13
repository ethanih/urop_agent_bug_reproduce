#!/usr/bin/env python3
"""Minimal reproduction for LangChain issue #2276.

The issue reports an exception when the conversation agent receives output that
is not valid JSON for the expected response format. This script models the
invalid-tool path that triggers the failure.
"""

from __future__ import annotations

import json


def buggy_parse_agent_response(response_text: str) -> dict[str, str]:
    # BUG: the parser assumes the model always returns valid JSON.
    return json.loads(response_text)


def fixed_handle_agent_response(response_text: str) -> dict[str, str]:
    # Correct behavior: detect the invalid tool response and convert it into a
    # recovery path instead of crashing.
    try:
        return json.loads(response_text)
    except json.JSONDecodeError:
        return {"action": "Final Answer", "action_input": response_text}


def main() -> int:
    response_text = "{action: recommend_tool, action_input: I recommend searching on LinkedIn.}"

    print("Model response:")
    print(response_text)
    print()

    try:
        parsed = buggy_parse_agent_response(response_text)
    except json.JSONDecodeError as exc:
        print("Buggy parse error:")
        print(exc)
        print()
        assert "Expecting" in str(exc)
        parsed = fixed_handle_agent_response(response_text)
    else:
        print("Buggy parsed response:")
        print(parsed)
        print()
        parsed = fixed_handle_agent_response(response_text)

    print("Fixed handled response:")
    print(parsed)
    assert parsed["action"] == "Final Answer"
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
