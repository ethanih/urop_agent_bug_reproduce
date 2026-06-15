#!/usr/bin/env python3
"""Minimal reproduction for crewAI issue #3889."""

import json


def parse_tool_args(raw: str):
    parsed = json.loads(raw)
    if not isinstance(parsed, dict):
        raise TypeError(
            f"Tool arguments must be a dictionary, got {type(parsed).__name__}."
        )
    return parsed


def main() -> int:
    gpt5_payload = json.dumps(
        [{"responsible_employee_id": None, "include_inactive": False}, []]
    )
    print(f"Raw payload: {gpt5_payload}")
    try:
        parse_tool_args(gpt5_payload)
    except TypeError as exc:
        print("\nParser raised:")
        print(exc)
        return 0
    raise AssertionError("Reproduction failed: array-wrapped tool args were accepted.")


if __name__ == "__main__":
    raise SystemExit(main())
