# Normalized Issue Summary

## issue_metadata
- project: langchain
- issue_url: https://github.com/langchain-ai/langchain/issues/21482
- title: AttributeError on calling LLMGraphTransformer.convert_to_graph_documents

## bug_overview
- one_sentence_summary: `LLMGraphTransformer.convert_to_graph_documents(...)` assumes the model response has a `.content` attribute, but a Bedrock-backed flow can return a plain string instead.
- expected_behavior: The transformer should convert the text chunks into graph documents.
- actual_behavior: It crashes while parsing the raw schema response.
- primary_error: `AttributeError: 'str' object has no attribute 'content'`

## reproduction_type_prediction
- predicted_type: minimal
- rationale: The visible bug is a type assumption on the response object. That contract mismatch can be reproduced locally without Bedrock, Wikipedia, or Neo4j.

## environment
- language_runtime: Python 3.10.8
- package_versions: `langchain==0.1.17`, `langchain-community==0.0.36`, `langchain-core==0.1.52`, `langchain-experimental==0.0.58`, `langchain-text-splitters==0.0.1`, `langsmith==0.1.52`
- operating_system: Windows
- llm_provider_or_external_service: AWS Bedrock using `mistral.mistral-7b-instruct-v0:2`
- other_constraints: Triggered inside `LLMGraphTransformer.process_response(...)`.

## trigger_conditions
- required_inputs: A plain string returned where the code expects an object exposing `.content`.
- required_configuration: `LLMGraphTransformer` path using JSON-repair parsing of model output.
- required_execution_flow: Call `convert_to_graph_documents(...)`, which internally parses the model response.

## evidence_from_issue
- explicit_reproduction_steps:
  - Load Wikipedia docs.
  - Split them.
  - Create `Bedrock(...)`.
  - Create `LLMGraphTransformer(llm=llm)`.
  - Call `convert_to_graph_documents(doc_chunks)`.
- code_snippets:
  - |
    llm_transformer = LLMGraphTransformer(llm=llm)
    graph_documents = llm_transformer.convert_to_graph_documents(doc_chunks)
- error_messages:
  - `AttributeError: 'str' object has no attribute 'content'`

## fact_vs_inference
- facts:
  - The reporter used Bedrock Mistral with `LLMGraphTransformer`.
  - The stack trace shows `raw_schema.content` access on a `str`.
- inferences:
  - The root cause is a response-shape mismatch between the transformer and the Bedrock-backed model wrapper.

## scope_decision
- chosen_bug_scope: Reproduce the `.content` attribute assumption failure.
- excluded_noise_or_secondary_issues: Wikipedia retrieval, text splitting, and Neo4j writing are excluded because the shown failure occurs before graph insertion.

## reproduction_guidance_for_agent
- minimal_repro_core: Call code that expects `raw_schema.content` with `raw_schema` set to a plain string.
- must_use_real_dependency: no
- external_network_required: no
- mocking_allowed: yes
- smallest_viable_artifacts:
  - reproduce.py
  - README.md
