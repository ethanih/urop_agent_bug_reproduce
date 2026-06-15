#!/usr/bin/env python3
"""Minimal reproduction for crewAI issue #316."""

from __future__ import annotations


def duckduckgo_search_run(query: str) -> str:
    return f"search results for {query!r}"


def buggy_tool_dispatch(tool_input: dict[str, str]) -> str:
    return duckduckgo_search_run(**tool_input)  # type: ignore[arg-type]


def fixed_tool_dispatch(tool_input: dict[str, str]) -> str:
    return duckduckgo_search_run(tool_input["q"])


def main() -> int:
    tool_input = {"q": "AIi news latest not older than 1 day"}

    print("Tool input:")
    print(tool_input)
    print()

    try:
        buggy_tool_dispatch(tool_input)
    except TypeError as exc:
        print("Actual result:")
        print(type(exc).__name__ + ":", exc)
        print()

    print("Expected result if forwarded correctly:")
    print(fixed_tool_dispatch(tool_input))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
