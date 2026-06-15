# https://github.com/langchain-ai/langchain/issues/17352

# Issue 17352 Reproduction

Source issue: `langchain-ai/langchain#17352`

## Reproduction Type

This is a minimal reproduction.

The issue fails before any actual retrieval result is returned. The important part is the structured-output parsing mismatch, so this reproduction isolates that boundary.

## Files

- `normalized_issue_summary.md`: stage A normalized issue facts
- `reproduce.py`: stage B reproduction

## Environment

- Python 3.10 or newer
- No network access required

## Reproduction Steps

1. Open the reproduction directory:

   ```bash
   cd langchain-issue-17352
   ```

2. Run the script:

   ```bash
   python reproduce.py
   ```

## Expected Result

The query-generation stage should produce a structured list of alternate queries.

## Actual Result

The parser receives an `int` instead of the expected structured object and raises:

```text
ValidationError: LineList expected dict not int
```
