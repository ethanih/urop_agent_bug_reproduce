# https://github.com/langchain-ai/langchain/issues/21482

# Issue 21482 Reproduction

Source issue: `langchain-ai/langchain#21482`

## Reproduction Type

This is a minimal reproduction.

The issue is a response-contract mismatch: code expects `raw_schema.content`, but gets a plain string. That can be shown without Bedrock or Neo4j.

## Files

- `normalized_issue_summary.md`: stage A normalized issue facts
- `reproduce.py`: stage B reproduction

## Environment

- Python 3.10 or newer
- No network access required

## Reproduction Steps

1. Open the reproduction directory:

   ```bash
   cd langchain-issue-21482
   ```

2. Run the script:

   ```bash
   python reproduce.py
   ```

## Expected Result

The transformer should read model output content and continue parsing graph data.

## Actual Result

It receives a plain string and raises:

```text
AttributeError: 'str' object has no attribute 'content'
```
