# https://github.com/langchain-ai/langchain/issues/2252

# Issue 2252 Reproduction V2

Source issue: `langchain-ai/langchain#2252`

## Reproduction Type

This is a minimal reproduction.

The normalized summary shows that the visible bug occurs before real pandas execution: the agent chooses the wrong tool name. That makes a local tool-name validator sufficient.

## Files

- `normalized_issue_summary.md`: stage A normalized issue facts
- `reproduce.py`: stage B reproduction

## Environment

- Python 3.12 or newer
- No network access required

## Reproduction Steps

1. Open the reproduction directory:

   ```bash
   cd langchain-issue-2252
   ```

2. Run the script:

   ```bash
   python reproduce.py
   ```

## Expected Result

Both dataframe questions should map to the exact tool name `python_repl_ast`.

## Actual Result

The second question produces a descriptive sentence instead of the exact tool name, and the validator rejects it as an invalid tool.
