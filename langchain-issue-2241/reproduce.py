#!/usr/bin/env python3
"""Two-stage minimal reproduction for LangChain issue #2241."""

from __future__ import annotations


def buggy_extract_json_block(response_text: str) -> str:
    """Naively split on code fences, matching the issue's failure mode."""

    return response_text.split("```")[1].strip()


def fixed_extract_json_block(response_text: str) -> str:
    """Extract the outer JSON fence without being confused by inner fences."""

    start = response_text.find("```json")
    end = response_text.rfind("```")
    if start == -1 or end == -1 or end <= start:
        raise ValueError("Missing outer JSON code block")
    return response_text[start + len("```json"):end].strip()


def main() -> int:
    response_text = """```json
{
  "action": "Final Answer",
  "action_input": "Here is the generated code:\\n```python\\nprint('hello')\\n```"
}
```"""

    print("Agent response:")
    print(response_text)
    print()

    buggy = buggy_extract_json_block(response_text)
    fixed = fixed_extract_json_block(response_text)

    print("Buggy extracted payload:")
    print(buggy)
    print()

    print("Fixed extracted payload:")
    print(fixed)

    assert "```python" not in buggy
    assert "```python" in fixed
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
