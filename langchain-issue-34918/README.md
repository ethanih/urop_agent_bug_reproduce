# https://github.com/langchain-ai/langchain/issues/34918

# Issue 34918 Reproduction

Source issue: `langchain-ai/langchain#34918`

## Reproduction Type

This is a real-dependency reproduction.

The full bug depends on Ollama streaming behavior, but the included script reproduces the exact empty-stream aggregation boundary locally and can be adapted to the real stack.

## Files

- `normalized_issue_summary.md`: stage A normalized issue facts
- `reproduce.py`: stage B reproduction

## Environment

- Python 3.11 or newer
- Full reproduction requires an Ollama-backed async agent stack

## Reproduction Steps

1. Open the reproduction directory:

   ```bash
   cd langchain-issue-34918
   ```

2. Run the local approximation:

   ```bash
   python reproduce.py
   ```

## Expected Result

The stream aggregation path should either handle an empty stream gracefully or raise a more structured provider error.

## Actual Result

The aggregation path raises `ValueError: No data received from Ollama stream.`

## Missing Information / Limits

The issue does not include a fully isolated Ollama-only script. The included repro focuses on the exact empty-stream boundary that matches the traceback.
