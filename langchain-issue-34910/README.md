# https://github.com/langchain-ai/langchain/issues/34910

# Issue 34910 Reproduction

Source issue: `langchain-ai/langchain#34910`

## Reproduction Type

This is a minimal reproduction.

The failure is a local parser lookup bug.

## Files

- `normalized_issue_summary.md`: stage A normalized issue facts
- `reproduce.py`: stage B reproduction

## Environment

- Python 3.10 or newer
- No network access required

## Reproduction Steps

1. Open the reproduction directory:

   ```bash
   cd langchain-issue-34910
   ```

2. Run the script:

   ```bash
   python reproduce.py
   ```

## Expected Result

With `partial=True`, unknown tools should be skipped or tolerated.

## Actual Result

The parser performs a direct lookup and raises `KeyError` for the unregistered tool.
