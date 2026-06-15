# https://github.com/langchain-ai/langchain/issues/19699

# Issue 19699 Reproduction

Source issue: `langchain-ai/langchain#19699`

## Reproduction Type

This is a minimal reproduction.

The issue is a strict JSON parsing failure. A local script is enough to show why `{ datasource: "python_docs" }` cannot be parsed as JSON.

## Files

- `normalized_issue_summary.md`: stage A normalized issue facts
- `reproduce.py`: stage B reproduction

## Environment

- Python 3.10 or newer
- No network access required

## Reproduction Steps

1. Open the reproduction directory:

   ```bash
   cd langchain-issue-19699
   ```

2. Run the script:

   ```bash
   python reproduce.py
   ```

## Expected Result

The router output should parse into:

```json
{"datasource": "python_docs"}
```

## Actual Result

The invalid payload causes:

```text
JSONDecodeError: Expecting property name enclosed in double quotes
```
