#!/usr/bin/env python3
"""Minimal reproduction for langchain issue #12077."""


def execute_sql(query: str) -> str:
    if query.lstrip().startswith("SQLQuery:"):
        raise ValueError(
            "Database executor received prompt-formatted SQL instead of raw SQL."
        )
    return "query succeeded"


def main() -> int:
    llm_output = (
        "SQLQuery:\n"
        "SELECT top 5 p.productname, sum(od.quantity) as total_sold\n"
        "FROM products p\n"
    )
    print("LLM output:")
    print(llm_output)
    try:
        execute_sql(llm_output)
    except ValueError as exc:
        print("Executor raised:")
        print(exc)
        return 0
    raise AssertionError("Reproduction failed: prefixed SQL unexpectedly succeeded.")


if __name__ == "__main__":
    raise SystemExit(main())
