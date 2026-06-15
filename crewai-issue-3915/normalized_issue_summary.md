# Normalized Issue Summary

## issue_metadata
- project: crewAI
- issue_url: https://github.com/crewAIInc/crewAI/issues/3915
- title: [BUG] ERROR:root:Failed to parse structured output from stream: 1 validation error for TaskEvaluation quality

## bug_overview
- one_sentence_summary: Long-term memory saving can fail because the streamed `TaskEvaluation` payload omits required fields and uses the wrong type for `suggestions`.
- expected_behavior: Task evaluations should parse and persist to long-term memory without validation errors.
- actual_behavior: Memory saving logs validation failures and drops that memory entry.
- primary_error: `Field required` for `quality`, plus `suggestions.* Input should be a valid string`

## reproduction_type_prediction
- predicted_type: minimal
- rationale: The visible failure is a Pydantic schema mismatch. A local script can recreate the same validation errors without running a full crew.

## environment
- language_runtime: Python
- package_versions: `crewai==1.4.1` mentioned in the issue description
- operating_system: 未提供
- llm_provider_or_external_service: Not required for the schema mismatch itself.
- other_constraints: Triggered in memory-saving / `TaskEvaluation` structured-output parsing.

## trigger_conditions
- required_inputs: A payload missing `quality` and containing `suggestions` as objects instead of strings.
- required_configuration: Memory-enabled crew with long-term evaluation storage.
- required_execution_flow: Run a task, generate a `TaskEvaluation`, then parse/store it.

## evidence_from_issue
- explicit_reproduction_steps:
  - Create a crew with `memory=True` and external memory.
  - Run any task.
  - Observe memory save attempt fail.
- code_snippets:
  - 未提供
- error_messages:
  - `quality Field required`
  - `suggestions.0 Input should be a valid string`
  - Similar errors repeated for multiple suggestion entries

## fact_vs_inference
- facts:
  - The issue reports validation errors for `TaskEvaluation`.
  - The payload omitted `quality`.
  - `suggestions` entries were dictionaries instead of strings.
- inferences:
  - The memory-evaluation prompt/model output no longer matches the expected storage schema.

## scope_decision
- chosen_bug_scope: Reproduce the `TaskEvaluation` schema mismatch.
- excluded_noise_or_secondary_issues: Full crew execution is excluded because the concrete failure is in structured-output validation at memory-save time.

## reproduction_guidance_for_agent
- minimal_repro_core: Validate a payload missing `quality` and containing dict-valued suggestions against a strict schema.
- must_use_real_dependency: no
- external_network_required: no
- mocking_allowed: yes
- smallest_viable_artifacts:
  - reproduce.py
  - README.md
