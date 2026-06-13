# https://github.com/crewAIInc/crewAI/issues/5275

# Issue 5275 Reproduction

Source issue: `crewAIInc/crewAI#5275`

## Bug

Bedrock Converse API returns tool calls in this shape:

```python
{"name": "get_travel_details", "toolUseId": "abc123", "input": {"city": "Paris"}}
```

Affected CrewAI versions such as `1.9.3` and `1.13.0` handled tool arguments with logic equivalent to:

```python
func_info = tool_call.get("function", {})
func_args = func_info.get("arguments", "{}") or tool_call.get("input", {})
```

For Bedrock tool calls there is no `function` wrapper. The default string `"{}"` is truthy, so the code never reads `tool_call["input"]`. The tool receives `{}` instead of `{"city": "Paris"}`.

## Reproduction Type

This is a real-dependency reproduction.

It uses the real `pydantic` dependency and mirrors the crewAI extraction logic described in the issue. The `requirements-crewai-1.13.0.txt` file is included for a closer version-pinned environment when you want to validate against crewAI itself.

## Environment

Use Python 3.12 if you want to match the issue report closely.

1. Create and activate a virtual environment:

   ```bash
   python3.12 -m venv .venv
   source .venv/bin/activate
   ```

2. Install the minimal dependencies for this reproduction:

   ```bash
   python -m pip install -r requirements.txt
   ```

3. If you want to try the version-pinned crewAI environment described in the
   issue, install the older dependency set instead:

   ```bash
   python -m pip install -r requirements-crewai-1.13.0.txt
   ```

## Reproduction Steps

1. Open the reproduction directory.
2. Create and activate the virtual environment.
3. Install dependencies with `python -m pip install -r requirements.txt`.
4. Run the script:

   ```bash
   python reproduce.py
   ```

## Expected Result

If the argument extraction were correct, the Bedrock payload would produce:

```text
Fixed extracted args:
{'city': 'Paris'}

Tool result with fixed args:
Details for Paris
```

## Actual Result

The buggy path drops the Bedrock `input` field and produces an empty argument
dict:

```text
Bedrock tool call input:
{'city': 'Paris'}

Buggy extracted args:
{}

Validation error caused by dropped args:
...
Field required ...

Fixed extracted args:
{'city': 'Paris'}

Tool result with fixed args:
Details for Paris
```

## Why This Reproduces the Bug

This script isolates the faulty argument extraction described in the issue.
It does not make a live Bedrock call, but it does use the same shape and the
same failure condition: a Bedrock-format payload with `input` and a buggy
fallback that reads `"{}"` first.

The reproduction proves the core regression:

- Bedrock provides valid tool arguments under `input`.
- The old extraction logic returns `{}`.
- Pydantic validation fails because required field `city` is missing.
- The proposed extraction logic correctly returns `{"city": "Paris"}`.
