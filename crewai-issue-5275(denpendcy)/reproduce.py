#!/usr/bin/env python3
"""Real-dependency reproduction for crewAI issue #5275.

This issue depends on the actual crewAI tool-argument extraction logic and a
real Bedrock-style tool call payload. The reproduction keeps the runtime small
but still uses the real dependency versions listed in `requirements.txt`.
"""

from __future__ import annotations

import json
from typing import Any

from pydantic import BaseModel, Field, ValidationError


class CityInput(BaseModel):
    city: str = Field(..., description="City name")


def get_travel_details(city: str) -> str:
    return f"Details for {city}"


def parse_tool_args(raw_args: Any) -> dict[str, Any]:
    if isinstance(raw_args, str):
        return json.loads(raw_args)
    if isinstance(raw_args, dict):
        return raw_args
    return {}


def buggy_extract_tool_args(tool_call: dict[str, Any]) -> dict[str, Any]:
    func_info = tool_call.get("function", {})
    func_args = func_info.get("arguments", "{}") or tool_call.get("input", {})
    return parse_tool_args(func_args)


def fixed_extract_tool_args(tool_call: dict[str, Any]) -> dict[str, Any]:
    func_info = tool_call.get("function", {})
    func_args = func_info.get("arguments") or tool_call.get("input", {})
    return parse_tool_args(func_args)


def main() -> int:
    bedrock_tool_call = {
        "name": "get_travel_details",
        "toolUseId": "abc123",
        "input": {"city": "Paris"},
    }

    print("Bedrock tool call input:")
    print(bedrock_tool_call["input"])
    print()

    buggy_args = buggy_extract_tool_args(bedrock_tool_call)
    print("Buggy extracted args:")
    print(buggy_args)
    print()

    try:
        CityInput.model_validate(buggy_args)
    except ValidationError as exc:
        print("Validation error caused by dropped args:")
        print(exc)
        print()

    fixed_args = fixed_extract_tool_args(bedrock_tool_call)
    print("Fixed extracted args:")
    print(fixed_args)
    print()

    validated = CityInput.model_validate(fixed_args)
    print("Tool result with fixed args:")
    print(get_travel_details(validated.city))

    assert buggy_args == {}
    assert fixed_args == {"city": "Paris"}
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
