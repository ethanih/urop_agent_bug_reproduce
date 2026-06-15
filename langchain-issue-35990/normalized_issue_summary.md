# Normalized Issue Summary

## issue_metadata
- project: langchain
- issue_url: https://github.com/langchain-ai/langchain/issues/35990
- title: Non-dict tool arguments should be set invalid

## bug_overview
- one_sentence_summary: Tool-call arguments that deserialize successfully but are not dictionaries can still be treated as valid tool calls, even though `AIMessage.tool_calls` requires dict args.
- expected_behavior: Non-dict deserialized args should be converted into `invalid_tool_calls`.
- actual_behavior: Non-dict args can propagate into the valid tool-call path and later trigger validation problems.
- primary_error: `ValidationError of AIMessage` is described; no concrete traceback was included

## reproduction_type_prediction
- predicted_type: minimal
- rationale: The bug is in local response conversion logic and does not require a real OpenAI response.

## environment
- language_runtime: Python 3.13.11
- package_versions: `langchain 1.2.8`, `langchain_core 1.2.8`, `langchain_openai 1.1.7`, `openai 2.13.0`
- operating_system: Linux Ubuntu 24.04
- llm_provider_or_external_service: OpenAI package mentioned, but provider access is not needed for the logic bug
- other_constraints: The response conversion path calls `json.loads(output.arguments, strict=False)`

## trigger_conditions
- required_inputs: Tool-call arguments that decode as JSON but produce a non-dict value such as a list or number
- required_configuration: Response conversion into LangChain `AIMessage.tool_calls`
- required_execution_flow: Deserialize arguments and classify them as valid or invalid tool calls

## evidence_from_issue
- explicit_reproduction_steps:
  - Feed a response output whose `arguments` field decodes to a non-dict JSON value
  - Let the conversion function classify the tool call
- code_snippets:
  - |
    args = json.loads(output.arguments, strict=False)
    if not isinstance(args, dict):
        raise TypeError("Arguments must be a dictionary")
- error_messages:
  - `ValidationError of AIMessage` was described but not pasted verbatim

## fact_vs_inference
- facts:
  - The issue body states `AIMessage.tool_calls` requires `args: dict[str, Any]`.
  - The issue body highlights non-dict JSON values as problematic.
- inferences:
  - Any conversion path that lets a non-dict value through as a valid tool call is a contract bug.

## scope_decision
- chosen_bug_scope: Reproduce misclassification of non-dict JSON arguments in the tool-call conversion path.
- excluded_noise_or_secondary_issues: Provider-specific response details are excluded because the conversion bug is local.

## reproduction_guidance_for_agent
- minimal_repro_core: Deserialize a JSON list or number and show that it must be marked invalid rather than treated as a valid tool call.
- must_use_real_dependency: no
- external_network_required: no
- mocking_allowed: yes
- smallest_viable_artifacts:
  - reproduce.py
  - README.md
