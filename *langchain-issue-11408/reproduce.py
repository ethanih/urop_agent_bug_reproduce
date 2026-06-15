#!/usr/bin/env python3
"""Minimal reproduction for langchain issue #11408."""


def parse_boolean_output(text: str) -> bool:
    cleaned = text.strip()
    if cleaned == "YES":
        return True
    if cleaned == "NO":
        return False
    raise ValueError(
        "BooleanOutputParser expected output value to either be YES or NO. "
        f"Received {cleaned}"
    )


def main() -> int:
    llm_response = "Yes, the context is relevant to the question."
    print(f"Raw LLM response: {llm_response}")
    try:
        parse_boolean_output(llm_response)
    except ValueError as exc:
        print("\nParser raised:")
        print(exc)
        return 0
    raise AssertionError("Reproduction failed: parser unexpectedly accepted verbose input.")


if __name__ == "__main__":
    raise SystemExit(main())
