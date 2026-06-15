# https://github.com/langchain-ai/langchain/issues/12077

# Issue 12077 Reproduction

Source issue: `langchain-ai/langchain#12077`

## Reproduction Type

This is a minimal reproduction.

The visible bug is that the SQL string still contains the prompt label `SQLQuery:` when it reaches the executor. That can be demonstrated locally without Snowflake or Bedrock.

## Files

- `normalized_issue_summary.md`: stage A normalized issue facts
- `reproduce.py`: stage B reproduction

## Environment

- Python 3.10 or newer
- No network access required

## Reproduction Steps

1. Open the reproduction directory:

   ```bash
   cd langchain-issue-12077
   ```

2. Run the script:

   ```bash
   python reproduce.py
   ```

## Expected Result

The executor should receive:

```text
SELECT top 5 ...
```

## Actual Result

The executor receives:

```text
SQLQuery:
SELECT top 5 ...
```

and rejects it as invalid SQL input.
