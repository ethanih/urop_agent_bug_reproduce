# langchain-ai/langchain#34358 Reproduction

Source issue: `https://github.com/langchain-ai/langchain/issues/34358`

## Reproduction Type

最小化复现。

This reproduction targets the reported failure mechanism only: direct access to
`response["tools"]` in tool-selection response handling when the selector output
omits that key.

## Files

- `normalized_issue_summary.md`: stage A normalized issue summary
- `reproduce.py`: stage B minimal reproduction

## Environment

- Python 3.11+ recommended
- No network access required
- No external model or provider required

## Missing Information

- The original issue does not fully pin every dependency in the affected environment.
- The exact malformed selector payload from the live model response is not preserved here.

## Reproduction Steps

1. Enter the reproduction directory.

   ```bash
   cd langchain-issue-34358-v2
   ```

2. Run the reproduction script.

   ```bash
   python reproduce.py
   ```

3. Observe the process exit with `KeyError: 'tools'`.

## Expected Result

If the middleware handled malformed selector output defensively, it would reject
the response cleanly or surface a validation error instead of crashing on direct
key access.

## Actual Result

The reproduction script raises:

```text
KeyError: 'tools'
```

## Outcome Classification

- `Fail`: observed `KeyError: 'tools'`
- `Pass`: no exception is raised
- `Broken/Error`: Python cannot run the script or a different unrelated error occurs

This reproduction is only considered successful when the observed outcome is `Fail`.
