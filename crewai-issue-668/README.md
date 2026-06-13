# https://github.com/crewAIInc/crewAI/issues/668

# Issue 668 Reproduction

Source issue: `crewAIInc/crewAI#668`

## Reproduction Type

This is a minimal reproduction.

The crash comes from unsafe `None.startswith(...)` handling, which can be shown
with a tiny Python script.

## Bug

The issue reports:

```text
'NoneType' object has no attribute 'startswith'
```

## Environment

- Python 3.12 or newer
- No network access required

## Reproduction Steps

1. Open the reproduction directory:

   ```bash
   cd crewai-issue-668
   ```

2. Run the script:

   ```bash
   python reproduce.py
   ```

## Expected Result

The tool-name check should treat `None` as a missing value and continue safely.

## Actual Result

The buggy path raises `AttributeError`:

```text
Buggy tool-name check error:
'NoneType' object has no attribute 'startswith'
```

## Why This Is Minimal

The reproduction keeps only:

- one nullable tool name
- one unsafe prefix check
- one guarded fix path

