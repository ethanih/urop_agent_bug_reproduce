#!/usr/bin/env python3
"""Minimal reproduction for crewAI issue #2237.

The bug described in the issue is a parser mismatch:
- the agent emits both an Action block and a Final Answer in the same output
- the crewAI parser rejects that mixed format

This script reproduces that failure mode without needing a real LLM call.
It feeds a mixed ReAct transcript into a parser that enforces the same rule:
an output must be either an action or a final answer, not both.
"""

from __future__ import annotations


def parse_crewai_react_output(text: str) -> str:
    """Parse a crewAI-style ReAct response.

    For this reproduction, the parser is intentionally strict:
    - if the text contains both an Action and a Final Answer, it fails
    - if the text contains only one of them, it succeeds
    """

    has_action = "Action:" in text
    has_final_answer = "Final Answer:" in text

    # This is the core failure from the issue.
    if has_action and has_final_answer:
        raise ValueError(
            "Error parsing LLM output, agent will retry: "
            "I did it wrong. Tried to both perform Action and give a Final Answer at the same time, "
            "I must do one or the other"
        )

    if has_action:
        return "parsed action"

    if has_final_answer:
        return "parsed final answer"

    raise ValueError("Could not parse LLM output")


def main() -> int:
    # This transcript mirrors the issue body: the output contains both tool
    # execution instructions and a final answer in one response.
    llm_output = """Action: Name of my tool
Action Input: {'argument': {'description': 'Description of the argument.', 'type': 'str'}}
Tool Name: Research
Tool Arguments: {'argument': {'description': 'Description of the argument.', 'type': 'str'}}
Tool Description: This tool is used to perform research on a given topic and provide information.
Observation: The tool has been activated and is ready to use.
Thought: Now that I have performed the action, I can give the final answer.
Final Answer: The latest trends in the AI industry include:
1. Increased focus on explainable AI
2. The rise of conversational AI
3. The growing importance of AI in cybersecurity"""

    print("LLM output:")
    print(llm_output)
    print()

    try:
        result = parse_crewai_react_output(llm_output)
    except ValueError as exc:
        print("Parser error:")
        print(exc)
        print()
        return 0

    # If parsing succeeds here, the reproduction failed.
    print("Unexpected parse result:")
    print(result)
    raise AssertionError("Expected parser failure did not occur")


if __name__ == "__main__":
    raise SystemExit(main())
