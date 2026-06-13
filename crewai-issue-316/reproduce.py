#!/usr/bin/env python3
"""Minimal reproduction for crewAI issue #316.

The bug report shows a DuckDuckGo search tool receiving a `q` keyword argument
and then failing because the underlying runner expects a plain search string.
This script models that argument-shape mismatch directly.
"""

from __future__ import annotations


def duckduckgo_search_run(query: str) -> str:
    # This stands in for the real search backend.
    return f"search results for {query!r}"


def buggy_tool_dispatch(tool_input: dict[str, str]) -> str:
    # BUG: the wrapper forwards the entire dict as keyword arguments.
    # The backend expects a single positional search string, not `q=...`.
    return duckduckgo_search_run(**tool_input)  # type: ignore[arg-type]


def fixed_tool_dispatch(tool_input: dict[str, str]) -> str:
    # Correct behavior: pass the query value as the positional search string.
    return duckduckgo_search_run(tool_input["q"])


def main() -> int:
    tool_input = {"q": "AI news latest not older than 1 day"}

    print("Tool input:")
    print(tool_input)
    print()

    try:
        buggy_tool_dispatch(tool_input)
    except TypeError as exc:
        print("Buggy dispatch error:")
        print(exc)
        print()
        assert "unexpected keyword argument 'q'" in str(exc)

    print("Fixed dispatch result:")
    print(fixed_tool_dispatch(tool_input))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
