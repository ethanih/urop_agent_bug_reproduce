# https://github.com/langchain-ai/langchain/issues/32977

# Issue 32977 Reproduction

Source issue: `langchain-ai/langchain#32977`

## Reproduction Type

This is a real-dependency reproduction.

The exact behavior depends on OpenAI/OpenRouter HTTP parsing and retry timing. The script defaults to a local approximation of the same failure boundary and can be adapted to the real client path.

## Files

- `normalized_issue_summary.md`: stage A normalized issue facts
- `reproduce.py`: stage B reproduction

## Environment

- Python 3.11 or newer
- Full reproduction requires provider access and a model/client path that can return malformed JSON

## Reproduction Steps

1. Open the reproduction directory:

   ```bash
   cd langchain-issue-32977
   ```

2. Run the local approximation:

   ```bash
   python reproduce.py
   ```

## Expected Result

When `include_raw=True`, callers should still get the raw payload or attached raw bytes even if JSON parsing fails.

## Actual Result

The parse error is raised first, raw content is lost from the public result, and retries can add visible delay.

## Missing Information / Limits

The issue does not include a deterministic upstream malformed-response fixture, so the included script reproduces the same failure boundary locally rather than the full provider exchange.
