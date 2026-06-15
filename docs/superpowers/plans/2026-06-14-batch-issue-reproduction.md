# Batch Issue Reproduction Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build normalized summaries and reproduction artifacts for the requested LangChain, CrewAI, and Codex issues using the repository's required two-stage workflow.

**Architecture:** Each issue lives in its own directory with a fixed artifact set: a stage-A normalized summary plus stage-B runnable reproduction files. The process is split into repository convention discovery, issue fact extraction, reproduction generation, and verification so failures can be isolated per issue.

**Tech Stack:** Markdown, Python, shell utilities, repository-local files

---

### Task 1: Inspect Repository Conventions

**Files:**
- Modify: `docs/superpowers/plans/2026-06-14-batch-issue-reproduction.md`
- Read: `prompt.md`
- Read: existing issue `README.md` files

- [ ] **Step 1: Review the workflow prompt**

Run: `sed -n '1,260p' prompt.md`
Expected: the two-stage Stage A / Stage B workflow and fixed normalized summary structure are visible.

- [ ] **Step 2: Review representative existing issue directories**

Run: `sed -n '1,220p' langchain-issue-2252/README.md`
Expected: an existing reproduction README showing repository style and naming patterns.

- [ ] **Step 3: Review Codex issue directories before rewriting**

Run: `find codex -maxdepth 2 -type f | sort`
Expected: the current Codex reproduction files that need to be rebuilt are listed.

### Task 2: Produce Stage A Summaries

**Files:**
- Create: `langchain-issue-11408/normalized_issue_summary.md`
- Create: `langchain-issue-12077/normalized_issue_summary.md`
- Create: `langchain-issue-17352/normalized_issue_summary.md`
- Create: `langchain-issue-19699/normalized_issue_summary.md`
- Create: `langchain-issue-21482/normalized_issue_summary.md`
- Create: `crewai-issue-3821/normalized_issue_summary.md`
- Create: `crewai-issue-3843/normalized_issue_summary.md`
- Create: `crewai-issue-3873/normalized_issue_summary.md`
- Create: `crewai-issue-3889/normalized_issue_summary.md`
- Create: `crewai-issue-3915/normalized_issue_summary.md`
- Create: `crewai-issue-3925/normalized_issue_summary.md`
- Create: `codex/codex-issue-666/normalized_issue_summary.md`
- Create: `codex/codex-issue-802/normalized_issue_summary.md`

- [ ] **Step 1: Gather issue facts**

Run: collect the issue title, body, environment, code, errors, and relevant comments for each target issue.
Expected: enough evidence to classify each issue as `minimal` or `real_dependency` without inventing missing details.

- [ ] **Step 2: Write normalized summaries**

Write one `normalized_issue_summary.md` per issue using the exact section names from `prompt.md`.
Expected: every summary includes issue metadata, bug overview, reproduction type prediction, environment, trigger conditions, issue evidence, fact-vs-inference, scope decision, and reproduction guidance.

- [ ] **Step 3: Verify summary structure**

Run: `rg -n "^## " */normalized_issue_summary.md codex/*/normalized_issue_summary.md`
Expected: each summary shows the required fixed headings.

### Task 3: Generate Stage B Reproductions

**Files:**
- Create or modify: each target issue directory `README.md`
- Create or modify: each target issue directory `reproduce.py`
- Create as needed: `requirements.txt`, `requirements-*.txt`, or equivalent minimal dependency files

- [ ] **Step 1: Decide reproduction mode from Stage A**

For each issue, read its `reproduction_type_prediction` and `reproduction_guidance_for_agent` fields.
Expected: a clear choice between minimal repro and real-dependency repro, with README notes if the prediction must be overridden.

- [ ] **Step 2: Write minimal runnable scripts**

Implement one focused `reproduce.py` per issue that triggers the bug path or the nearest justified approximation from the normalized summary.
Expected: each script is short, readable, and only depends on declared inputs and dependencies.

- [ ] **Step 3: Write step-by-step READMEs**

Document environment setup, install commands, run commands, expected result, actual result, repro type, and any missing information or API key placeholders.
Expected: a user can follow the README without guessing hidden setup.

- [ ] **Step 4: Add dependency manifests only where necessary**

Create dependency files only when the script requires installed packages or version pinning to make the bug meaningful.
Expected: no unnecessary manifests in purely standard-library reproductions.

### Task 4: Rebuild Existing Codex Reproductions

**Files:**
- Modify: `codex/codex-issue-666/README.md`
- Modify: `codex/codex-issue-666/reproduce.py`
- Modify: `codex/codex-issue-802/README.md`
- Modify: `codex/codex-issue-802/reproduce.py`
- Create if missing: matching `normalized_issue_summary.md`

- [ ] **Step 1: Inspect current Codex repro content**

Run: `find codex -maxdepth 2 -type f | sort`
Expected: a concrete list of files to rewrite under `codex/`.

- [ ] **Step 2: Reapply the two-stage workflow**

Create fresh normalized summaries, then regenerate README and reproduction scripts from those summaries.
Expected: Codex directories match the same structure and quality bar as the new LangChain and CrewAI directories.

- [ ] **Step 3: Leave API-key fields blank where needed**

Use empty environment variable examples such as `OPENAI_API_KEY=` rather than real values.
Expected: no secrets are introduced and the limitation is documented.

### Task 5: Verify Generated Artifacts

**Files:**
- Modify if needed: any generated README or script that fails basic execution

- [ ] **Step 1: Run syntax checks for Python scripts**

Run: `python3 -m compileall langchain-issue-* crewai-issue-* codex/codex-issue-*`
Expected: compilation succeeds for generated Python files.

- [ ] **Step 2: Spot-run representative reproductions**

Run a subset of generated scripts spanning minimal and real-dependency styles.
Expected: they execute to the documented failure or explanatory output path.

- [ ] **Step 3: Review file inventory**

Run: `find langchain-issue-* crewai-issue-* codex/codex-issue-* -maxdepth 1 -type f | sort`
Expected: each target directory contains the expected stage A and stage B files.
