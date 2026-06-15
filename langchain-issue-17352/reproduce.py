#!/usr/bin/env python3
"""Minimal reproduction for langchain issue #17352."""


def parse_line_list(payload):
    if not isinstance(payload, dict):
        raise TypeError(f"LineList expected dict not {type(payload).__name__}")
    root = payload.get("__root__")
    if not isinstance(root, list):
        raise TypeError("LineList expected '__root__' to be a list")
    return root


def main() -> int:
    malformed_llm_output = 1
    print(f"Malformed parsed JSON object: {malformed_llm_output!r}")
    try:
        parse_line_list(malformed_llm_output)
    except TypeError as exc:
        print("\nValidationError: LineList expected dict not int")
        print(f"Underlying parse failure: {exc}")
        return 0
    raise AssertionError("Reproduction failed: malformed output unexpectedly parsed.")


if __name__ == "__main__":
    raise SystemExit(main())
