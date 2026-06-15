# https://github.com/crewAIInc/crewAI/issues/3821

# Issue 3821 Reproduction

Source issue: `crewAIInc/crewAI#3821`

## Reproduction Type

This is a minimal reproduction with a real Pydantic dependency.

The issue is not about a specific remote model. It is about what happens when a field validator raises during structured output validation and the retry loop does not handle it correctly.

## Files

- `normalized_issue_summary.md`: stage A normalized issue facts
- `reproduce.py`: stage B reproduction
- `requirements.txt`: minimal dependency set

## Environment

- Python 3.10 or newer

## Reproduction Steps

1. Open the reproduction directory:

   ```bash
   cd crewai-issue-3821
   ```

2. Create and activate a virtual environment:

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. Install dependencies:

   ```bash
   python -m pip install -r requirements.txt
   ```

4. Run the script:

   ```bash
   python reproduce.py
   ```

## Expected Result

When validation fails, the system should retry with a new output candidate.

## Actual Result

The validator raises a raw exception, the buggy retry loop does not retry, and execution stops on the first bad value.
