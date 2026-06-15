# https://github.com/crewAIInc/crewAI/issues/3925

# Issue 3925 Reproduction

Source issue: `crewAIInc/crewAI#3925`

## Reproduction Type

This is a real-dependency reproduction.

The issue is fundamentally about live LLM behavior in CrewAI hierarchical delegation. A deterministic local mock would not faithfully capture the English-vs-Japanese divergence, so this directory provides a runnable real-stack reproduction harness instead.

## Files

- `normalized_issue_summary.md`: stage A normalized issue facts
- `reproduce.py`: stage B reproduction harness

## Environment

- Python 3.10 or newer
- `crewai==1.5.0`
- A valid OpenAI-compatible API key if you want to reproduce the live model behavior

## API Key Placeholder

Leave the key blank until you supply your own value:

```bash
export OPENAI_API_KEY=
```

## Reproduction Steps

1. Open the reproduction directory:

   ```bash
   cd crewai-issue-3925
   ```

2. Create and activate a virtual environment:

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. Install CrewAI and its dependencies:

   ```bash
   python -m pip install "crewai==1.5.0"
   ```

4. Set your API key:

   ```bash
   export OPENAI_API_KEY=
   ```

5. Run the script:

   ```bash
   python reproduce.py
   ```

## Expected Result

The English and Japanese versions should produce similar delegation behavior because they describe the same workflow.

## Actual Result

According to the issue report, the English version delegates to the correct coworker, while the Japanese version may self-delegate or answer without consulting the coworker.

## Limitation

This issue depends on live model behavior. The repository intentionally leaves the API key blank and does not ship a fake key.
