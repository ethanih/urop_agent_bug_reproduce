# Normalized Issue Summary

## issue_metadata
- project: langchain
- issue_url: https://github.com/langchain-ai/langchain/issues/36290
- title: Agent with structured output fails when OpenAI response has phased response with 'commentary' and 'final_answer'

## bug_overview
- one_sentence_summary: Structured-output parsing can fail when an `AIMessage` content list contains multiple `text` items from different OpenAI phases and LangChain concatenates them into invalid JSON.
- expected_behavior: The parser should select the appropriate phase or otherwise handle multi-part text content without producing invalid combined JSON.
- actual_behavior: Two JSON strings are effectively concatenated, causing `json.loads` to fail with `Extra data`.
- primary_error: `ValueError: Native structured output expected valid JSON ... Extra data`

## reproduction_type_prediction
- predicted_type: minimal
- rationale: The issue body already includes a pure local `AIMessage` example with no provider call.

## environment
- language_runtime: Python 3.14.0
- package_versions: `langchain 1.2.13`, `langchain_core 1.2.22`, `langchain_openai 1.1.12`, `openai 2.30.0`
- operating_system: Windows 10
- llm_provider_or_external_service: OpenAI phased responses are referenced, but the repro is local
- other_constraints: `ProviderStrategyBinding.parse(message)` path

## trigger_conditions
- required_inputs: `AIMessage.content` list with multiple `text` items from different phases, each containing JSON text
- required_configuration: Structured output provider strategy binding for a pydantic model
- required_execution_flow: Parse the message content into a single raw JSON payload

## evidence_from_issue
- explicit_reproduction_steps:
  - Define a pydantic model
  - Create an `AIMessage` whose content is a list of two `text` items with phases `commentary` and `final_answer`
  - Call `ProviderStrategyBinding(...).parse(message)`
- code_snippets:
  - |
    message = AIMessage(
        content=[
            dict(type="text", phase="commentary", text='{"some_field": "some text"}'),
            dict(type="text", phase="final_answer", text='{"some_field": "some other text"}'),
        ]
    )
- error_messages:
  - `json.decoder.JSONDecodeError: Extra data`
  - `ValueError: Native structured output expected valid JSON for MyModel, but parsing failed`

## fact_vs_inference
- facts:
  - The issue repro does not use a real model call.
  - The traceback shows `json.loads(raw_text)` failing with `Extra data`.
- inferences:
  - LangChain is concatenating multiple text segments instead of selecting the correct one.

## scope_decision
- chosen_bug_scope: Reproduce the multi-phase text concatenation failure.
- excluded_noise_or_secondary_issues: OpenAI upstream implementation details are excluded except as evidence that phase fields exist.

## reproduction_guidance_for_agent
- minimal_repro_core: Concatenate two JSON strings from separate text phases and parse them as one JSON object.
- must_use_real_dependency: no
- external_network_required: no
- mocking_allowed: yes
- smallest_viable_artifacts:
  - reproduce.py
  - README.md
