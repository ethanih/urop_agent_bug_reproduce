# https://github.com/langchain-ai/langchain/issues/2252

# Issue 2252 Reproduction

Source issue: `langchain-ai/langchain#2252`

## Reproduction Type

This is a minimal reproduction.

The issue is about inconsistent tool selection in the dataframe agent. A small
question classifier is enough to show the buggy behavior.

## Bug

The issue reports that `python_repl_ast` is not called consistently.

## Environment

- Python 3.12 or newer
- No network access required

## Reproduction Steps

1. Open the reproduction directory:

   ```bash
   cd langchain-issue-2252
   ```

2. Run the script:

   ```bash
   python reproduce.py
   ```

## Expected Result

Questions that require dataframe inspection should route to `python_repl_ast`.

## Actual Result

The buggy path handles one phrasing but misses a similar query:

```text
Buggy tool decision:
False
```

## Why This Is Minimal

The reproduction keeps only:

- two representative questions
- one buggy routing rule
- one corrected routing rule

