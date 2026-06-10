# Issue 4788 Reproduction

Source issue: `crewAIInc/crewAI#4788`

## Bug

The reported regression happens when an assistant message contains both:

- normal text content
- native `tool_calls`

The buggy control flow in `llm.py` checks the text branch first and returns
early. Once that happens, the tool calls are ignored, so the tool is never
invoked even though the model asked for it.

## Why This Reproduction Is Minimal

This repository does not need a full CrewAI agent, an external LLM, or any
provider credentials. The reproduction only needs the response shape that
triggers the bad branch order:

```python
{
    "content": "I can help with that, and I will call the tool now.",
    "tool_calls": [
        {"name": "lookup_weather", "arguments": {"city": "Paris"}}
    ],
}
```

The script mirrors the bug by implementing two paths:

- `llm_buggy_branch_order(...)` returns as soon as it sees text.
- `llm_fixed_branch_order(...)` prioritizes tool calls whenever they are present.

## Run

```bash
python reproduce_text_plus_tool_calls_bug.py
```

Expected output:

```text
Incoming response:
...

Buggy llm.py branch order:
{'path': 'text', 'content': 'I can help with that, and I will call the tool now.', 'tool_calls_seen': 0, 'available_functions': None}

Fixed llm.py branch order:
{'path': 'tool_calls', 'content': 'I can help with that, and I will call the tool now.', 'tool_calls_seen': 1, 'available_functions': None}
```

## Notes

- The reproduction deliberately sets `available_functions = None` because that
  is the state called out in the issue.
- The comments in the script are meant to make the failure mode explicit:
  text is being treated as a terminal answer even when tool calls are also
  present, so the tool branch is never reached.
