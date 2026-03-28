# v0.10 Roadmap Notes

Use this file when the task is about deepening the next stage of ScholarAgents.

## Models Direction

Current foundation already includes:

- `BaseModelClient`
- `MockModelClient`
- `OpenAIModelClient`
- generation config
- parser
- retry policy
- usage tracker

Likely next improvements:

- richer response parsing
- better OpenAI output handling
- stronger call auditing
- cleaner provider-specific metadata

## Retrieval Direction

Current retrieval work should evolve toward:

- literature search in the main literature flow
- retriever metadata written to `skill_records`
- richer paper records: title, summary, year, authors, source
- optional ranking / filtering
- future real connectors without breaking local mock development

## Good v0.10 Tasks

- enrich `PaperSearchSkill` and connector outputs
- use search results to condition literature summaries
- add retrieval information to artifacts or shared memory
- improve search query construction with model assistance
- add tests around workflow + retrieval behavior
