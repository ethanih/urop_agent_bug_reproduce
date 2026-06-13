# https://github.com/langchain-ai/langchain/issues/1358

# Issue 1358 Reproduction

Source issue: `langchain-ai/langchain#1358`

## Bug

The issue describes a LangChain agent configured with
`conversational-react-description` receiving a normal conversational answer
from the model. The agent's output parser expects ReAct-style text, so it fails
with:

```text
Could not parse LLM output
```

## Why This Is Minimal

The reproduction does not need a full agent or a real model call. The key
problem is the contract mismatch:

- the model output is plain chat text
- the parser expects `Action:` / `Action Input:` or `Final Answer:`

## Environment

- Python 3.12 or newer
- No external services required

## Reproduction Steps

1. Create a virtual environment:

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

2. Run the script:

   ```bash
   python reproduce.py
   ```

## Expected Result

If the agent/parser accepted plain conversational text, the output would parse
successfully instead of failing.

## Actual Result

The script prints the parser error and shows that the mixed output is rejected:

```text
LLM output:
Sure, I can help with that. Let me think for a second.

Parser error:
Could not parse LLM output
```

## Notes

- This is a logic-level reproduction of the parser mismatch.
- This MRE intentionally avoids external network calls and does not require the
  real LangChain package.
