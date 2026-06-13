# https://github.com/openai/codex/issues/666

# Issue 666 Reproduction

Source issue: `openai/codex#666`

## Bug

The issue reports that Codex can generate a patch-like suggestion in the
assistant message, but the change is not actually applied.

This MRE reproduces that behavior without depending on Codex itself:

- create a temporary file
- generate a suggested patch
- print the patch suggestion
- intentionally skip the apply step
- verify that the file content stays unchanged

## Environment

- Python 3.12 or newer
- No network access required
- No external services required

## Reproduction Steps

1. Open the reproduction directory:

   ```bash
   cd issue-666-codex
   ```

2. Create a virtual environment if you want an isolated Python runtime:

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. Run the MRE:

   ```bash
   python reproduce.py
   ```

## Expected Result

If the suggestion were correctly applied, the temporary file would change from
`before` to `after`.

## Actual Result

The script prints the suggestion but leaves the file unchanged:

```text
Original file content:
before

Suggested patch content:
after

Actual file content after suggestion-only flow:
before
```

## Why This Is Minimal

This reproduction keeps only the failure mechanism:

- one temporary file
- one generated patch suggestion
- one missing apply step

That is enough to reproduce the bug without pulling in a full frontend app or
Codex internals.
