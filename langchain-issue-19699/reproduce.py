#!/usr/bin/env python3
"""Minimal reproduction for langchain issue #19699."""

import json


def main() -> int:
    invalid_router_output = '{\n  datasource: "python_docs"\n}'
    print("Router output:")
    print(invalid_router_output)
    try:
        json.loads(invalid_router_output)
    except json.JSONDecodeError as exc:
        print("\nJSONDecodeError raised:")
        print(exc)
        return 0
    raise AssertionError("Reproduction failed: invalid JSON unexpectedly parsed.")


if __name__ == "__main__":
    raise SystemExit(main())
