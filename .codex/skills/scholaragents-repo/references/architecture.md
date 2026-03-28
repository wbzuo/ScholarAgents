# Architecture

## Main Entry Points

- `scholaragents/core/orchestrator.py`
- `examples/demo.py`
- `scholaragents/workflows/`

## Subsystem Boundaries

- `core/`: context, routing, orchestration, planner, artifact structures
- `agents/`: role-oriented decision layer
- `skills/`: reusable capability units
- `models/`: model provider abstraction and generation utilities
- `mcp/`: external data/tool connectors
- `memory/`: task-scoped and short-term state
- `artifacts/`: export and storage

## Invariants

Preserve these unless the task explicitly changes them:

1. Single-agent flow works for non-workflow requests.
2. Workflow selection is traceable.
3. Workflow runs generate `task_plan` before execution.
4. Workflow responses include `result`, `artifact`, `traces`, and `shared_memory`.
5. Shared memory includes at least `task_info`, `task_plan`, `intermediate_results`, `skill_records`, and `final_result`.
6. Artifact export remains compatible with `outputs/markdown/`, `outputs/json/`, and `outputs/artifact_index.json`.

## Important Files by Task

### Workflow changes

- `scholaragents/core/orchestrator.py`
- `scholaragents/workflows/*.py`

### Skill changes

- `scholaragents/skills/*.py`
- `scholaragents/agents/*.py`

### Model changes

- `scholaragents/models/*.py`
- `scholaragents/config.py`

### Retrieval changes

- `scholaragents/skills/paper_search.py`
- `scholaragents/mcp/arxiv_mcp.py`
- `scholaragents/agents/literature_agent.py`
