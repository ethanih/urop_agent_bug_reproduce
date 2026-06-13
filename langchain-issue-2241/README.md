# https://github.com/langchain-ai/langchain/issues/2241

# Issue 2241 Reproduction

Source issue: `langchain-ai/langchain#2241`

## Reproduction Type

This is a minimal reproduction.

The failure is a parser bug caused by nested markdown code fences. A small
string-based parser is enough to reproduce it.

## Bug

The issue reports that a multi-line markdown code block can break the
`conversational_chat` agent response parsing.

## Environment

- Python 3.12 or newer
- No network access required

## Reproduction Steps

1. Open the reproduction directory:

   ```bash
   cd langchain-issue-2241
   ```

2. Run the script:

   ```bash
   python reproduce.py
   ```

## Expected Result

The agent response should be parsed even if the payload contains an inner code
block.

## Actual Result

The buggy parser returns only the truncated JSON payload extracted from the
outer fence.

## Why This Is Minimal

The reproduction keeps only:

- one markdown response string
- one naive fence splitter
- one fixed parser path

