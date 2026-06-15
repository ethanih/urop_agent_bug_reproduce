# https://github.com/langchain-ai/langchain/issues/35990

# Issue 35990 Reproduction

Source issue: `langchain-ai/langchain#35990`

## Reproduction Type

This is a minimal reproduction.

The failure is a local classification bug for tool-call arguments.

## Files

- `normalized_issue_summary.md`: stage A normalized issue facts
- `reproduce.py`: stage B reproduction

## Environment

- Python 3.10 or newer
- No network access required

## Reproduction Steps

1. Open the reproduction directory:

   ```bash
   cd langchain-issue-35990
   ```

2. Run the script:

   ```bash
   python reproduce.py
   ```

## Expected Result

Non-dict JSON arguments should become `invalid_tool_calls`.

## Actual Result

If they are treated as valid tool calls, the message contract is violated.
