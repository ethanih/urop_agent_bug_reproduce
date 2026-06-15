# https://github.com/crewAIInc/crewAI/issues/3843

# Issue 3843 Reproduction

Source issue: `crewAIInc/crewAI#3843`

## Reproduction Type

This is a minimal reproduction.

The issue is an oversized tool-output budgeting failure. The script models a follow-up LLM request whose `max_tokens` becomes negative after a large tool result is inserted into context.

## Files

- `normalized_issue_summary.md`: stage A normalized issue facts
- `reproduce.py`: stage B reproduction

## Environment

- Python 3.10 or newer
- No network access required

## Reproduction Steps

1. Open the reproduction directory:

   ```bash
   cd crewai-issue-3843
   ```

2. Run the script:

   ```bash
   python reproduce.py
   ```

## Expected Result

The system should summarize or reject oversized tool output before constructing the follow-up LLM call.

## Actual Result

The computed `max_tokens` becomes negative and the simulated API request fails.
