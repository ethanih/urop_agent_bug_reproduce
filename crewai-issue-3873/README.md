# https://github.com/crewAIInc/crewAI/issues/3873

# Issue 3873 Reproduction

Source issue: `crewAIInc/crewAI#3873`

## Reproduction Type

This is a minimal reproduction.

The visible bug is that the final answer leaks internal reasoning fields. That can be modeled locally without a real database or multi-agent runtime.

## Files

- `normalized_issue_summary.md`: stage A normalized issue facts
- `reproduce.py`: stage B reproduction

## Environment

- Python 3.10 or newer
- No network access required

## Reproduction Steps

1. Open the reproduction directory:

   ```bash
   cd crewai-issue-3873
   ```

2. Run the script:

   ```bash
   python reproduce.py
   ```

## Expected Result

The final response should be a user-facing error summary or fallback answer without internal scratchpad fields.

## Actual Result

The final answer includes `Thought:` and `Action:` lines that should have remained internal.
