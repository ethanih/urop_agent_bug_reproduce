# https://github.com/crewAIInc/crewAI/issues/620

# Issue 620 Reproduction

Source issue: `crewAIInc/crewAI#620`

## Reproduction Type

This is a minimal reproduction.

The failure is a coworker-resolution bug in the orchestration logic. The issue
mentions a local LLM, but the core symptom can be reproduced with an in-memory
lookup against the wrong worker list.

## Bug

The issue reports:

```text
Error executing tool. Co-worker mentioned not found
```

even though the coworker name is valid.

## Environment

- Python 3.12 or newer
- No network access required

## Reproduction Steps

1. Open the reproduction directory:

   ```bash
   cd crewai-issue-620
   ```

2. Run the script:

   ```bash
   python reproduce.py
   ```

## Expected Result

The coworker should be resolved and the task should be delegated.

## Actual Result

The buggy path rejects the valid coworker name:

```text
Buggy delegation result:
Error executing tool. Co-worker mentioned not found, it must to be one of the following options: []
```

## Why This Is Minimal

The reproduction keeps only:

- the coworker name from the task payload
- a crew roster
- the bad lookup scope

