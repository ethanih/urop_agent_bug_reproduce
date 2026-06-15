#!/usr/bin/env python3
"""Minimal reproduction for crewAI issue #3915."""

from pydantic import BaseModel, ValidationError


class TaskEvaluation(BaseModel):
    quality: str
    suggestions: list[str]


def main() -> int:
    payload = {
        "suggestions": [
            {"point": "Proceed immediately", "priority": "high"},
            {"point": "Use markdown formatting", "priority": "medium"},
        ]
    }
    print(f"Payload: {payload!r}")
    try:
        TaskEvaluation.model_validate(payload)
    except ValidationError as exc:
        print("\nValidationError raised:")
        print(exc)
        return 0
    raise AssertionError("Reproduction failed: invalid task evaluation unexpectedly parsed.")


if __name__ == "__main__":
    raise SystemExit(main())
