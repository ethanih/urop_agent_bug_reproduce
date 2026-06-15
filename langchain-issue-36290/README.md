# https://github.com/langchain-ai/langchain/issues/36290

# Issue 36290 Reproduction

Source issue: `langchain-ai/langchain#36290`

## Reproduction Type

This is a minimal reproduction.

The bug is a local content-aggregation problem.

## Files

- `normalized_issue_summary.md`: stage A normalized issue facts
- `reproduce.py`: stage B reproduction

## Environment

- Python 3.10 or newer
- No network access required

## Reproduction Steps

1. Open the reproduction directory:

   ```bash
   cd langchain-issue-36290
   ```

2. Run the script:

   ```bash
   python reproduce.py
   ```

## Expected Result

The parser should use the correct phase and successfully parse one JSON object.

## Actual Result

Two JSON strings are combined and `json.loads` fails with `Extra data`.
