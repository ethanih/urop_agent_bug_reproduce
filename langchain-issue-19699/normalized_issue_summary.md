# Normalized Issue Summary

## issue_metadata
- project: langchain
- issue_url: https://github.com/langchain-ai/langchain/issues/19699
- title: Received JSONDecodeError Expecting property name enclosed in double quotes

## bug_overview
- one_sentence_summary: Structured output routing fails because the model returns JSON-like text with unquoted property names, which `json.loads(...)` rejects.
- expected_behavior: `with_structured_output(...)` should parse the routing decision into a `RouteQuery` object.
- actual_behavior: The router crashes with a `JSONDecodeError`.
- primary_error: `JSONDecodeError Expecting property name enclosed in double quotes`

## reproduction_type_prediction
- predicted_type: minimal
- rationale: The core failure is invalid JSON syntax in model output. That can be reproduced locally without Azure or the full notebook.

## environment
- language_runtime: Python 3.11
- package_versions: `langchain==0.0.352`, `langchain-community==0.0.5`, `langchain-core==0.1.2`; issue text also listed newer pyproject pins.
- operating_system: 未提供
- llm_provider_or_external_service: `AzureChatOpenAI`
- other_constraints: The structured output schema used a `RouteQuery` model with `datasource` literal values.

## trigger_conditions
- required_inputs: A router output such as `{ datasource: "python_docs" }` instead of valid JSON.
- required_configuration: Structured output parsing path with a JSON decoder.
- required_execution_flow: Ask the router to choose a datasource, then parse the model output as JSON.

## evidence_from_issue
- explicit_reproduction_steps:
  - Build a router with `with_structured_output(RouteQuery)`.
  - Invoke it with a question.
  - Observe the invalid JSON parse failure.
- code_snippets:
  - |
    class RouteQuery(BaseModel):
        datasource: Literal["python_docs", "js_docs", "golang_docs"]
    structured_llm = llm.with_structured_output(RouteQuery)
- error_messages:
  - `{ datasource: "python_docs" } are not valid JSON. Received JSONDecodeError Expecting property name enclosed in double quotes`

## fact_vs_inference
- facts:
  - The issue used `AzureChatOpenAI`.
  - The reported invalid payload was `{ datasource: "python_docs" }`.
  - The parser failed with `JSONDecodeError`.
- inferences:
  - The bug is triggered by the model/provider returning JSON-like text instead of strict JSON.

## scope_decision
- chosen_bug_scope: Reproduce the invalid JSON parsing failure on unquoted object keys.
- excluded_noise_or_secondary_issues: The full notebook and retrieval stack are excluded because the visible failure is the JSON parse boundary.

## reproduction_guidance_for_agent
- minimal_repro_core: Call `json.loads(...)` on `{ datasource: "python_docs" }`.
- must_use_real_dependency: no
- external_network_required: no
- mocking_allowed: yes
- smallest_viable_artifacts:
  - reproduce.py
  - README.md
