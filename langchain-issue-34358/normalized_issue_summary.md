# Normalized Issue Summary

## issue_metadata
- project: langchain
- issue_url: https://github.com/langchain-ai/langchain/issues/34358
- title: KeyError: 'tools' in LLMToolSelectorMiddleware when model response misses expected key

## bug_overview
- one_sentence_summary: `LLMToolSelectorMiddleware` assumes the tool-selection response contains a `tools` key and crashes with `KeyError` when the response shape is incomplete.
- expected_behavior: Middleware should validate the response shape and fail gracefully or recover when `tools` is missing.
- actual_behavior: `_process_selection_response` indexes `response["tools"]` directly and raises `KeyError`.
- primary_error: `KeyError: 'tools'`

## reproduction_type_prediction
- predicted_type: minimal
- rationale: The bug is a direct dictionary-access failure and does not require a real model.

## environment
- language_runtime: Python 3.11+
- package_versions: `langchain 1.1.3`; other versions not fully pinned
- operating_system: Windows
- llm_provider_or_external_service: The issue example uses OpenAI, but the key failure is middleware-local
- other_constraints: Requires `LLMToolSelectorMiddleware(max_tools=2)` or similar tool selection path

## trigger_conditions
- required_inputs: A tool-selector response missing the `tools` key
- required_configuration: Agent with `LLMToolSelectorMiddleware`
- required_execution_flow: Middleware processes selector output before the main model call

## evidence_from_issue
- explicit_reproduction_steps:
  - Register at least two tools
  - Create `LLMToolSelectorMiddleware(max_tools=2)`
  - Invoke the agent multiple times
  - Observe intermittent `KeyError` when response is malformed
- code_snippets:
  - |
    for tool_name in response["tools"]:
        ...
- error_messages:
  - `KeyError: 'tools'`

## fact_vs_inference
- facts:
  - The issue body identifies `tool_selection.py` and the direct `response["tools"]` access.
  - The failure is intermittent and tied to malformed tool-selection output.
- inferences:
  - Defensive schema validation is missing in the middleware response handler.

## scope_decision
- chosen_bug_scope: Reproduce the middleware crash on a missing `tools` key.
- excluded_noise_or_secondary_issues: Real model behavior is excluded because the local response-shape assumption is sufficient to trigger the bug.

## reproduction_guidance_for_agent
- minimal_repro_core: Call the response-processing logic with a dict that omits `tools`.
- must_use_real_dependency: no
- external_network_required: no
- mocking_allowed: yes
- smallest_viable_artifacts:
  - reproduce.py
  - README.md
