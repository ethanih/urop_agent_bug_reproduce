# https://github.com/crewAIInc/crewAI/issues/2383

# Issue 2383 Reproduction

Source issue: `crewAIInc/crewAI#2383`

## Reproduction Type

This is a minimal reproduction.

The issue is about tool-dispatch logic when a model returns text instead of an
explicit tool call. A tiny in-memory model output is enough to show the bug.

## Bug

The issue reports that some models do not call custom tools at all.

## Environment

- Python 3.12 or newer
- No network access required

## Reproduction Steps

1. Open the reproduction directory:

   ```bash
   cd crewai-issue-2383
   ```

2. Run the script:

   ```bash
   python reproduce.py
   ```

## Expected Result

The tool-dispatch layer should route the request into the custom tool's `_run`
method.

## Actual Result

The buggy path skips the tool because it only looks for explicit tool calls:

```text
Buggy tool-dispatch decision:
False
```

## Why This Is Minimal

The reproduction keeps only:

- one model output
- one dispatch predicate
- one missing tool-call branch

