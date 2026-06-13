# https://github.com/crewAIInc/crewAI/issues/316

# Issue 316 Reproduction

Source issue: `crewAIInc/crewAI#316`

## Reproduction Type

This is a minimal reproduction.

The bug is an argument-shape mismatch between the CrewAI tool wrapper and the
DuckDuckGo search backend. No external service is required to reproduce the
failure.

## Bug

The issue reports that the tool receives `{"q": "..."}` but the underlying
search runner is invoked as if `q` were a keyword argument. That causes:

```text
TypeError: DuckDuckGoSearchRun._run() got an unexpected keyword argument 'q'
```

## Environment

- Python 3.12 or newer
- No network access required

## Reproduction Steps

1. Open the reproduction directory:

   ```bash
   cd crewai-issue-316
   ```

2. Run the script:

   ```bash
   python reproduce.py
   ```

## Expected Result

If the wrapper forwarded the query correctly, the search backend would receive
the string query and return search results.

## Actual Result

The buggy path raises a `TypeError`, then the fixed path shows the intended
behavior:

```text
Buggy dispatch error:
...

Fixed dispatch result:
search results for 'AI news latest not older than 1 day'
```

## Why This Is Minimal

The reproduction keeps only the broken boundary:

- one tool input dict
- one wrapper that mis-forwards `q`
- one backend function that expects a positional string

