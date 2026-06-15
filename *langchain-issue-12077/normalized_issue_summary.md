# Normalized Issue Summary

## issue_metadata
- project: langchain
- issue_url: https://github.com/langchain-ai/langchain/issues/12077
- title: Running SQLDatabaseChain adds prefix "SQLQuery:\n" infront of returned SQL by LLM, causing invalid query when ran on Database using chain

## bug_overview
- one_sentence_summary: `SQLDatabaseChain` can pass an LLM-generated SQL string that still includes the prompt prefix `SQLQuery:\n`, which then breaks database execution.
- expected_behavior: The chain should execute only the SQL statement itself.
- actual_behavior: The generated text includes `SQLQuery:\nSELECT ...`, which is invalid as a raw SQL query.
- primary_error: Invalid query execution caused by the `SQLQuery:\n` prefix remaining in the SQL passed to the database.

## reproduction_type_prediction
- predicted_type: minimal
- rationale: The failure is about string post-processing, not a Snowflake-specific protocol. The bug can be reproduced by feeding prefixed SQL into a strict executor.

## environment
- language_runtime: Python
- package_versions: `langchain==0.0.319`
- operating_system: 未提供
- llm_provider_or_external_service: AWS Bedrock with Anthropic Claude v2 was reported, but not required for the core reproduction.
- other_constraints: The default SQL chain prompt format explicitly includes `SQLQuery:`.

## trigger_conditions
- required_inputs: An LLM answer whose returned SQL text still starts with `SQLQuery:\n`.
- required_configuration: SQL chain flow that forwards the raw SQL segment to the executor.
- required_execution_flow: Generate query text, then execute it against the database without stripping the label.

## evidence_from_issue
- explicit_reproduction_steps:
  - Use `SQLDatabaseChain` with AWS Bedrock Anthropic Claude 2.
  - Observe the generated SQL in verbose/debug output.
  - Execute the returned query.
- code_snippets:
  - |
    "text": " SQLQuery:\nSELECT top 5 p.productname, sum(od.quantity) as total_sold\nFROM products p\n..."
- error_messages:
  - Returned SQL contains the prefix `SQLQuery:\n`, which breaks execution on Snowflake.

## fact_vs_inference
- facts:
  - The reporter used `SQLDatabaseChain`.
  - The returned text contained `SQLQuery:\n`.
  - The reporter expected raw SQL without that prefix.
- inferences:
  - The root cause is insufficient stripping/parsing of the LLM text before execution.

## scope_decision
- chosen_bug_scope: Reproduce the invalid SQL caused by preserving the `SQLQuery:` label.
- excluded_noise_or_secondary_issues: Bedrock- and Snowflake-specific setup is excluded because the string-format bug appears before network/database execution.

## reproduction_guidance_for_agent
- minimal_repro_core: Send a string beginning with `SQLQuery:\n` into a function that expects raw SQL.
- must_use_real_dependency: no
- external_network_required: no
- mocking_allowed: yes
- smallest_viable_artifacts:
  - reproduce.py
  - README.md
