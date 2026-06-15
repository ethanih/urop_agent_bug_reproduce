# Normalized Issue Summary

## issue_metadata
- project: crewAI
- issue_url: https://github.com/crewAIInc/crewAI/issues/3873
- title: [BUG] Agent Final Answer includes Agent `Thought` and `Action`

## bug_overview
- one_sentence_summary: In a hierarchical crew, the manager can leak internal `Thought` and `Action` text in the final answer after a delegated task fails.
- expected_behavior: The final answer should be user-facing and should not expose internal reasoning or action markup.
- actual_behavior: The manager returns a response containing internal `Thought` and `Action` fields.
- primary_error: Final answer includes internal agent reasoning/action text instead of a clean response.

## reproduction_type_prediction
- predicted_type: minimal
- rationale: The bug is a response-formatting failure after delegated task failure. That can be reproduced by modeling a manager that forwards raw agent scratchpad text.

## environment
- language_runtime: Python 3.12
- package_versions: `crewai==0.165.0`, `crewai-tools==0.62.3`
- operating_system: macOS Sonoma
- llm_provider_or_external_service: The report mentions hierarchical crews but does not require a specific provider for the formatting bug itself.
- other_constraints: Trigger is easier to observe when a delegated task fails.

## trigger_conditions
- required_inputs: A delegated task response indicating failure.
- required_configuration: Hierarchical crew with a manager delegating to specialized agents.
- required_execution_flow: Delegate task, receive failure-like result, then generate final answer.

## evidence_from_issue
- explicit_reproduction_steps:
  - Create a hierarchical crew with a manager and multiple specialists.
  - Ask for a task that may fail.
  - Observe the manager's final answer.
- code_snippets:
  - User task example: `Fetch list of tables from postgres db`
- error_messages:
  - The issue describes final output containing `Thought` and `Action` content.

## fact_vs_inference
- facts:
  - The issue happens in a hierarchical manager/worker setup.
  - Internal `Thought` and `Action` text appears in the final answer.
- inferences:
  - The manager likely forwards or fails to sanitize the worker scratchpad on failure paths.

## scope_decision
- chosen_bug_scope: Reproduce the formatting leak of internal reasoning/action text.
- excluded_noise_or_secondary_issues: The actual database and full crew configuration are excluded because the visible bug is response formatting.

## reproduction_guidance_for_agent
- minimal_repro_core: Construct a manager response path that returns raw `Thought:` / `Action:` text after a delegate failure.
- must_use_real_dependency: no
- external_network_required: no
- mocking_allowed: yes
- smallest_viable_artifacts:
  - reproduce.py
  - README.md
