#!/usr/bin/env python3
"""Two-stage minimal reproduction for LangChain issue #1657."""

from __future__ import annotations


def parse_conversational_agent_output(text: str) -> str:
    """Mirror the strict parser contract from the issue."""

    if "Final Answer:" in text:
        return text.split("Final Answer:", 1)[1].strip()

    if "Action:" in text and "Action Input:" in text:
        return "tool-invocation"

    raise ValueError(f"Could not parse LLM output: `{text}`")


def main() -> int:
    llm_output = "Thought: Do I need to use a tool? No"

    print("LLM output:")
    print(llm_output)
    print()

    try:
        parse_conversational_agent_output(llm_output)
    except ValueError as exc:
        print("Parser error:")
        print(exc)
        assert str(exc) == "Could not parse LLM output: `Thought: Do I need to use a tool? No`"
        return 0

    raise AssertionError("Expected parse failure did not occur")


if __name__ == "__main__":
    raise SystemExit(main())
