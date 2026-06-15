# https://github.com/langchain-ai/langchain/issues/11408

# Issue 11408 Reproduction

Source issue: `langchain-ai/langchain#11408`

## Reproduction Type

This is a minimal reproduction.

The reported failure is caused by strict boolean parsing. A local script is enough to show that an LLM-style response such as `Yes, ...` is rejected even though it is clearly affirmative.

## Files

- `normalized_issue_summary.md`: stage A normalized issue facts
- `reproduce.py`: stage B reproduction

## Environment

- Python 3.10 or newer
- No network access required

## Reproduction Steps

1. Open the reproduction directory:

   ```bash
   cd langchain-issue-11408
   ```

2. Run the script:

   ```bash
   python reproduce.py
   ```

## Expected Result

A relevance filter should accept an affirmative response and continue with document filtering.

## Actual Result

The parser rejects the response because it is not exactly `YES` or `NO`:

```text
Parser raised:
BooleanOutputParser expected output value to either be YES or NO. Received Yes, the context is relevant to the question.
```
