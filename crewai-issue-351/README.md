# https://github.com/crewAIInc/crewAI/issues/351

# Issue 351 Reproduction

Source issue: `crewAIInc/crewAI#351`

## Reproduction Type

This is a minimal reproduction.

The reported failure is a delegation lookup bug. The observable symptom can be
reproduced with a small in-memory roster, without running a full crewAI stack or
connecting to an LLM.

## Bug

The issue reports that the coworker name is correct, but the delegation flow
still says the coworker is not found.

## Environment

- Python 3.12 or newer
- No network access required

## Reproduction Steps

1. Open the reproduction directory:

   ```bash
   cd crewai-issue-351
   ```

2. Run the script:

   ```bash
   python reproduce.py
   ```

## Expected Result

The coworker should be resolved from the crew roster.

## Actual Result

The buggy lookup fails against the wrong roster scope:

```text
Buggy delegation lookup:
Co-worker mentioned not found, it must to be one of the following options: ['Planner']
```

## Why This Is Minimal

The reproduction keeps only:

- the requested coworker name
- a small crew roster
- the bad lookup scope

