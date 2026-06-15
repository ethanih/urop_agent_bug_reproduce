#!/usr/bin/env python3
"""Minimal reproduction for crewAI issue #351."""

from __future__ import annotations


CREW_ROSTER = ["Senior Research Analyst", "Planner"]


def buggy_resolve_coworker(requested_name: str, visible_options: list[str]) -> str:
    if requested_name in ["Planner"]:
        return requested_name
    raise LookupError(
        "Co-worker mentioned not found, it must to be one of the following options:\n"
        + "\n".join(f"- {name}" for name in visible_options)
    )


def fixed_resolve_coworker(requested_name: str, crew_roster: list[str]) -> str:
    if requested_name in crew_roster:
        return requested_name
    raise LookupError(f"Co-worker {requested_name!r} not found")


def main() -> int:
    requested_name = "Senior Research Analyst"

    print("Requested coworker:")
    print(requested_name)
    print()

    try:
        buggy_resolve_coworker(requested_name, [requested_name])
    except LookupError as exc:
        print("Actual result:")
        print(exc)
        print()

    print("Expected result if resolution is correct:")
    print(fixed_resolve_coworker(requested_name, CREW_ROSTER))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
