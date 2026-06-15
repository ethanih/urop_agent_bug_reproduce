# Normalized Issue Summary

## issue_metadata
- project: langchain
- issue_url: https://github.com/langchain-ai/langchain/issues/17352
- title: MultiQueryRetriever is failing

## bug_overview
- one_sentence_summary: `MultiQueryRetriever.from_llm(...)` can fail when the query-generation output parser receives data in the wrong shape and raises a Pydantic validation error.
- expected_behavior: `get_relevant_documents(...)` should return retrieved documents for the question.
- actual_behavior: The retriever crashes during query generation with a validation error for `LineList`.
- primary_error: `ValidationError: LineList expected dict not int`

## reproduction_type_prediction
- predicted_type: minimal
- rationale: The visible failure is in the structured-output parsing path. That parser mismatch can be reproduced locally without loading documents from the web or calling OpenAI embeddings.

## environment
- language_runtime: Python
- package_versions: Exact versions were not fully listed in the captured excerpt.
- operating_system: Windows was shown in the traceback paths.
- llm_provider_or_external_service: OpenAI key and chat model were used in the example, but the parser mismatch can be reproduced locally.
- other_constraints: Trigger occurs during `MultiQueryRetriever.generate_queries(...)`.

## trigger_conditions
- required_inputs: A parser input in the wrong shape, such as an `int` where the parser expects a mapping or structured object.
- required_configuration: Multi-query retrieval path using the line-list structured parser.
- required_execution_flow: Generate alternate queries from an LLM response, then parse the structured result.

## evidence_from_issue
- explicit_reproduction_steps:
  - Load and split documents.
  - Build FAISS retriever.
  - Construct `MultiQueryRetriever.from_llm(...)`.
  - Call `get_relevant_documents(...)`.
- code_snippets:
  - |
    advanced_retriever = MultiQueryRetriever.from_llm(retriever=retriever, llm=primary_qa_llm)
    print(advanced_retriever.get_relevant_documents("Where is nyc?"))
- error_messages:
  - `TypeError: 'int' object is not iterable`
  - `ValidationError: LineList expected dict not int`

## fact_vs_inference
- facts:
  - The issue used `MultiQueryRetriever.from_llm(...)`.
  - The stack trace shows parsing failed before retrieval completed.
  - The parser reported `LineList expected dict not int`.
- inferences:
  - The root cause is a mismatch between the LLM output shape and the parser's expected structure.

## scope_decision
- chosen_bug_scope: Reproduce the parser shape mismatch that crashes query generation.
- excluded_noise_or_secondary_issues: Web loading, embeddings, FAISS indexing, and OpenAI networking are excluded because the shown failure occurs at the parse boundary.

## reproduction_guidance_for_agent
- minimal_repro_core: Feed a non-mapping object into a parser that expects a structured line-list payload.
- must_use_real_dependency: no
- external_network_required: no
- mocking_allowed: yes
- smallest_viable_artifacts:
  - reproduce.py
  - README.md
