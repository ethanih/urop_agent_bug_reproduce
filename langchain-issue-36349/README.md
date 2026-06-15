# https://github.com/langchain-ai/langchain/issues/36349

# Issue 36349 Reproduction

Source issue: `langchain-ai/langchain#36349`

## Reproduction Type

This is a minimal reproduction.

The issue is a missing error path when no structured-output tool call is emitted.

## Files

- `normalized_issue_summary.md`: stage A normalized issue facts
- `reproduce.py`: stage B reproduction

## Environment

- Python 3.10 or newer
- No network access required

## Reproduction Steps

1. Open the reproduction directory:

   ```bash
   cd langchain-issue-36349
   ```

2. Run the script:

   ```bash
   python reproduce.py
   ```

## Expected Result

The no-tool-call case should raise a structured-output error.

## Actual Result

The response returns without `structured_response` and without an exception.
