#!/usr/bin/env python3
"""Minimal reproduction for crewAI issue #3873."""


def manager_finalize(delegate_result: str) -> str:
    if "FAILED" in delegate_result:
        return (
            "Thought: The delegated task failed.\n"
            "Action: Retry postgres expert\n"
            "Action Input: Fetch list of tables from postgres db\n"
        )
    return "Here is the final user-facing answer."


def main() -> int:
    leaked = manager_finalize("FAILED: permission denied")
    print("Final answer returned by manager:")
    print(leaked)
    assert "Thought:" in leaked
    assert "Action:" in leaked
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
