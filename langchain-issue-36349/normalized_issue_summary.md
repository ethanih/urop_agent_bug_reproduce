# Normalized Issue Summary

## issue_metadata
- project: langchain
- issue_url: https://github.com/langchain-ai/langchain/issues/36349
- title: Agents silently fail to deal with structured responses when models forget to make a tool call.

## bug_overview
- one_sentence_summary: An agent configured with `response_format=ToolStrategy(...)` can return without `structured_response` and without raising an error when the model emits no tool call at all.
- expected_behavior: With `handle_errors=False`, the agent should raise a structured-output error when the model omits the required output tool call.
- actual_behavior: The agent returns a response without `structured_response`, causing a silent failure.
- primary_error: No structured-output exception is raised; downstream code hits missing `structured_response`

## reproduction_type_prediction
- predicted_type: minimal
- rationale: The issue body uses fake chat models and isolates the behavior without real providers.

## environment
- language_runtime: Python
- package_versions: Not fully pinned in the issue body
- operating_system: 未提供
- llm_provider_or_external_service: None required in the repro
- other_constraints: `create_agent(..., response_format=ToolStrategy(..., handle_errors=False))`

## trigger_conditions
- required_inputs: A model response with no tool calls
- required_configuration: Structured response format with `handle_errors=False`
- required_execution_flow: Invoke the agent and inspect whether `structured_response` exists or an exception is raised

## evidence_from_issue
- explicit_reproduction_steps:
  - Create one fake model with correct tool calls
  - Create one fake model with bad tool calls
  - Create one fake model with no tool calls
  - Invoke agents and compare outcomes
- code_snippets:
  - |
    no_call_model = FakeWithSO(
        messages=iter([AIMessage(content="NOT a tool call")])
    )
- error_messages:
  - `No exception raised for no tool call!`
  - `AssertionError`

## fact_vs_inference
- facts:
  - Correct tool calls work.
  - Bad tool calls raise an exception.
  - No tool calls do not raise an exception and produce no `structured_response`.
- inferences:
  - The structured-output path handles invalid calls but misses the absent-call case.

## scope_decision
- chosen_bug_scope: Reproduce the missing-tool-call silent failure for structured responses.
- excluded_noise_or_secondary_issues: Related fake-model adaptation issues from another ticket are excluded.

## reproduction_guidance_for_agent
- minimal_repro_core: Simulate the branch where no tool call is emitted and no structured-output error is raised.
- must_use_real_dependency: no
- external_network_required: no
- mocking_allowed: yes
- smallest_viable_artifacts:
  - reproduce.py
  - README.md
