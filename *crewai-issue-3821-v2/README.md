# crewAIInc/crewAI#3821 Reproduction

Source issue: `https://github.com/crewAIInc/crewAI/issues/3821`

## Reproduction Type

最小化复现。

This reproduction isolates the validator-exception retry bypass described by the
issue title and minimal narrative. It does not recreate the full HTTP-backed
crewAI stack or the longer `ConverterError` chain from the issue discussion.

## Files

- `normalized_issue_summary.md`: stage A normalized issue summary
- `reproduce.py`: stage B minimal reproduction

## Environment

- Python 3.10+
- `pydantic>=2,<3`
- No network access required

## Missing Information

- The exact failing crewAI version is not fully pinned in the preserved issue evidence available here.
- The full end-to-end issue path also mentions `ConverterError`, which is not reproduced in this minimal script.

## Reproduction Steps

1. Open the reproduction directory.

   ```bash
   cd crewai-issue-3821-v2
   ```

2. Ensure `pydantic` is available.

   Example:

   ```bash
   python -m pip install "pydantic>=2,<3"
   ```

3. Run the reproduction script.

   ```bash
   python reproduce.py
   ```

4. Observe that execution stops on the first invalid candidate before the second valid candidate is retried.

## Expected Result

If structured-output retry behaved robustly, the first invalid candidate would
be rejected and the second candidate `{"label": "support"}` would still be
retried and accepted.

## Actual Result

The script stops on the first candidate with a raw validator exception such as:

```text
Exception: Invalid label: wrong-label
```

## Outcome Classification

- `Fail-Match`: execution aborts on the first invalid candidate because the validator-raised exception bypasses the retry path
- `Fail-Approx`: a closely related validation-path failure occurs, but the observed error surface differs materially from the issue narrative
- `Pass`: the script retries and successfully returns the second candidate
- `Broken-Setup`: `pydantic` is unavailable or the environment cannot run the script
- `Broken-Script`: the reproduction script itself has a syntax/import/logic bug unrelated to the target issue

This reproduction should only be treated as successful when the observed result is `Fail-Match`.
