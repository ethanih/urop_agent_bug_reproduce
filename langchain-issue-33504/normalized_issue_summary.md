# Normalized Issue Summary

## issue_metadata
- project: langchain
- issue_url: https://github.com/langchain-ai/langchain/issues/33504
- title: create_agent Does Not Handle invalid_tool_calls from JSON Parsing Errors (langchain alpha v1)

## bug_overview
- one_sentence_summary: `create_agent` exits after an `AIMessage` containing `invalid_tool_calls` because routing only checks `tool_calls` and ignores invalid ones.
- expected_behavior: The agent should convert or surface invalid tool calls so the model can recover instead of silently stopping.
- actual_behavior: The agent stops after the first model call and never creates a `ToolMessage` for the parsing error.
- primary_error: No exception; agent exits early after one call with `invalid_tool_calls` populated

## reproduction_type_prediction
- predicted_type: minimal
- rationale: The issue already includes a self-contained mock chat model and requires no external provider behavior.

## environment
- language_runtime: Python
- package_versions: Not fully listed in the captured body
- operating_system: 未提供
- llm_provider_or_external_service: None required; the repro uses a mock model
- other_constraints: The bug is in `create_agent` routing and tool execution flow

## trigger_conditions
- required_inputs: An `AIMessage` with `tool_calls=[]` and non-empty `invalid_tool_calls`
- required_configuration: Agent created via `create_agent(model=..., tools=[...])`
- required_execution_flow: First model call emits malformed tool JSON, then the agent routing step decides whether to continue

## evidence_from_issue
- explicit_reproduction_steps:
  - Define a tool
  - Define a mock chat model that returns `invalid_tool_calls` on its first call
  - Create an agent with `create_agent`
  - Invoke the agent and count model calls
- code_snippets:
  - |
    return AIMessage(
        content="",
        tool_calls=[],
        invalid_tool_calls=[{...}],
    )
- error_messages:
  - `Model was called 1 time(s)`
  - `BUG CONFIRMED: Agent exited after first call`

## fact_vs_inference
- facts:
  - The issue body points to routing logic that exits when `len(last_ai_message.tool_calls) == 0`.
  - The issue body says `ToolNode` only processes `tool_calls`.
  - The mock repro shows only one model call.
- inferences:
  - Proper handling would either retry or produce a `ToolMessage` equivalent for the invalid call.

## scope_decision
- chosen_bug_scope: Reproduce the early-exit routing bug for `invalid_tool_calls`.
- excluded_noise_or_secondary_issues: Comparisons to deprecated `AgentExecutor` are kept as context only; the repro targets `create_agent`.

## reproduction_guidance_for_agent
- minimal_repro_core: Route on a message with empty `tool_calls` but non-empty `invalid_tool_calls`, and show that the loop exits.
- must_use_real_dependency: no
- external_network_required: no
- mocking_allowed: yes
- smallest_viable_artifacts:
  - reproduce.py
  - README.md
