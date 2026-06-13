# https://github.com/langchain-ai/langchain/issues/2276

# Issue 2276 Reproduction

Source issue: `langchain-ai/langchain#2276`

## Reproduction Type

This is a minimal reproduction.

The failure is an invalid JSON / recovery-path bug. A tiny JSON parser is
enough to show the problem.

## Bug

The issue reports an exception when the conversation agent does not receive the
expected JSON output.

## Environment

- Python 3.12 or newer
- No network access required

## Reproduction Steps

1. Open the reproduction directory:

   ```bash
   cd langchain-issue-2276
   ```

2. Run the script:

   ```bash
   python reproduce.py
   ```

## Expected Result

The agent should recover from the invalid tool response instead of crashing.

## Actual Result

The buggy path parses the response strictly and then the fixed path converts it
into a final-answer fallback.

## Why This Is Minimal

The reproduction keeps only:

- one invalid tool response
- one strict JSON parser
- one fallback handler

