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

## Environment

Use Python 3.12 if you want to match the issue report closely.

```bash
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

`requirements.txt` is intentionally lightweight so this reproduction does not require AWS credentials or a real Bedrock call.

For a closer old-version environment, see `requirements-crewai-1.13.0.txt`.

## Run

```bash
python reproduce_bedrock_tool_args_bug.py
```

Expected output:

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

This script isolates the faulty argument extraction described in the issue. It does not call CrewAI internals directly, because the observed failure happens after Bedrock has already produced a valid tool call and before the tool is invoked.

The reproduction proves the core regression:

- Bedrock provides valid tool arguments under `input`.
- The old extraction logic returns `{}`.
- Pydantic validation fails because required field `city` is missing.
- The proposed extraction logic correctly returns `{"city": "Paris"}`.
