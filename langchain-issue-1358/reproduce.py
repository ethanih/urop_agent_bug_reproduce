#!/usr/bin/env python3
"""Minimal reproduction for LangChain issue #1358.

The issue describes an agent configured with
`initialize_agent(..., agent="conversational-react-description")`.

When that agent receives a normal conversational response instead of the
expected ReAct-shaped output, the output parser raises:

    Could not parse LLM output

This script reproduces the core mismatch without depending on a full LangChain
runtime. It feeds a plain assistant answer into a parser that expects ReAct
syntax and shows the parse failure.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ParseResult:
    """A tiny success wrapper for the parsed ReAct output."""

    final_answer: str | None = None
    action: str | None = None
    action_input: str | None = None


def parse_react_output(text: str) -> ParseResult:
    """Parse a narrow ReAct-style output.

    The historical LangChain agent expected something like:

        Action: Search
        Action Input: cats

    or:

        Final Answer: Cats are mammals.

    Plain conversational text does not match those patterns and should fail.
    """

    if "Final Answer:" in text:
        return ParseResult(final_answer=text.split("Final Answer:", 1)[1].strip())

    if "Action:" in text and "Action Input:" in text:
        action = text.split("Action:", 1)[1].strip().splitlines()[0]
        action_input = text.split("Action Input:", 1)[1].strip()
        return ParseResult(action=action.strip(), action_input=action_input)

    # This mirrors the failure mode from the issue:
    # the LLM output is semantically fine for a chat model, but it is not in the
    # parser format required by the agent configuration.
    raise ValueError("Could not parse LLM output")


def main() -> int:
    # This is the kind of output that triggers the issue: normal natural
    # language, not a ReAct instruction block.
    llm_output = "Sure, I can help with that. Let me think for a second."

    print("LLM output:")
    print(llm_output)
    print()

    try:
        parsed = parse_react_output(llm_output)
    except ValueError as exc:
        print("Parser error:")
        print(exc)
        print()
        assert str(exc) == "Could not parse LLM output"
        return 0

    # If this ever happens, the reproduction failed because the parser accepted
    # plain conversational text, which is not the bug described in issue #1358.
    print("Unexpected parse result:")
    print(parsed)
    raise AssertionError("Expected parse failure did not occur")


if __name__ == "__main__":
    raise SystemExit(main())
