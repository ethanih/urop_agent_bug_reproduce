# https://github.com/langchain-ai/langchain/issues/33995

# Issue 33995 Reproduction

Source issue: `langchain-ai/langchain#33995`

## Reproduction Type

This is a real-dependency reproduction.

The bug depends on Groq request semantics and intermittent model behavior. The script defaults to a local approximation, and also includes the real Groq path.

## Files

- `normalized_issue_summary.md`: stage A normalized issue facts
- `reproduce.py`: stage B reproduction

## Environment

- Python 3.11 or newer
- Full reproduction requires `GROQ_API_KEY`

## Reproduction Steps

1. Open the reproduction directory:

   ```bash
   cd langchain-issue-33995
   ```

2. Run the local approximation:

   ```bash
   python reproduce.py
   ```

3. For the real provider path:

   ```bash
   pip install langchain-groq pydantic python-dotenv
   GROQ_API_KEY=... USE_REAL_GROQ=1 python reproduce.py
   ```

## Expected Result

If the model returns schema-valid JSON, the structured-output path should either parse it or not require a tool call.

## Actual Result

The provider rejects the request with `tool_use_failed` because a tool call was required but not emitted.

## Missing Information / Limits

The issue says the failure is intermittent. The default script reproduces the contract mismatch deterministically; the real provider path is needed for the exact upstream behavior.
