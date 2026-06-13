# Normalized Issue Summary

## issue_metadata
- project: LangChain
- repository: langchain-ai/langchain
- issue_number: 2252
- issue_url: https://github.com/langchain-ai/langchain/issues/2252
- title: Toolkits - Pandas Dataframe Agent failed to call "python_repl_ast" consistently
- author: 未提供
- created_at: 2023-04-01T01:14:39Z

## bug_overview
- one_sentence_summary: The Pandas dataframe agent sometimes emits natural-language tool names instead of the exact `python_repl_ast` tool name, causing repeated invalid-tool errors.
- expected_behavior: The agent should consistently choose the exact `python_repl_ast` tool for dataframe inspection queries.
- actual_behavior: For some prompts the agent invents tool names such as `Use pandas boolean indexing...` or `Use python_repl_ast to execute the previous input.`
- primary_error: `... is not a valid tool, try another one.`

## reproduction_type_prediction
- predicted_type: minimal
- rationale: The core failure is inconsistent tool-name selection and can be modeled locally without a real dataframe or LangChain runtime.

## environment
- language_runtime: Python
- package_versions: 未提供
- operating_system: 未提供
- llm_provider_or_external_service: 未提供
- other_constraints: The issue concerns the Pandas Dataframe Agent and the `python_repl_ast` tool

## trigger_conditions
- required_inputs: A dataframe-related question phrased differently from the successful example
- required_configuration: Dataframe agent with `python_repl_ast` as the valid tool
- required_execution_flow: The model chooses a descriptive sentence instead of the exact tool name

## evidence_from_issue
- explicit_reproduction_steps:
  - Ask `how many rows`
  - Observe correct use of `python_repl_ast`
  - Ask `does fg-40f support local report`
  - Observe invalid tool names and repeated retries
- code_snippets:
  - `Action: python_repl_ast`
  - `Action: Use pandas boolean indexing to filter the dataframe...`
  - `Action: Use python_repl_ast to execute the previous input.`
- error_messages:
  - `... is not a valid tool, try another one.`

## fact_vs_inference
- facts:
  - One query correctly selects `python_repl_ast`
  - Another query produces descriptive tool names instead of exact tool identifiers
  - Invalid-tool errors follow
- inferences:
  - The tool-selection prompt is brittle to wording changes and not constrained enough to exact tool names

## scope_decision
- chosen_bug_scope: Reproduce the invalid-tool failure caused by non-exact tool names.
- excluded_noise_or_secondary_issues: Real dataframe contents and pandas execution are excluded because the issue is already visible before any real tool execution happens.

## reproduction_guidance_for_agent
- minimal_repro_core: Compare one successful exact-tool output against one invalid natural-language tool output and show the invalid-tool rejection.
- must_use_real_dependency: no
- external_network_required: no
- mocking_allowed: yes
- smallest_viable_artifacts:
  - reproduce.py
  - README.md
