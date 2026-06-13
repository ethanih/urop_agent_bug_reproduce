# https://github.com/openai/codex/issues/802

# Issue 802 Reproduction

Source issue: `openai/codex#802`

## Bug

The issue describes a workflow where Codex suggests changes, but those changes
do not end up applied to the filesystem.

This reproduction models that behavior with a minimal Python script:

- create a temporary file
- generate a suggested replacement
- print the suggestion
- intentionally skip the write/apply step
- verify the file still contains the original content

## Why This Is Minimal

The script does not depend on Codex internals or a real patch engine. It only
captures the observable failure:

- a change is proposed
- the proposal is visible
- the file on disk remains unchanged

## Environment

- Python 3.12 or newer
- No external services required

## Reproduction Steps

1. Create a virtual environment:

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
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

## Notes

- The `apply_change(...)` function exists only to show the missing step.
- It is intentionally not called, because the reproduction is about the broken
  suggestion-only path.
