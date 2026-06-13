#!/usr/bin/env python3
"""Minimal reproduction for crewAI issue #351.

The issue describes a delegation flow where the coworker name is correct, but
the system still reports that the coworker cannot be found. This script models
that by comparing a buggy lookup against the full crew roster.
"""

from __future__ import annotations


CREW_ROSTER = ["Senior Research Analyst", "Researcher", "Planner"]


def buggy_resolve_coworker(requested_name: str, current_agent_only: list[str]) -> str:
    # BUG: the lookup is performed against the wrong roster scope.
    # The crew member exists, but the current-agent list does not include them.
    if requested_name in current_agent_only:
        return requested_name
    raise LookupError(
        f"Co-worker mentioned not found, it must to be one of the following options: {current_agent_only}"
    )


def fixed_resolve_coworker(requested_name: str, crew_roster: list[str]) -> str:
    # Correct behavior: search the whole crew roster.
    if requested_name in crew_roster:
        return requested_name
    raise LookupError(f"Co-worker {requested_name!r} not found in crew roster")


def main() -> int:
    requested_name = "Senior Research Analyst"
    current_agent_only = ["Planner"]

    print("Requested coworker:")
    print(requested_name)
    print()

    try:
        buggy_resolve_coworker(requested_name, current_agent_only)
    except LookupError as exc:
        print("Buggy delegation lookup:")
        print(exc)
        print()
        assert "not found" in str(exc)

    print("Fixed delegation lookup:")
    print(fixed_resolve_coworker(requested_name, CREW_ROSTER))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
