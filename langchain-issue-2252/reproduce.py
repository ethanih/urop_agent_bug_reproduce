#!/usr/bin/env python3
"""Minimal reproduction for LangChain issue #2252.

The issue reports inconsistent use of `python_repl_ast` in the dataframe agent.
This script models an agent that handles one question correctly and then skips
the tool on a similar question.
"""

from __future__ import annotations


def buggy_should_call_python_repl_ast(question: str) -> bool:
    # BUG: the decision is overfit to one query shape and misses similar ones.
    return "how many rows" in question.lower()


def fixed_should_call_python_repl_ast(question: str) -> bool:
    # Correct behavior: detect dataframe questions that require the python REPL
    # even when the wording changes.
    keywords = ("row", "rows", "dataframe", "report", "local report")
    lowered = question.lower()
    return any(keyword in lowered for keyword in keywords)


def main() -> int:
    questions = [
        "Please ask: how many rows",
        "Please ask: does fg-40f support local report",
    ]

    for question in questions:
        print("Question:")
        print(question)
        print()
        print("Buggy tool decision:")
        print(buggy_should_call_python_repl_ast(question))
        print("Fixed tool decision:")
        print(fixed_should_call_python_repl_ast(question))
        print()

    assert buggy_should_call_python_repl_ast(questions[0]) is True
    assert buggy_should_call_python_repl_ast(questions[1]) is False
    assert fixed_should_call_python_repl_ast(questions[1]) is True
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
