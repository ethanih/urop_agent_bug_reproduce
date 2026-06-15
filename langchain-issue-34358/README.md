# https://github.com/langchain-ai/langchain/issues/34358

# Issue 34358 Reproduction

Source issue: `langchain-ai/langchain#34358`

## Reproduction Type

This is a minimal reproduction.

The failure is a direct `dict` access bug in middleware response handling.

## Files

- `normalized_issue_summary.md`: stage A normalized issue facts
- `reproduce.py`: stage B reproduction

## Environment

- Python 3.10 or newer
- No network access required

## Reproduction Steps

1. Open the reproduction directory:

   ```bash
   cd langchain-issue-34358
   ```

2. Run the script:

   ```bash
   python reproduce.py
   ```

## Expected Result

Middleware should report an invalid selector response instead of crashing.

## Actual Result

The code accesses `response["tools"]` unconditionally and raises `KeyError`.
