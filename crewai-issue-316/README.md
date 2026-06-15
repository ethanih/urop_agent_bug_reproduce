# https://github.com/crewAIInc/crewAI/issues/316

# Issue 316 Reproduction

Source issue: `crewAIInc/crewAI#316`

## Reproduction Type

This is a minimal reproduction.

The issue is an argument-shape mismatch between the CrewAI tool wrapper and the DuckDuckGo search backend. The failure happens before any real search request is needed, so a local script is enough.

## Files

- `normalized_issue_summary.md`: stage A normalized issue facts
- `reproduce.py`: stage B reproduction

## Environment

- Python 3.10 or newer
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

The wrapper should forward the search query in the backend's expected shape and return search results.

## Actual Result

The buggy path forwards `{"q": ...}` as keyword arguments and raises:

```text
TypeError: duckduckgo_search_run() got an unexpected keyword argument 'q'
```

## Reproduction Type Label

最小化复现
