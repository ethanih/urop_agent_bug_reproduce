# https://github.com/openai/codex/issues/666

# Issue 666 Reproduction

Source issue: `openai/codex#666`

## Reproduction Type

This is a minimal reproduction.

The original issue is about files being created with empty contents. This reproduction models that exact failure: generated content exists in memory, but empty strings are written to disk instead.

## Files

- `normalized_issue_summary.md`: stage A normalized issue facts
- `reproduce.py`: stage B reproduction

## Environment

- Python 3.10 or newer
- No network access required
- No external services required

## Reproduction Steps

1. Open the reproduction directory:

   ```bash
   cd codex/codex-issue-666
   ```

2. Run the MRE:

   ```bash
   python reproduce.py
   ```

## Expected Result

The created files should contain the generated content.

## Actual Result

The script creates files, but writes empty content:

```text
Generated content for App.vue:
<template><h1>Hello from generated app</h1></template>

Actual file content on disk for App.vue:
''
```

The same bug is shown for multiple created files.
