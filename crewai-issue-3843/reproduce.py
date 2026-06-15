#!/usr/bin/env python3
"""Minimal reproduction for crewAI issue #3843."""


def build_followup_request(context_limit: int, prompt_tokens: int, tool_output_tokens: int):
    remaining = context_limit - prompt_tokens - tool_output_tokens
    if remaining < 1:
        raise ValueError(f"custom error: max_tokens must be at least 1, got {remaining}.")
    return {"max_tokens": remaining}


def main() -> int:
    context_limit = 128_000
    prompt_tokens = 4_559
    tool_output_tokens = 928_000
    print(
        f"context_limit={context_limit}, prompt_tokens={prompt_tokens}, "
        f"tool_output_tokens={tool_output_tokens}"
    )
    try:
        build_followup_request(context_limit, prompt_tokens, tool_output_tokens)
    except ValueError as exc:
        print("\nSimulated API failure:")
        print(exc)
        return 0
    raise AssertionError("Reproduction failed: oversized tool output unexpectedly fit.")


if __name__ == "__main__":
    raise SystemExit(main())
