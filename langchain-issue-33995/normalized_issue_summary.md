# Normalized Issue Summary

## issue_metadata
- project: langchain
- issue_url: https://github.com/langchain-ai/langchain/issues/33995
- title: ChatGroq setting wrong toolcall flag in resulting API call.

## bug_overview
- one_sentence_summary: `ChatGroq(...).with_structured_output(...)` can send a request that requires a tool call even when the model returns plain JSON without calling a tool, causing Groq to reject the request.
- expected_behavior: Structured parsing should succeed when the model returns valid schema-shaped JSON, or the request should not require an unnecessary tool call.
- actual_behavior: Groq returns HTTP 400 `tool_use_failed` because the request requires a tool call but the model did not emit one.
- primary_error: `BadRequestError: Tool choice is required, but model did not call a tool`

## reproduction_type_prediction
- predicted_type: real_dependency
- rationale: The issue depends on Groq request semantics and intermittent provider/model behavior for `openai/gpt-oss-20b`.

## environment
- language_runtime: Python 3.13.5
- package_versions: `langchain_core 1.0.4`, `langchain 1.0.5`, `langsmith 0.4.42`, `langchain_groq 1.0.1`, `groq 0.34.1`
- operating_system: Windows
- llm_provider_or_external_service: Groq API using model `openai/gpt-oss-20b`
- other_constraints: The prompt explicitly tells the model it does not need tools

## trigger_conditions
- required_inputs: Structured parsing prompt over music metadata
- required_configuration: `ChatGroq(...).with_structured_output(Track)`
- required_execution_flow: Send a structured-output request where the API requires a tool call, but the model instead returns ordinary JSON text

## evidence_from_issue
- explicit_reproduction_steps:
  - Define a Pydantic `Track` model
  - Create `ChatGroq(model="openai/gpt-oss-20b", temperature=0, api_key=...)`
  - Wrap it with `.with_structured_output(Track)`
  - Invoke it on the provided system and human messages
- code_snippets:
  - |
    llm = ChatGroq(model="openai/gpt-oss-20b", temperature=0, api_key=GROQ_API_KEY).with_structured_output(Track)
    llm.invoke(message)
- error_messages:
  - `BadRequestError: Error code: 400`
  - `Tool choice is required, but model did not call a tool`

## fact_vs_inference
- facts:
  - The provider error says the model output was valid but no tool was called.
  - The issue is intermittent.
  - The reporter says `tool_choice="none"` only helped sometimes.
- inferences:
  - LangChain is likely setting tool-choice/request flags inconsistently for this structured-output path.

## scope_decision
- chosen_bug_scope: Reproduce the provider-level contract mismatch between required tool use and plain JSON output.
- excluded_noise_or_secondary_issues: Detailed prompt wording and downstream parsing logic are secondary to the request contract failure.

## reproduction_guidance_for_agent
- minimal_repro_core: Show a request contract that requires a tool call, then simulate a provider response that contains valid JSON but no tool call.
- must_use_real_dependency: yes
- external_network_required: yes
- mocking_allowed: no
- smallest_viable_artifacts:
  - reproduce.py
  - README.md
