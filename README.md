# ScholarAgents

ScholarAgents is a lightweight multi-agent research assistant prototype for academic workflows. It keeps the system modular while staying easy to run locally with pure Python.

Current version: `v0.9`  
Latest release notes: [CHANGELOG.md](/Users/wbzuo/Documents/04-Developer/Source-Code/github/ScholarAgents/CHANGELOG.md)  
License: [MIT](/Users/wbzuo/Documents/04-Developer/Source-Code/github/ScholarAgents/LICENSE)

Current capabilities include:

- single-agent routing
- multi-workflow orchestration
- shared memory and execution trace
- reusable skills
- mode-aware academic writing
- lightweight planning with `task_plan`
- structured `artifact` output
- local artifact export to Markdown and JSON
- a configurable `models/` layer with `mock` and `openai` providers
- a first retrieval path for literature workflows through `PaperSearchSkill` and `ArxivMCPClient`

The default experience is intentionally safe and local-first: `MODEL_PROVIDER=mock` works without any API key and keeps the demo fully runnable.

## Quick Start

Install in editable mode:

```bash
pip install -e .
```

Run the main demo:

```bash
python examples/demo.py
```

Run with the explicit mock provider:

```bash
MODEL_PROVIDER=mock python examples/demo.py
```

## Architecture

ScholarAgents is organized as layered building blocks:

- `core/`: task context, routing, orchestration, planner, artifact structures
- `agents/`: role-oriented agents such as literature, writing, experiment, and general agents
- `skills/`: reusable capability units used by agents
- `workflows/`: multi-agent serial collaboration flows
- `memory/`: shared memory and short-term memory
- `models/`: provider-agnostic model client layer
- `artifacts/`: export and storage utilities for structured outputs

## Project Structure

```text
ScholarAgents/
├── scholaragents/
│   ├── __init__.py
│   ├── config.py
│   ├── agents/
│   │   ├── experiment_agent.py
│   │   ├── general_agent.py
│   │   ├── literature_agent.py
│   │   └── writing_agent.py
│   ├── artifacts/
│   │   ├── __init__.py
│   │   ├── artifact_store.py
│   │   └── exporters.py
│   ├── core/
│   │   ├── artifact.py
│   │   ├── base_agent.py
│   │   ├── context.py
│   │   ├── orchestrator.py
│   │   ├── planner.py
│   │   ├── registry.py
│   │   └── router.py
│   ├── memory/
│   │   ├── shared_memory.py
│   │   └── short_term_memory.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── base_model_client.py
│   │   ├── exceptions.py
│   │   ├── generation_config.py
│   │   ├── mock_client.py
│   │   ├── model_factory.py
│   │   ├── openai_client.py
│   │   ├── response_parser.py
│   │   ├── retry_policy.py
│   │   └── usage_tracker.py
│   ├── skills/
│   │   ├── base_skill.py
│   │   ├── experiment_planning.py
│   │   ├── outline_generation.py
│   │   ├── paper_summary.py
│   │   └── result_formatting.py
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── config.py
│   │   └── logger.py
│   └── workflows/
│       ├── experiment_design_workflow.py
│       ├── literature_review_workflow.py
│       └── paper_writing_workflow.py
├── examples/
│   ├── demo.py
│   └── quickstart.py
├── outputs/
│   ├── artifact_index.json
│   ├── json/
│   └── markdown/
├── README.md
└── pyproject.toml
```

## Main Components

### Agents

- `LiteratureAgent`: literature review, papers, surveys, related work
- `WritingAgent`: introduction, methods, section drafting, writing structure
- `ExperimentAgent`: experiment planning, baselines, metrics, ablations
- `GeneralAgent`: fallback agent and workflow summary agent

### Workflows

- `literature_review_workflow`
  Flow: `LiteratureAgent -> WritingAgent -> GeneralAgent`
- `paper_writing_workflow`
  Flow: `LiteratureAgent -> WritingAgent -> GeneralAgent` or `WritingAgent -> GeneralAgent`
- `experiment_design_workflow`
  Flow: `ExperimentAgent -> WritingAgent -> GeneralAgent`

### Skills

- `PaperSearchSkill`
- `PaperSummarySkill`
- `OutlineGenerationSkill`
- `ExperimentPlanningSkill`
- `ResultFormattingSkill`

### Models Layer

The `models/` package provides a unified client abstraction for skills:

- `MockModelClient`: default local provider for development and testing
- `OpenAIModelClient`: optional real model provider using the OpenAI Python SDK
- `create_model_client(...)`: provider factory
- `GenerationConfig`: shared config object
- `ResponseParser`: output cleanup
- `RetryPolicy`: simple retry wrapper
- `UsageTracker`: in-memory model call tracking
- `exceptions.py`: unified model exceptions

Skills do not need to know which provider is active. They only call `model_client.generate(...)`.

### Retrieval Layer

The current literature path also includes a lightweight retrieval step:

- `PaperSearchSkill`: skill wrapper for literature retrieval
- `ArxivMCPClient`: stub arXiv-style connector for local development

The default retrieval path remains local and deterministic so the demo can run without external services, while leaving room for future real search connectors.

## How Routing Works

For each query, the system:

1. Creates a `TaskContext`
2. Evaluates whether a workflow should be used
3. If a workflow is selected:
   - records candidate workflows and selection reason in trace
   - generates a lightweight `task_plan`
   - runs the selected workflow
