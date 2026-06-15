# Normalized Issue Summary

## issue_metadata
- project: crewAI
- issue_url: https://github.com/crewAIInc/crewAI/issues/3843
- title: [BUG] Using OpenAI API and gpt-oss - Tool usage output sent to LLM exceed max_tokens

## bug_overview
- one_sentence_summary: Large tool output can be forwarded back to the model without truncation or summarization, producing an invalid negative `max_tokens` calculation.
- expected_behavior: The system should either summarize oversized tool output or fail gracefully before sending an impossible request.
- actual_behavior: The request is built with a negative `max_tokens` value and the API rejects it.
- primary_error: `custom error: max_tokens must be at least 1, got -804559`

## reproduction_type_prediction
- predicted_type: minimal
- rationale: The core bug is token-budget arithmetic when tool output is too large. That can be shown locally without Elasticsearch or a live OpenAI call.

## environment
- language_runtime: Python 3.12
- package_versions: `crewai==1.3.0`, `crewai-tools==1.3.0`
- operating_system: macOS Sonoma
- llm_provider_or_external_service: OpenAI API with `gpt-oss`
- other_constraints: Triggered when a tool returns much more text than the model context allows.

## trigger_conditions
- required_inputs: Oversized tool output.
- required_configuration: Tool-calling flow that appends tool output back into the next LLM request.
- required_execution_flow: Run a tool, compute remaining tokens, send follow-up LLM call.

## evidence_from_issue
- explicit_reproduction_steps:
  - Use a tool that exceeds the LLM context or token budget.
  - Observe the follow-up OpenAI request fail.
- code_snippets:
  - 未提供
- error_messages:
  - `Error code: 400 - {'status': 'failure', 'message': 'custom error: max_tokens must be at least 1, got -804559.'}`

## fact_vs_inference
- facts:
  - The reporter used a tool that sometimes returned around 10,000 records.
  - The resulting OpenAI call failed with negative `max_tokens`.
- inferences:
  - The bug is likely missing truncation/summarization before the token budget is computed.

## scope_decision
- chosen_bug_scope: Reproduce negative `max_tokens` from oversized tool output.
- excluded_noise_or_secondary_issues: Elasticsearch and model planning quality are excluded because the concrete failure is the impossible token budget.

## reproduction_guidance_for_agent
- minimal_repro_core: Compute `remaining_tokens = context_limit - prompt_tokens - tool_output_tokens` and show it goes below 1.
- must_use_real_dependency: no
- external_network_required: no
- mocking_allowed: yes
- smallest_viable_artifacts:
  - reproduce.py
  - README.md
