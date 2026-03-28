---
name: scholaragents-repo
description: Use this skill when working on the ScholarAgents repository. It covers the repo architecture, the expected development workflow, the key invariants around workflows, artifacts, traces, shared memory, and how to validate changes safely before committing.
---

# ScholarAgents Repository Skill

Use this skill when the task is to modify, extend, debug, review, or document the `ScholarAgents` codebase.

## Quick Orientation

Read these files first when you need project context:

- `README.md`
- `CHANGELOG.md`
- `examples/demo.py`
- `scholaragents/core/orchestrator.py`

Read these areas when the task touches specific subsystems:

- `scholaragents/agents/` for agent behaviors
- `scholaragents/workflows/` for workflow routing and sequencing
- `scholaragents/skills/` for reusable generation capabilities
- `scholaragents/models/` for provider-facing model infrastructure
- `scholaragents/artifacts/` for export and persistence logic
- `scholaragents/memory/` for shared memory and short-term memory behavior

## What This Repository Optimizes For

ScholarAgents is a lightweight multi-agent research workflow prototype. Preserve these design goals:

- keep the architecture easy to read
- prefer plain Python over framework-heavy abstractions
- preserve backward compatibility for demo-facing outputs when practical
- keep workflows explainable through `trace`
- keep outputs machine-friendly through `artifact`
- keep workflow state inspectable through `shared_memory`

## Core Invariants

When changing the system, preserve these behaviors unless the user explicitly asks to change them:

1. Single-agent flow still works for non-workflow queries.
2. Workflow selection remains explicit and traceable.
3. Workflow runs write `task_plan` before execution.
4. Workflow results include:
   - `result`
   - `artifact`
   - `traces`
   - `shared_memory`
5. Shared memory remains structured and at minimum includes:
   - `task_info`
   - `task_plan`
   - `intermediate_results`
   - `skill_records`
   - `final_result`
6. Artifact export remains available under `outputs/markdown/` and `outputs/json/`.
7. `outputs/artifact_index.json` remains a valid index of exported workflow artifacts.

## Preferred Development Workflow

Follow this sequence for most code changes:

1. Inspect the relevant subsystem before editing.
2. Identify whether the task belongs to:
   - routing
   - workflow behavior
   - skill behavior
   - model provider behavior
   - artifact/export behavior
   - documentation
3. Make the smallest cohesive change that solves the task.
4. Run validation.
5. Check whether `README.md` or `CHANGELOG.md` should be updated.

## Validation Checklist

After meaningful code changes, prefer running:

```bash
python -m compileall scholaragents examples
python examples/demo.py
```

If you modify model-facing behavior, also verify that:

- mock mode still works without credentials
- traces still show provider-related information
- fallback behavior does not break the demo path

## Repo-Specific Guidance

### Routing and Workflow Changes

When modifying workflow selection:

- keep candidate workflow logging
- keep selection reason logging
- keep `task_plan` generation before workflow execution

If a query might match multiple workflows, make the prioritization visible in trace.

### Skill Changes

When modifying `scholaragents/skills/`:

- keep skills reusable and provider-agnostic where possible
- prefer injecting dependencies rather than hardcoding providers
- keep metadata useful because it is written to `skill_records`

If a skill uses model generation, preserve provider trace lines such as:

- `PaperSummarySkill using model provider: ...`
- `OutlineGenerationSkill using model provider: ...`
- `ExperimentPlanningSkill using model provider: ...`

### Model Layer Changes

When modifying `scholaragents/models/`:

- default behavior should remain safe in `mock` mode
- missing OpenAI credentials should not crash the default local workflow
- keep error messages clear
- keep fallback behavior understandable

### Artifact and Export Changes

When modifying `artifact` or export logic:

- preserve `title`, `sections`, `next_actions`, and `raw_text`
- preserve Markdown and JSON export compatibility
- preserve index updates in `outputs/artifact_index.json`

If changing filenames or export layout, update both:

- `README.md`
- `outputs/README.md`

## Documentation Rules

If you change behavior that users can see, consider updating:

- `README.md` for current usage or architecture
- `CHANGELOG.md` for release-facing summaries

Keep README practical. Prefer:

- what the system does
- how to run it
- what changed

Avoid adding long theoretical explanations that do not help a contributor act.

## Anti-Patterns for This Repo

Avoid these unless the user explicitly wants them:

- introducing heavy frameworks
- adding network-dependent requirements to the default path
- breaking `examples/demo.py`
- removing trace detail
- replacing structured outputs with plain strings only
- hiding workflow state in opaque objects

## Good Task Framing for This Skill

This skill is especially relevant for requests like:

- "add a new workflow"
- "improve the models layer"
- "make artifact export more useful"
- "refine trace and shared memory"
- "update README after code changes"
- "review whether this change breaks demo compatibility"

## Completion Standard

A change is in good shape when:

- the targeted behavior works
- the demo still runs unless the user intentionally changed that contract
- traces remain readable
- artifacts remain structured
- documentation matches the new behavior
