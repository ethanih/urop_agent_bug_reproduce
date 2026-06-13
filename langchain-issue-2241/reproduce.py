#!/usr/bin/env python3
"""Minimal reproduction for LangChain issue #2241.

The issue reports that nested markdown code blocks can break the conversational
chat agent response parsing. This script models the delimiter collision.
"""

from __future__ import annotations


def buggy_parse_agent_json(response_text: str) -> str:
    # BUG: a naive fence split stops at the first nested triple-backtick block.
    parts = response_text.split("```")
    if len(parts) < 3:
        raise ValueError("Missing JSON code block")
    return parts[1].strip()


def fixed_parse_agent_json(response_text: str) -> str:
    # Correct behavior: treat the outer response wrapper separately from any
    # inner markdown fence that appears in the payload.
    outer_start = response_text.find("```json")
    outer_end = response_text.rfind("```")
    if outer_start == -1 or outer_end == -1 or outer_end <= outer_start:
        raise ValueError("Missing JSON code block")
    return response_text[outer_start + len("```json"):outer_end].strip()


def main() -> int:
    response_text = """```json
{
  "action": "Final Answer",
  "action_input": "Use this snippet: ```python\\nprint('hello')\\n```"
}
```"""

    print("Agent response:")
    print(response_text)
    print()

    buggy_value = buggy_parse_agent_json(response_text)
    fixed_value = fixed_parse_agent_json(response_text)

    print("Buggy parsed payload:")
    print(buggy_value)
    print()

    print("Fixed parsed payload:")
    print(fixed_value)

    assert buggy_value.startswith("json")
    assert "print('hello')" in fixed_value
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
