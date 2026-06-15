# Normalized Issue Summary

## issue_metadata
- project: langchain
- issue_url: https://github.com/langchain-ai/langchain/issues/34918
- title: `No data received from Ollama stream.` exception

## bug_overview
- one_sentence_summary: LangChain's Ollama async aggregation path can raise `ValueError` when a streaming call yields no chunks.
- expected_behavior: The stream path should either handle empty streams gracefully or provide a more robust retry/recovery path.
- actual_behavior: `_achat_stream_with_aggregation` raises `ValueError: No data received from Ollama stream.`
- primary_error: `ValueError: No data received from Ollama stream.`

## reproduction_type_prediction
- predicted_type: real_dependency
- rationale: The issue occurs in an actual streaming integration stack involving Ollama, LangGraph, and a deep-agent workflow.

## environment
- language_runtime: Python 3.13.7
- package_versions: `langchain 1.2.7`, `langchain_core 1.2.7`, `langchain_ollama 1.0.1`, `langgraph_api 0.7.9`, plus deep-agent related packages
- operating_system: Linux Ubuntu
- llm_provider_or_external_service: Ollama with `gpt-oss`
- other_constraints: Async graph streaming path through agent `.astream(...)`

## trigger_conditions
- required_inputs: A user message through the agent streaming interface
- required_configuration: Async stream mode over an Ollama-backed model
- required_execution_flow: The underlying Ollama stream returns no data chunks before aggregation completes

## evidence_from_issue
- explicit_reproduction_steps:
  - Iterate over `self._agent.astream(...)`
  - Reach the model node backed by `langchain_ollama`
  - Observe failure in `_achat_stream_with_aggregation`
- code_snippets:
  - |
    async for stream_mode, data in self._agent.astream(...):
        ...
- error_messages:
  - `ValueError: No data received from Ollama stream.`

## fact_vs_inference
- facts:
  - The traceback ends in `langchain_ollama.chat_models._achat_stream_with_aggregation`.
  - The issue is described as intermittent.
- inferences:
  - The upstream streaming transport sometimes yields an empty sequence where LangChain expects at least one chunk.

## scope_decision
- chosen_bug_scope: Reproduce the empty-stream aggregation failure boundary.
- excluded_noise_or_secondary_issues: The broader deep-agent stack is excluded except for the fact that it reaches the Ollama async stream path.

## reproduction_guidance_for_agent
- minimal_repro_core: Aggregate an async stream that yields zero chunks and show the same `ValueError`.
- must_use_real_dependency: yes
- external_network_required: no
- mocking_allowed: no
- smallest_viable_artifacts:
  - reproduce.py
  - README.md
