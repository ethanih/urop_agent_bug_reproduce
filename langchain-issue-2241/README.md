# https://github.com/langchain-ai/langchain/issues/2241

# Issue 2241 Reproduction V2

Source issue: `langchain-ai/langchain#2241`

## Reproduction Type

This is a minimal reproduction.

The normalized summary isolates a pure delimiter-collision bug, so the smallest reproduction is a single nested-fence response string plus a naive parser.

## Files

- `normalized_issue_summary.md`: stage A normalized issue facts
- `reproduce.py`: stage B reproduction

## Environment

- Python 3.12 or newer
- No network access required

## Reproduction Steps

1. Open the reproduction directory:

   ```bash
   cd langchain-issue-2241
   ```

2. Run the script:

   ```bash
   python reproduce.py
   ```

## Expected Result

The parser should preserve the full JSON payload, including the inner code block inside `action_input`.

## Actual Result

The buggy parser truncates the payload at the nested fenced code block.
