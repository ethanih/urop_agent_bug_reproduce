#!/usr/bin/env python3
"""Minimal reproduction for LangChain issue #1657.

The issue shows a parser error when a conversational agent receives plain text
that does not match the expected ReAct format.
"""

from __future__ import annotations


def parse_llm_output(llm_output: str) -> str:
    # BUG: the parser expects ReAct-style formatting, so plain text fails.
    if "Final Answer:" in llm_output:
        return llm_output.split("Final Answer:", 1)[1].strip()
    if "Action:" in llm_output and "Action Input:" in llm_output:
        return "parsed-action"
    raise ValueError(f"Could not parse LLM output: `{llm_output}`")


def main() -> int:
    llm_output = "Thought: Do I need to use a tool? No"

    print("LLM output:")
    print(llm_output)
    print()

    try:
        parse_llm_output(llm_output)
    except ValueError as exc:
        print("Parser error:")
        print(exc)
        print()
        assert "Could not parse LLM output" in str(exc)
        return 0

    raise AssertionError("Expected parse failure did not occur")


if __name__ == "__main__":
    raise SystemExit(main())
