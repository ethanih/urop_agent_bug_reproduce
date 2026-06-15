# https://github.com/langchain-ai/langchain/issues/33116

# Issue 33116 Reproduction

Source issue: `langchain-ai/langchain#33116`

## Reproduction Type

This is a real-dependency reproduction.

The issue report says the failure is specific to `ChatOllama(model="gpt-oss:20b")`. The included script is runnable in two modes:

- default: a local approximation of the failing parse boundary
- real mode: the actual Ollama-based reproduction path

## Files

- `normalized_issue_summary.md`: stage A normalized issue facts
- `reproduce.py`: stage B reproduction

## Environment

- Python 3.12 or newer
- Real reproduction requires a local Ollama server with `gpt-oss:20b`

## Reproduction Steps

1. Open the reproduction directory:

   ```bash
   cd langchain-issue-33116
   ```

2. Run the local approximation:

   ```bash
   python reproduce.py
   ```

3. For the real provider path, install the needed packages and run with real mode enabled:

   ```bash
   pip install langchain-ollama langchain-core pydantic
   USE_REAL_OLLAMA=1 python reproduce.py
   ```

## Expected Result

Structured output should parse into a `Joke` object.

## Actual Result

The parser receives non-JSON output and fails with a JSON parsing error wrapped as an output parsing failure.

## Missing Information / Limits

The exact malformed provider payload is not included in the issue, so the default mode reproduces the same parser boundary with a synthetic non-JSON response. The full issue behavior still depends on real Ollama `gpt-oss:20b`.
