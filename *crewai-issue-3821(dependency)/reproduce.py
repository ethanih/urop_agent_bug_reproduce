#!/usr/bin/env python3
"""Minimal reproduction for crewAI issue #3821."""

from pydantic import BaseModel, field_validator


class LabelOutput(BaseModel):
    label: str

    @field_validator("label")
    @classmethod
    def check_label(cls, value: str) -> str:
        if value not in {"billing", "support"}:
            raise Exception(f"Invalid label: {value}")
        return value


def buggy_retry_loop(candidates):
    for attempt, candidate in enumerate(candidates, start=1):
        print(f"Attempt {attempt}: {candidate!r}")
        try:
            return LabelOutput.model_validate(candidate)
        except ValueError as exc:
            print(f"Retryable validation error: {exc}")
            continue


def main() -> int:
    candidates = [{"label": "wrong-label"}, {"label": "support"}]
    try:
        buggy_retry_loop(candidates)
    except Exception as exc:
        print("\nExecution stopped before retry:")
        print(exc)
        return 0
    raise AssertionError("Reproduction failed: retry loop unexpectedly recovered.")


if __name__ == "__main__":
    raise SystemExit(main())
