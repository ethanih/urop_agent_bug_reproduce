# Normalized Issue Summary

## issue_metadata
- project: crewAI
- issue_url: https://github.com/crewAIInc/crewAI/issues/316
- title: DuckDuckGo Search not working anymore? Not supported?

## bug_overview
- one_sentence_summary: After upgrading to `crewai 0.19.0`, the DuckDuckGo search tool forwards `{"q": ...}` in a way that causes the wrapped search runner to reject the argument shape.
- expected_behavior: The DuckDuckGo search tool should accept a natural-language query and execute the search successfully.
- actual_behavior: The tool call fails because `DuckDuckGoSearchRun._run()` receives an unexpected `q` keyword argument.
- primary_error: `TypeError: DuckDuckGoSearchRun._run() got an unexpected keyword argument 'q'`

## reproduction_type_prediction
- predicted_type: minimal
- rationale: The failure is an argument-shape mismatch between the CrewAI tool wrapper and the underlying search runner. That boundary can be reproduced locally without calling DuckDuckGo.

## environment
- language_runtime: Python
- package_versions: `crewai 0.19.0`
- operating_system: 未提供
- llm_provider_or_external_service: DuckDuckGo search is the intended integration, but the core failure occurs before any real network call is required.
- other_constraints: The tool invocation shows `Action: duckduckgo_search` with `Action Input: {"q": "AIi news latest not older than 1 day"}`

## trigger_conditions
- required_inputs: Tool input shaped like `{"q": "<search query>"}`
- required_configuration: CrewAI DuckDuckGo search tool wrapped around `DuckDuckGoSearchRun`
- required_execution_flow: Agent invokes `duckduckgo_search`, CrewAI forwards the input to the backend runner, and the backend receives `q` as an unexpected keyword argument

## evidence_from_issue
- explicit_reproduction_steps:
  - Upgrade to `crewai 0.19.0`
  - Run a workflow that invokes `duckduckgo_search`
  - Observe the tool action input containing `{"q": "..."}`
  - Observe the backend raise a keyword-argument error
- code_snippets:
  - |
    Action: duckduckgo_search
    Action Input: {"q": "AIi news latest not older than 1 day"}
- error_messages:
  - `DuckDuckGoSearchRun._run() got an unexpected keyword argument 'q'`
  - `Tool duckduckgo_search accepts there inputs: ... Input should be a search query.`

## fact_vs_inference
- facts:
  - The issue says the problem appeared after updating to `crewai 0.19.0`.
  - The tool action input is shown as a dict with key `q`.
  - The backend rejects the `q` keyword.
- inferences:
  - The wrapper is passing structured keyword input where the backend expects a plain search string or a different call shape.

## scope_decision
- chosen_bug_scope: Reproduce the `q` keyword argument mismatch at the tool-wrapper boundary.
- excluded_noise_or_secondary_issues: Whether DuckDuckGo support was intentionally removed is excluded because the concrete evidence points to a call-shape bug rather than a missing feature.

## reproduction_guidance_for_agent
- minimal_repro_core: Model a backend `_run(query: str)` function and a wrapper that incorrectly dispatches `{"q": ...}` as keyword arguments.
- must_use_real_dependency: no
- external_network_required: no
- mocking_allowed: yes
- smallest_viable_artifacts:
  - reproduce.py
  - README.md
