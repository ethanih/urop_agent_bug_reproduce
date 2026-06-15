# https://github.com/langchain-ai/langchain/issues/33504

# Issue 33504 Reproduction

Source issue: `langchain-ai/langchain#33504`

## Reproduction Type

This is a minimal reproduction.

The bug is routing logic that ignores `invalid_tool_calls`, so a local mock is enough.

## Files

- `normalized_issue_summary.md`: stage A normalized issue facts
- `reproduce.py`: stage B reproduction

## Environment

- Python 3.10 or newer
- No network access required

## Reproduction Steps

1. Open the reproduction directory:

   ```bash
   cd langchain-issue-33504
   ```

2. Run the script:

   ```bash
   python reproduce.py
   ```

## Expected Result

The agent should continue after the malformed tool call and surface the error to a later step.

## Actual Result

The routing logic exits immediately because `tool_calls` is empty, even though `invalid_tool_calls` is present.
