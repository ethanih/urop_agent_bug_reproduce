# https://github.com/crewAIInc/crewAI/issues/2288

# Issue 2288 Reproduction

Source issue: `crewAIInc/crewAI#2288`

## Reproduction Type

This is a minimal reproduction.

The bug is an input-shape bug in the tool callback path. A small payload is
enough to show the wrong nested structure.

## Bug

The issue reports that a tool input can be passed in the wrong shape, for
example:

```text
[{"ticker": "VST"}, {"tool_code": "Stock Info", "tool_input": {"ticker": "VST"}}]
```

instead of the expected:

```text
{"ticker": "VST"}
```

## Environment

- Python 3.12 or newer
- No network access required

## Reproduction Steps

1. Open the reproduction directory:

   ```bash
   cd crewai-issue-2288
   ```

2. Run the script:

   ```bash
   python reproduce.py
   ```

## Expected Result

The tool input should be normalized to a single argument dict.

## Actual Result

The buggy path keeps the nested list shape:

```text
Buggy extracted tool input:
[{'ticker': 'VST'}, {'tool_code': 'Stock Info', 'tool_input': {'ticker': 'VST'}}]
```

## Why This Is Minimal

The reproduction keeps only:

- one callback payload
- one nested `tool_input` shape
- one normalization function