4. Otherwise:
   - routes to a single agent
   - runs the selected agent directly

## Workflow Planning

Before a workflow starts, ScholarAgents generates a simple step plan and stores it in:

- `trace`
- `shared_memory["task_plan"]`

Example plan:

```text
1. LiteratureAgent -> 整理文献
2. WritingAgent -> 生成综述骨架
3. GeneralAgent -> 给出 related work 扩写建议
```

## Shared Memory

Workflow runs store structured state in shared memory:

- `task_info`
- `task_plan`
- `intermediate_results`
- `skill_records`
- `final_result`

Current `task_info` may include:

- `workflow_name`
- `selected_workflow`
- `selected_writing_mode`
- `model_provider`
- `model_name`

Literature-oriented workflows may also write retrieved paper candidates into shared memory so later agents can reuse them.

## Artifact Output

Every workflow returns a structured artifact. Single-agent runs also return a lightweight artifact for compatibility.

Artifact fields:

- `title`
- `sections`
- `next_actions`
- `raw_text`

This lets the system keep both:

- human-readable text output through `result`
- machine-friendly structured output through `artifact`

## Artifact Export

Workflow artifacts can be exported locally as:

- Markdown
- JSON

Exports are written to:

- `outputs/markdown/`
- `outputs/json/`

An index file is maintained at:

- `outputs/artifact_index.json`

The index includes:

- `workflow_name`
- `case_name`
- `query`
- `selected_writing_mode`
- `task_plan`
- `artifact_title`
- export paths

The repository currently keeps a small set of generated example outputs under [outputs/README.md](/Users/wbzuo/Documents/04-Developer/Source-Code/github/ScholarAgents/outputs/README.md) so the export pipeline is visible directly on GitHub.

## Models Usage

ScholarAgents now supports two model providers:

- `mock`
- `openai`

### Default: Mock Mode

Mock mode is the default and requires no API key.

```bash
MODEL_PROVIDER=mock python examples/demo.py
```

This is the recommended mode for:

- local development
- CI-style regression checks
- codebase iteration without external dependencies

### OpenAI Mode

OpenAI mode is optional and requires the OpenAI Python SDK plus credentials.

Install the optional dependency:

```bash
pip install -e .[openai]
```

Then run:

```bash
MODEL_PROVIDER=openai OPENAI_API_KEY=YOUR_KEY OPENAI_MODEL=gpt-5.4 python examples/demo.py
```

If `MODEL_PROVIDER=openai` is selected but the key or SDK is missing, the system uses the configured fallback behavior. By default, it falls back to `mock`.

## Environment Variables

Supported environment variables:

```bash
MODEL_PROVIDER=mock
MOCK_MODEL_NAME=mock-default
OPENAI_MODEL=gpt-5.4
OPENAI_BASE_URL=
OPENAI_API_KEY=...
MODEL_TEMPERATURE=0.2
MODEL_MAX_OUTPUT_TOKENS=600
MODEL_TIMEOUT=30
MODEL_TOP_P=1.0
MODEL_FALLBACK_TO_MOCK=true
MODEL_USE_CACHE=false
```

For OpenAI-compatible providers such as DeepSeek, set:

```bash
MODEL_PROVIDER=openai
OPENAI_BASE_URL=https://api.deepseek.com
OPENAI_MODEL=deepseek-chat
OPENAI_API_KEY=...
```

## Trace and Provider Visibility

The trace is designed to stay readable while making model usage explicit. Example entries include:

- `PaperSummarySkill using model provider: mock`
- `OutlineGenerationSkill using model provider: mock`
- `ExperimentPlanningSkill using model provider: mock`
- `OpenAI model: gpt-5.4`
- `WritingAgent calling OutlineGenerationSkill with mode=experiment_section`
- `Workflow candidate matched by keywords: related work, introduction -> paper_writing_workflow`

## Install

Basic install:

```bash
pip install -e .
```

With OpenAI support:

```bash
pip install -e .[openai]
```

## Run

Run the main demo:

```bash
python examples/demo.py
```

Run the quickstart:

```bash
python examples/quickstart.py
```

## Demo Behavior

The demo currently includes cases that cover:

- literature organization
- methods writing
- experiment planning
- general platform ideation
- literature review workflow
- paper writing workflow
- experiment design workflow

For each case, it prints:

- selected agent or workflow
- final result text
- artifact summary
- trace
- shared memory
- export paths for workflow artifacts

## Development Notes

The project intentionally keeps the implementation lightweight:

- no external workflow engine
- no database dependency
- no real tool integrations required
- simple rule-based routing and planning
- structured outputs designed for future frontend and integration work

That makes it a good base for later additions such as:

- richer memory
- skill registry
- tool integrations
- MCP connectors
- frontend views
- artifact browsing UI

## Version Direction

The current codebase has evolved from:

- v0.1: single-agent routing
- v0.2: workflow and shared memory
- v0.3-v0.5: skills, writing modes, richer workflow behavior
- v0.6: planner and task plan
- v0.7: structured artifact output
- v0.8: artifact export and artifact index
- current: `models/` layer with mock/openai support

## License

This project is licensed under the MIT License. See [LICENSE](/Users/wbzuo/Documents/04-Developer/Source-Code/github/ScholarAgents/LICENSE) for details.
