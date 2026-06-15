#!/usr/bin/env python3
"""Two-stage minimal reproduction for LangChain issue #1358."""

from __future__ import annotations


def parse_conversational_react_output(text: str) -> str:
    """Accept only the ReAct shapes expected by the historical agent parser."""

    if "Final Answer:" in text:
        return text.split("Final Answer:", 1)[1].strip()

    if "Action:" in text and "Action Input:" in text:
        return "tool-invocation"

    raise ValueError(f"Could not parse LLM output: {text}")


def main() -> int:
    # The normalized issue summary identifies this exact failure mode:
    # a non-OpenAI chat model returns a plain conversational greeting.
    model_output = "Assistant, how can I help you today?"

    print("Model output:")
    print(model_output)
    print()

    try:
        parse_conversational_react_output(model_output)
    except ValueError as exc:
        print("Parser error:")
        print(exc)
        assert str(exc) == "Could not parse LLM output: Assistant, how can I help you today?"
        return 0

    raise AssertionError("Expected parse failure did not occur")


if __name__ == "__main__":
    raise SystemExit(main())
