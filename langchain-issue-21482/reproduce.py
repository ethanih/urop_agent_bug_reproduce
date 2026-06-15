#!/usr/bin/env python3
"""Minimal reproduction for langchain issue #21482."""


def process_response(raw_schema):
    return raw_schema.content


def main() -> int:
    raw_schema = '{"nodes": [], "relationships": []}'
    print(f"raw_schema type: {type(raw_schema).__name__}")
    try:
        process_response(raw_schema)
    except AttributeError as exc:
        print("\nTransformer raised:")
        print(exc)
        return 0
    raise AssertionError("Reproduction failed: string unexpectedly exposed .content.")


if __name__ == "__main__":
    raise SystemExit(main())
