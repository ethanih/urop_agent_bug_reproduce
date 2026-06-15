# Normalized Issue Summary

## issue_metadata
- project: langchain
- issue_url: https://github.com/langchain-ai/langchain/issues/34358
- title: KeyError: 'tools' in LLMToolSelectorMiddleware when model response misses expected key

## bug_overview
- one_sentence_summary: `LLMToolSelectorMiddleware` assumes tool-selection output always contains a `tools` field and crashes with `KeyError` when that field is missing.
- expected_behavior: Middleware should validate selector output and reject or handle malformed responses without crashing on direct key access.
- actual_behavior: The tool-selection response handler indexes `response["tools"]` directly and raises `KeyError` when the model output omits that field.
- primary_error: `KeyError: 'tools'`

## reproduction_type_prediction
- predicted_type: minimal
- rationale: The failure is caused by unconditional dictionary access in middleware-local logic and can be triggered with a malformed in-memory response object, without any real model call or external service.

## environment
- target_language: python
- language_runtime: Python 3.11+
- package_versions: `langchain==1.1.3` reported in the issue; exact reproduction here does not require importing the package
- operating_system: Windows reported in the issue; reproduction logic is OS-agnostic
- llm_provider_or_external_service: The issue uses an LLM-backed tool selector, but the crashing path itself does not require a live provider
- other_constraints: Trigger occurs when tool selection middleware processes a selector response that lacks the `tools` key

## trigger_conditions
- required_inputs: A selector response object missing the `tools` field, for example `{"reason": "No tools needed"}` or any similarly malformed dict
- required_configuration: A code path equivalent to `LLMToolSelectorMiddleware` tool-selection response handling
- required_execution_flow: Selector output is parsed before the main model call, and the handler iterates over `response["tools"]`

## evidence_from_issue
- explicit_reproduction_steps:
  - Create an agent configured with `LLMToolSelectorMiddleware(max_tools=2)` and at least two tools
  - Invoke the agent so the middleware performs tool selection
  - Observe intermittent failure when the selector response is malformed and omits `tools`
- code_snippets:
  - |
    for tool_name in response["tools"]:
        ...
- error_messages:
  - `KeyError: 'tools'`

## fact_vs_inference
- facts:
  - The issue identifies a direct `response["tools"]` access in the tool-selection handling path.
  - The reported crash is `KeyError: 'tools'`.
  - The user describes the failure as occurring when the model response misses the expected key.
- inferences:
  - The minimal bug mechanism is missing schema validation before iterating selected tool names.
  - A local surrogate function with the same direct key access is sufficient to reproduce the failure mode relevant to the issue.

## uncertainty_and_gaps
- missing_critical_info:
  - The issue does not provide a fully pinned dependency set beyond the affected LangChain version.
  - The exact original selector prompt/response payload is not fully preserved in the local workspace.
- known_ambiguities:
  - The issue describes the malformed selector output as intermittent, but the local minimal reproduction makes it deterministic by supplying a malformed response directly.
  - The exact middleware internals may evolve across LangChain revisions, but the reported failing mechanism is stable enough for a minimal repro.
- confidence_level: high

## scope_decision
- chosen_bug_scope: Reproduce the crash caused by missing `tools` in the selector response handling path.
- excluded_noise_or_secondary_issues: Real provider behavior, prompt quality, and intermittent model formatting variance are excluded because they are upstream causes, not required to trigger the direct key-access failure.

## reproduction_guidance_for_agent
- minimal_repro_core: Implement the same direct iteration over `response["tools"]` and call it with a malformed dict that omits the key.
- must_use_real_dependency: no
- external_network_required: no
- mocking_allowed: yes
- approximate_reproduction_allowed: yes
- smallest_viable_artifacts:
  - reproduce.py
  - README.md
