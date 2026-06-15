# Normalized Issue Summary

## issue_metadata
- project: langchain
- issue_url: https://github.com/langchain-ai/langchain/issues/34910
- title: `PydanticToolsParser` raises KeyError when partial=True and an unmatched tool is present

## bug_overview
- one_sentence_summary: `PydanticToolsParser.parse_result(..., partial=True)` still raises `KeyError` when a parsed tool name is not registered.
- expected_behavior: With `partial=True`, unmatched tools should be skipped or treated as partial/unparseable output rather than crashing.
- actual_behavior: The parser indexes `name_dict[res["type"]]` and raises `KeyError` for unknown tools.
- primary_error: `KeyError: 'Model3'`

## reproduction_type_prediction
- predicted_type: minimal
- rationale: The issue already contains a standalone parser example with no external dependencies.

## environment
- language_runtime: Python 3.10
- package_versions: `langchain_core 0.3.68`, `langchain 0.3.26`, `langsmith 0.4.5`
- operating_system: 未提供
- llm_provider_or_external_service: None required
- other_constraints: Uses `PydanticToolsParser`

## trigger_conditions
- required_inputs: Parsed tool call list containing at least one tool name not registered in the parser
- required_configuration: `partial=True`
- required_execution_flow: Parse tool-call results into pydantic objects

## evidence_from_issue
- explicit_reproduction_steps:
  - Define `Model1` and `Model2`
  - Build `PydanticToolsParser(tools=[Model1, Model2])`
  - Pass an `AIMessage` with tool calls for `Model1` and unknown `Model3`
  - Call `parse_result([result], partial=True)`
- code_snippets:
  - |
    output = parser.parse_result([result], partial=True)
- error_messages:
  - `KeyError: 'Model3'`

## fact_vs_inference
- facts:
  - The issue uses `partial=True`.
  - The crash occurs on an unmatched tool name.
- inferences:
  - The parser only handles partial failures for validation/arg parsing, not unknown tool names.

## scope_decision
- chosen_bug_scope: Reproduce the unmatched-tool `KeyError` under `partial=True`.
- excluded_noise_or_secondary_issues: Argument validation and other parser paths are secondary; the repro targets unknown tool-name handling.

## reproduction_guidance_for_agent
- minimal_repro_core: Create a tool-name lookup and hit it with an unknown type while `partial=True`.
- must_use_real_dependency: no
- external_network_required: no
- mocking_allowed: yes
- smallest_viable_artifacts:
  - reproduce.py
  - README.md
