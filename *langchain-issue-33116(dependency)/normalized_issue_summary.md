# Normalized Issue Summary

## issue_metadata
- project: langchain
- issue_url: https://github.com/langchain-ai/langchain/issues/33116
- title: Ollama not able to do structured outputs for gpt-oss (upstream issue)

## bug_overview
- one_sentence_summary: `ChatOllama(model="gpt-oss:20b").with_structured_output(..., method="json_schema")` can fail because the returned text is not valid JSON for the structured-output parser.
- expected_behavior: Structured output invocation should return a parsed `Joke` object.
- actual_behavior: The parser receives non-JSON text and raises an output parsing failure rooted in `JSONDecodeError`.
- primary_error: `langchain_core.exceptions.OutputParserException: Invalid json output`

## reproduction_type_prediction
- predicted_type: real_dependency
- rationale: The issue is reported as model-specific to Ollama `gpt-oss:20b`; the same code works for other models. A faithful reproduction depends on actual provider/model behavior.

## environment
- language_runtime: Python 3.12
- package_versions: `langchain_core 0.3.76`, `langsmith 0.4.31`, `langchain_ollama 0.3.8`, `langchain_openai 0.3.33`
- operating_system: Linux Ubuntu 22.04
- llm_provider_or_external_service: Ollama with `gpt-oss:20b`; comparison cases mention OpenAI and Ollama `llama3.1:8b`
- other_constraints: Structured output uses Pydantic schema and `method="json_schema"`

## trigger_conditions
- required_inputs: A prompt such as `Tell me a joke about cats`
- required_configuration: `ChatOllama(model="gpt-oss:20b", reasoning=True).with_structured_output(Joke, method="json_schema")`
- required_execution_flow: Invoke the structured LLM and let LangChain parse the returned text as JSON

## evidence_from_issue
- explicit_reproduction_steps:
  - Define a Pydantic `Joke` model
  - Create `ChatOllama(model="gpt-oss:20b", reasoning=True)`
  - Wrap it with `.with_structured_output(Joke, method="json_schema")`
  - Call `.invoke("Tell me a joke about cats")`
- code_snippets:
  - |
    llm = ChatOllama(model="gpt-oss:20b", reasoning=True)
    structured_llm = llm.with_structured_output(Joke, method="json_schema")
    response = structured_llm.invoke("Tell me a joke about cats")
- error_messages:
  - `json.decoder.JSONDecodeError: Expecting value: line 1 column 1 (char 0)`
  - `langchain_core.exceptions.OutputParserException: Invalid json output`

## fact_vs_inference
- facts:
  - The issue reproduces with `gpt-oss:20b` on Ollama.
  - The reporter says it does not reproduce with `llama3.1:8b` or OpenAI.
  - The failure happens while parsing JSON structured output.
- inferences:
  - The returned text likely contains reasoning or another non-JSON payload that the JSON parser cannot consume.

## scope_decision
- chosen_bug_scope: Reproduce the structured-output parsing failure caused by non-JSON text from the provider/model boundary.
- excluded_noise_or_secondary_issues: GPU hardware details and unrelated successful models are excluded except where they help establish that this is model-specific.

## reproduction_guidance_for_agent
- minimal_repro_core: Feed non-JSON provider output into the same parse boundary used by structured output and show the parsing failure.
- must_use_real_dependency: yes
- external_network_required: no
- mocking_allowed: no
- smallest_viable_artifacts:
  - reproduce.py
  - README.md
