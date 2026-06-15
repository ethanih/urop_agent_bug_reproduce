# Normalized Issue Summary

## issue_metadata
- project: crewAI
- issue_url: https://github.com/crewAIInc/crewAI/issues/3821
- title: [BUG] crewAI fails when pydantic field validator is used

## bug_overview
- one_sentence_summary: When `output_pydantic` validation uses `@field_validator` and raises an exception, the crew stops instead of retrying.
- expected_behavior: Invalid structured output should trigger retry behavior instead of aborting execution immediately.
- actual_behavior: A validator-raised exception breaks the flow and compromises auto-retry.
- primary_error: Validator-raised exception escapes the retry path.

## reproduction_type_prediction
- predicted_type: minimal
- rationale: The issue is about retry control flow around Pydantic validation. A local script can reproduce the difference between retrying on structured-output failure and aborting on an uncaught validator exception.

## environment
- language_runtime: Python
- package_versions: Reporter mentioned a regression from `0.201.1` to later versions; exact failing version not fully pinned in the captured excerpt.
- operating_system: 未提供
- llm_provider_or_external_service: Custom LLM wrapper over an HTTP endpoint was shown, but not required to reproduce the retry bug.
- other_constraints: Uses Pydantic `@field_validator` in the output model.

## trigger_conditions
- required_inputs: Model output that violates a custom field validator rule.
- required_configuration: `output_pydantic` plus retry-capable execution path.
- required_execution_flow: Parse structured output, hit validator exception, then observe retry or no-retry behavior.

## evidence_from_issue
- explicit_reproduction_steps:
  - Define an output model with `@field_validator`.
  - Raise an exception in the validator for invalid values.
  - Run a crew using that model as `output_pydantic`.
- code_snippets:
  - |
    class LabelOutput(BaseModel):
        @field_validator("label")
        def check_label(cls, v):
            if v not in LABEL_VOCAB:
                raise Exception(...)
- error_messages:
  - The issue states that execution stops and auto-retry is compromised when the validator raises.

## fact_vs_inference
- facts:
  - The issue uses Pydantic field validators in an output schema.
  - Validator exceptions stop execution instead of retrying.
- inferences:
  - The retry path likely catches only a narrower validation class than the raw exception raised by the validator.

## scope_decision
- chosen_bug_scope: Reproduce validator exception bypassing retry.
- excluded_noise_or_secondary_issues: The full HTTP-based custom LLM stack is excluded because the failure is in output-validation control flow.

## reproduction_guidance_for_agent
- minimal_repro_core: Build a retry loop that validates output with a field validator raising `Exception`, then show the first error aborts the flow.
- must_use_real_dependency: no
- external_network_required: no
- mocking_allowed: yes
- smallest_viable_artifacts:
  - reproduce.py
  - README.md
