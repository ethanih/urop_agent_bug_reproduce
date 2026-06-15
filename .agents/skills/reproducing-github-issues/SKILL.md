---
name: reproducing-github-issues
description: Use when asked to turn a GitHub issue URL, raw issue text, or a normalized issue summary into a runnable bug reproduction repository or MRE
---

# Reproducing GitHub Issues

## Overview

Use a strict two-stage workflow for issue reproduction work:

1. Normalize the issue into a fixed summary.
2. Generate the reproduction only from that normalized summary.

If the input is a raw GitHub issue URL or raw issue text, never skip stage A.

## When to Use

Use this skill when the task is to:

- reproduce a bug from a GitHub issue
- turn an issue into an MRE
- build a minimal repro repo from issue text
- extract reproducible facts from noisy issue discussions

Do not use this skill for:

- general code review
- fixing an already-local bug without issue material
- summarizing issues without any reproduction goal

## Required Workflow

1. Determine the input type:
   - raw GitHub issue URL
   - raw issue text
   - normalized issue summary
2. If the input is raw, run stage A first.
3. If the input is already normalized, start from stage B.
4. Preserve the exact output structure defined in `prompt-template.md`.
5. Do not mix raw issue details back into stage B unless stage A captured them.

## Allowed Actions

- Inspect the normalized issue summary
- Inspect repo files, docs, and dependency manifests relevant to reproduction
- Create or edit reproduction artifacts only
- Run reproduction commands
- Record outcomes as `Fail`, `Pass`, or `Broken/Error`
- Finish only after at least one execution attempt

## Forbidden Actions

- Modifying application source code or core library logic
- Modifying existing tests to make reproduction easier
- Adding unrelated fixes, assertions, or scenarios
- Claiming success without execution evidence
- Treating environment/setup failure as successful reproduction

## Files

- Main template: `prompt-template.md`

## Execution Rules

- Treat stage A output as the only contract between extraction and reproduction.
- Distinguish facts from inference.
- Prefer minimal reproductions unless the evidence shows real dependencies are required.
- If precise reproduction is blocked by missing evidence, state the gap and downgrade to an approximate reproduction only when the template allows it.
- The goal is reproduction, not repair.
- Only reproduction artifacts may be edited unless the task explicitly says otherwise.
- `Broken/Error` is not a successful reproduction outcome.

## Quick Start

- For raw issue input: apply stage A from `prompt-template.md`, output only the normalized summary, then apply stage B.
- For normalized input: apply only stage B from `prompt-template.md`.
