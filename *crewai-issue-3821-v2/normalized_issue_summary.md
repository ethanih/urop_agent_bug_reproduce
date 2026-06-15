# Normalized Issue Summary

## issue_metadata
- project: crewAI
- issue_url: https://github.com/crewAIInc/crewAI/issues/3821
- title: [BUG] crewAI fails when pydantic field validator is used

## bug_overview
- one_sentence_summary: When structured output validation uses a Pydantic `@field_validator` that raises a raw exception, the retry path is bypassed and execution stops instead of retrying with a new candidate.
- expected_behavior: Invalid structured output should remain retryable, even when validation fails inside a custom Pydantic field validator.
- actual_behavior: The validator-raised exception escapes the retry-oriented validation flow and aborts execution on the first invalid output.
- primary_error: Validator-raised exception escapes the retry path.

## reproduction_type_prediction
- predicted_type: minimal
- rationale: The core bug is retry-control-flow behavior around Pydantic validation and can be reproduced locally with a small script plus the real `pydantic` dependency, without needing crewAI itself or any live model/provider.

## environment
- target_language: python
- language_runtime: Python 3.10+
- package_versions: The issue reports a regression after `0.201.1`; exact failing crewAI version is not fully pinned in the preserved local evidence. The reproduction here uses `pydantic>=2,<3`.
- operating_system: 未提供
- llm_provider_or_external_service: The issue includes a custom LLM wrapper over HTTP, but the retry-bypass failure can be reproduced without any external service
- other_constraints: Uses a Pydantic `@field_validator` in an `output_pydantic`-style structured-output flow

## trigger_conditions
- required_inputs: A structured output candidate whose field value violates a custom `@field_validator` rule
- required_configuration: A retry-capable structured-output loop that does not catch the raw exception type emitted by the validator
- required_execution_flow: Validate the candidate, hit a validator-raised exception, and observe that execution aborts before a second candidate is retried

## issue_related_context
- issue_related_code:
  - path_or_symbol: output model with `@field_validator`
    kind: class
    excerpt_or_role: Defines the custom validation rule whose exception is expected to stay within the structured-output retry flow
  - path_or_symbol: retry-oriented structured output / converter path
    kind: module
    excerpt_or_role: Handles parsing and retry behavior after LLM output is converted into a Pydantic model
- relevance_explanation:
  - The output model is directly relevant because the reported bug is specifically triggered by a `@field_validator` raising on invalid content.
  - The converter or structured-output retry path is directly relevant because the issue is not merely “validation fails”, but “validation failure stops execution instead of retrying”.

## evidence_from_issue
- explicit_reproduction_steps:
  - Define an output model using `@field_validator`
  - Raise an exception from the validator when the output value is invalid
  - Run a crew or structured-output flow using that model as `output_pydantic`
  - Observe that execution stops instead of retrying
- code_snippets:
  - |
    class LabelOutput(BaseModel):
        label: str

        @field_validator("label")
        @classmethod
        def check_label(cls, value: str) -> str:
            if value not in LABEL_VOCAB:
                raise Exception(...)
            return value
- error_messages:
  - The issue reports that auto-retry is compromised when the validator raises
  - The longer example in the issue also mentions `ConverterError`, creating ambiguity about whether the failing surface is the validator itself, fenced JSON parsing, or both

## fact_vs_inference
- facts:
  - The issue title and description attribute the failure to use of a Pydantic `field_validator`.
  - The issue states that execution stops and does not retry when validation fails in this way.
  - The issue includes a more complex end-to-end example involving structured output conversion and HTTP-backed model output.
- inferences:
  - A minimal retry loop that catches a narrower validation class than the raw validator exception is sufficient to reproduce the core retry-bypass mechanism.
  - The issue may involve more than one contributing factor in the full stack, but the validator exception bypass is the smallest defensible repro scope.

## uncertainty_and_gaps
- missing_critical_info:
  - The exact failing crewAI version is not fully pinned in the local preserved evidence.
  - The exact internal crewAI catch/exception hierarchy from the reporter’s version is not reproduced in this local workspace.
- known_ambiguities:
  - The issue title emphasizes `field_validator`, but the larger example also mentions code-fenced JSON and `ConverterError`, so the full production failure path may include both parsing and validation concerns.
  - This reproduction isolates the validator exception bypass and does not attempt to prove every detail of the end-to-end crewAI stack.
- confidence_level: medium

## scope_decision
- chosen_bug_scope: Reproduce the retry bypass caused by a raw exception raised inside a Pydantic `@field_validator`.
- excluded_noise_or_secondary_issues: The full custom HTTP LLM wrapper, fenced JSON parsing behavior, and broader `ConverterError` chain are excluded because they are not necessary to demonstrate the core “validator exception aborts instead of retries” mechanism described by the title and minimal issue narrative.

## reproduction_guidance_for_agent
- minimal_repro_core: Build a retry loop over two structured-output candidates where the first candidate triggers a validator-raised `Exception`, and show that a narrow catch path aborts before the second valid candidate is retried.
- must_use_real_dependency: no
- external_network_required: no
- mocking_allowed: yes
- approximate_reproduction_allowed: yes
- smallest_viable_artifacts:
  - reproduce.py
  - README.md
