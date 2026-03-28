---
name: scholaragents-repo
description: Use this skill when working on the ScholarAgents repository. It provides repo entry points, architecture references, workflow invariants, validation steps, and v0.10 extension guidance for models, retrieval, artifacts, and docs.
---

# ScholarAgents Repository Skill

Use this skill when modifying, extending, reviewing, debugging, or documenting the `ScholarAgents` codebase.

## Quick Start

Read these first:

- `README.md`
- `CHANGELOG.md`
- `examples/demo.py`
- `scholaragents/core/orchestrator.py`

Then read the relevant reference file:

- `references/architecture.md`
- `references/development-workflow.md`
- `references/validation-and-docs.md`
- `references/v010-roadmap.md`

## Core Rules

- Keep the default path runnable with `MODEL_PROVIDER=mock`.
- Do not break `examples/demo.py` unless the task explicitly changes that contract.
- Preserve structured outputs: `result`, `artifact`, `traces`, and `shared_memory`.
- Preserve workflow explainability through trace and `task_plan`.
- Prefer small, cohesive Python changes over framework-heavy abstraction.

## Completion Standard

A change is in good shape when:

- the requested behavior works
- demo-facing flows still run
- traces remain readable
- artifacts remain structured
- docs match the new behavior
