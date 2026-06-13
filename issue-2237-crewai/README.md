# https://github.com/crewAIInc/crewAI/issues/2237

# Issue 2237 Reproduction

Source issue: `crewAIInc/crewAI#2237`

## Bug

The issue reports that crewAI cannot parse an LLM response when the response
contains both:

- an `Action` block
- a `Final Answer`

The parser treats that as an invalid mixed-format output and raises:

```text
Error parsing LLM output, agent will retry: I did it wrong. Tried to both perform Action and give a Final Answer at the same time, I must do one or the other
```

## Environment

This reproduction is a plain Python script and does not require network access
or a real LLM call.

- Python: any modern Python 3 version
- OS: any

## Reproduction Steps

1. Create or enter the reproduction directory.
2. Run the script:

   ```bash
   python reproduce.py
   ```

## Expected Result

If the parser accepted the mixed output, it would parse the response normally.

## Actual Result

The script prints the parser error and shows that the mixed output is rejected:

```text
Parser error:
Error parsing LLM output, agent will retry: I did it wrong. Tried to both perform Action and give a Final Answer at the same time, I must do one or the other
```

## Why This Is Minimal

The reproduction keeps only the essential failure condition:

- one response string
- one strict parser
- one invalid combination: `Action` plus `Final Answer`

That is enough to reproduce the issue without involving any external tools or
real crewAI execution.
