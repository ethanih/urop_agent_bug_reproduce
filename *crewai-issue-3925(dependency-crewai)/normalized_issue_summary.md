# Normalized Issue Summary

## issue_metadata
- project: crewAI
- issue_url: https://github.com/crewAIInc/crewAI/issues/3925
- title: [BUG?] Hierarchical process behaves differently depending on the Language

## bug_overview
- one_sentence_summary: In hierarchical mode, an English manager prompt delegates correctly, while a Japanese version may keep delegating to itself instead of handing work to coworkers.
- expected_behavior: Delegation behavior should be semantically consistent across languages when the role, goal, and task intent are equivalent.
- actual_behavior: English delegates to the appropriate coworker, while Japanese may repeatedly self-handle or self-delegate.
- primary_error: Language-dependent delegation behavior rather than a single stack-trace error.

## reproduction_type_prediction
- predicted_type: real_dependency
- rationale: The reported bug depends on real LLM behavior, prompt interpretation, and CrewAI hierarchical delegation. A fully faithful reproduction requires a live model.

## environment
- language_runtime: Python
- package_versions: `crewai==1.5.0`
- operating_system: 未提供
- llm_provider_or_external_service: `gpt-5-nano` and `gpt-4o-mini` are mentioned.
- other_constraints: The same hierarchical crew behaves differently depending on whether the agent metadata and task descriptions are in English or Japanese.

## trigger_conditions
- required_inputs: Two semantically equivalent hierarchical crew setups, one in English and one in Japanese.
- required_configuration: `Process.hierarchical`, manager agent with delegation enabled, specialist coworkers with knowledge sources.
- required_execution_flow: Run the English inquiry and the Japanese inquiry and compare delegation traces.

## evidence_from_issue
- explicit_reproduction_steps:
  - Run the English code sample with `crewai==1.5.0`.
  - Observe manager agent delegate immediately to `Return Policy Checker`.
  - Run the Japanese code sample.
  - Observe the manager repeatedly delegate to itself or answer on its own.
- code_snippets:
  - English and Japanese crew definitions were both provided in the issue body.
- error_messages:
  - No single exception; the issue is behavior divergence in delegation traces.

## fact_vs_inference
- facts:
  - The reporter observed different delegation behavior between English and Japanese.
  - The same effect was seen with `gpt-5-nano` and `gpt-4o-mini`.
- inferences:
  - The bug likely depends on prompt interpretation and language-specific planning behavior in the live model / orchestration stack.

## scope_decision
- chosen_bug_scope: Preserve the language-dependent hierarchical delegation issue.
- excluded_noise_or_secondary_issues: No attempt is made to reduce this to a purely local deterministic parser bug because the issue's core evidence depends on live model behavior.

## reproduction_guidance_for_agent
- minimal_repro_core: Provide a runnable hierarchical CrewAI script that compares English and Japanese delegation traces.
- must_use_real_dependency: yes
- external_network_required: yes
- mocking_allowed: no
- smallest_viable_artifacts:
  - reproduce.py
  - README.md
