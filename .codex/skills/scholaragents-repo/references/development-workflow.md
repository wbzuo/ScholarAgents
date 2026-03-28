# Development Workflow

## Preferred Sequence

1. Read the relevant subsystem before editing.
2. Identify the narrowest layer that should change.
3. Prefer dependency injection over hardcoding.
4. Keep metadata useful because it is written into `skill_records`.
5. Update docs if user-visible behavior changes.

## Layer-Specific Guidance

### Workflow changes

- Keep candidate workflow logging.
- Keep workflow selection reasons in trace.
- Keep `task_plan` generation before workflow execution.

### Skill changes

- Keep skills reusable and provider-agnostic when possible.
- If a skill uses model generation, preserve provider trace lines.
- If a skill uses retrieval, record source and counts in metadata.

### Retrieval changes

- Retrieval should enrich literature flow without breaking mock-only local development.
- Prefer deterministic local stubs over mandatory network access.
- If search results are introduced, expose them through trace, `skill_records`, and `shared_memory` when useful.

### Model changes

- Default behavior should stay safe in `mock`.
- Missing OpenAI credentials must not break local development.
- Keep fallback behavior explicit and easy to understand.
