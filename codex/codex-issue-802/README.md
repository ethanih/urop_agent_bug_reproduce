# https://github.com/openai/codex/issues/802

# Issue 802 Reproduction

Source issue: `openai/codex#802`

## Reproduction Type

This is a minimal reproduction.

The script captures the exact visible behavior from the issue:

- a change is proposed
- the proposal is shown
- the file on disk remains unchanged

## Environment

- Python 3.10 or newer
- No external services required

## Files

- `normalized_issue_summary.md`: stage A normalized issue facts
- `reproduce.py`: stage B reproduction

## Reproduction Steps

1. Open the reproduction directory:

   ```bash
   cd codex/codex-issue-802
   ```

2. Run the script:

   ```bash
   python reproduce.py
   ```

## Expected Result

If the suggestion were applied, the file content would change from `before` to
`after`.

## Actual Result

```text
Original file content:
before

Suggested content:
after

Actual file content after suggestion-only flow:
before
```

The missing apply step is the reproduced bug.
