# Normalized Issue Summary

## issue_metadata
- project: langchain
- issue_url: https://github.com/langchain-ai/langchain/issues/11408
- title: BooleanOutputParser expected output value error

## bug_overview
- one_sentence_summary: `LLMChainFilter.from_llm(...)` can fail because `BooleanOutputParser` only accepts exact `YES` or `NO`, while the LLM returns a longer sentence that starts with `Yes`.
- expected_behavior: The retriever should return filtered documents.
- actual_behavior: Execution fails with a `ValueError` when the parser receives a verbose affirmative answer.
- primary_error: `ValueError: BooleanOutputParser expected output value to either be YES or NO. Received Yes, the context is relevant ...`

## reproduction_type_prediction
- predicted_type: minimal
- rationale: The core failure is strict boolean parsing of a verbose model response. That parser behavior can be reproduced locally without a live SageMaker endpoint.

## environment
- language_runtime: Python
- package_versions: `langchain==0.0.308`
- operating_system: 未提供
- llm_provider_or_external_service: SageMaker endpoint model is mentioned, but not required to reproduce the parser bug itself.
- other_constraints: Triggered through `LLMChainFilter.from_llm(...)` in a contextual compression retriever flow.

## trigger_conditions
- required_inputs: An LLM response like `Yes, the context is relevant ...` instead of exact `YES` or `NO`.
- required_configuration: A filter path that uses `BooleanOutputParser`.
- required_execution_flow: Call the filter so the model output is parsed as a boolean relevance decision.

## evidence_from_issue
- explicit_reproduction_steps:
  - Create `LLMChainFilter.from_llm(llm)`.
  - Use it as the `base_compressor` in `ContextualCompressionRetriever`.
  - Call `get_relevant_documents(...)`.
- code_snippets:
  - |
    from langchain.retrievers import ContextualCompressionRetriever
    from langchain.retrievers.document_compressors import LLMChainExtractor, LLMChainFilter
    _filter = LLMChainFilter.from_llm(llm)
    compressor = LLMChainExtractor.from_llm(llm)
    compression_retriever = ContextualCompressionRetriever(base_compressor=_filter, base_retriever=faiss_retriever)
    compressed_docs = compression_retriever.get_relevant_documents("What did the president say about Ketanji Jackson Brown?")
- error_messages:
  - `ValueError: BooleanOutputParser expected output value to either be YES or NO. Received Yes, the context is relevant ...`

## fact_vs_inference
- facts:
  - The reporter was using `LLMChainFilter.from_llm(llm)`.
  - The parser rejected a response beginning with `Yes, ...`.
  - The reporter expected filtered docs.
- inferences:
  - The root cause is strict exact-match parsing rather than semantic boolean parsing.

## scope_decision
- chosen_bug_scope: Reproduce the strict parser failure on verbose affirmative output.
- excluded_noise_or_secondary_issues: The full FAISS/SageMaker retriever stack is excluded because the visible bug happens at the parser boundary.

## reproduction_guidance_for_agent
- minimal_repro_core: Feed a verbose `Yes, ...` string into a parser that only accepts exact `YES` or `NO`.
- must_use_real_dependency: no
- external_network_required: no
- mocking_allowed: yes
- smallest_viable_artifacts:
  - reproduce.py
  - README.md
