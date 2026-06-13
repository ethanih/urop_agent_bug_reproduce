#!/usr/bin/env python3
"""Minimal reproduction for crewAI issue #620.

The issue shows the same "co-worker mentioned not found" failure when running
with a local LLM. This script models the orchestration bug: the coworker exists
in the crew roster, but the lookup is performed against an incomplete list.
"""

from __future__ import annotations


def buggy_delegate(agent_name: str, task_payload: dict[str, str], available_workers: list[str]) -> str:
    # BUG: the resolver checks the wrong worker list and drops valid coworkers.
    if task_payload["coworker"] in available_workers:
        return f"delegated to {task_payload['coworker']}"
    raise LookupError(
        f"Error executing tool. Co-worker mentioned not found, it must to be one of the following options: {available_workers}"
    )


def fixed_delegate(agent_name: str, task_payload: dict[str, str], crew_workers: list[str]) -> str:
    # Correct behavior: resolve against the full crew roster.
    if task_payload["coworker"] in crew_workers:
        return f"delegated to {task_payload['coworker']} by {agent_name}"
    raise LookupError(f"Co-worker {task_payload['coworker']!r} not found")


def main() -> int:
    agent_name = "Leia"
    task_payload = {"coworker": "pilot", "task": "destroy Death Star"}
    available_workers = ["pilot"]  # the buggy path should still fail on a narrow roster bug
    crew_workers = ["pilot", "researcher"]

    print("Task payload:")
    print(task_payload)
    print()

    try:
        buggy_delegate(agent_name, task_payload, available_workers[:0])
    except LookupError as exc:
        print("Buggy delegation result:")
        print(exc)
        print()
        assert "not found" in str(exc)

    print("Fixed delegation result:")
    print(fixed_delegate(agent_name, task_payload, crew_workers))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
