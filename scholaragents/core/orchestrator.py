from __future__ import annotations

from scholaragents.agents.experiment_agent import ExperimentAgent
from scholaragents.agents.general_agent import GeneralAgent
from scholaragents.agents.literature_agent import LiteratureAgent
from scholaragents.agents.writing_agent import WritingAgent
from scholaragents.config import load_generation_config
from scholaragents.core.artifact import Artifact, ArtifactSection
from scholaragents.core.planner import WorkflowPlanner
from scholaragents.memory.short_term_memory import ShortTermMemory
from scholaragents.mcp.arxiv_mcp import ArxivMCPClient
from scholaragents.models import create_model_client
from scholaragents.models.response_parser import ResponseParser
from scholaragents.models.retry_policy import RetryPolicy
from scholaragents.models.usage_tracker import UsageTracker
from scholaragents.skills.experiment_planning import ExperimentPlanningSkill
from scholaragents.skills.outline_generation import OutlineGenerationSkill
from scholaragents.skills.paper_search import PaperSearchSkill
from scholaragents.skills.paper_summary import PaperSummarySkill
from scholaragents.skills.result_formatting import ResultFormattingSkill
from scholaragents.workflows.experiment_design_workflow import ExperimentDesignWorkflow
from scholaragents.workflows.literature_review_workflow import LiteratureReviewWorkflow
from scholaragents.workflows.paper_writing_workflow import PaperWritingWorkflow
from .context import TaskContext
from .registry import AgentRegistry
from .router import AgentRouter


class MultiAgentSystem:
    """Minimal orchestrator for the v0.1 multi-agent prototype."""

    def __init__(self) -> None:
        self.registry = AgentRegistry()
        self.generation_config = load_generation_config()
        self.response_parser = ResponseParser()
        self.usage_tracker = UsageTracker()
        self.retry_policy = RetryPolicy(max_retries=1, retry_delay=0.5)
        self.model_client = create_model_client(
            provider=self.generation_config.provider,
            config=self.generation_config,
            parser=self.response_parser,
            usage_tracker=self.usage_tracker,
            retry_policy=self.retry_policy,
        )
        self.retrieval_client = ArxivMCPClient()
        self.result_formatter = ResultFormattingSkill()
        self.planner = WorkflowPlanner()
        self._register_default_agents()
        self.router = AgentRouter(self.registry)
        self.short_term_memory = ShortTermMemory()

    def _register_default_agents(self) -> None:
        self.registry.register(
            LiteratureAgent(
                paper_search=PaperSearchSkill(client=self.retrieval_client),
                paper_summary=PaperSummarySkill(model_client=self.model_client),
                result_formatter=self.result_formatter,
            )
        )
        self.registry.register(
            WritingAgent(
                outline_generation=OutlineGenerationSkill(model_client=self.model_client),
                result_formatter=self.result_formatter,
            )
        )
        self.registry.register(
            ExperimentAgent(
                experiment_planning=ExperimentPlanningSkill(model_client=self.model_client),
                result_formatter=self.result_formatter,
            )
        )
        self.registry.register(GeneralAgent())

    def _should_use_literature_review_workflow(self, query: str) -> bool:
        lowered = query.lower()
        literature_terms = (
            "文献",
            "论文",
            "literature",
            "paper",
            "survey",
            "related work",
        )
        review_intent_terms = (
            "综述",
            "文献调研",
            "调研",
            "研究现状",
            "现状",
            "综述框架",
            "related work",
            "review",
            "整理",
            "梳理",
            "总结",
            "归纳",
            "框架",
        )
        has_literature = any(word in lowered for word in literature_terms)
        has_review_intent = any(word in lowered for word in review_intent_terms)
        return has_literature and has_review_intent

    def _matched_keywords(self, query: str, terms: tuple[str, ...]) -> list[str]:
        lowered = query.lower()
        return [term for term in terms if term in lowered]

    def _should_use_experiment_design_workflow(self, query: str) -> bool:
        lowered = query.lower()
        experiment_terms = ("实验", "experiment", "baseline", "消融", "ablation", "指标", "metric")
        writing_terms = ("写", "写作", "methods", "experiments", "实验部分", "章节", "section")
        has_experiment = any(word in lowered for word in experiment_terms)
        has_writing = any(word in lowered for word in writing_terms)
        return has_experiment and has_writing

    def _should_use_paper_writing_workflow(self, query: str) -> bool:
        lowered = query.lower()
        writing_terms = (
            "写作",
            "写",
            "润色",
            "draft",
            "introduction",
            "methods",
            "章节",
            "论文",
        )
        grounding_terms = (
            "文献",
            "related work",
            "introduction",
            "引言",
            "背景",
            "论文",
        )
        has_writing = any(word in lowered for word in writing_terms)
        has_grounding = any(word in lowered for word in grounding_terms)
        return has_writing and has_grounding

    def _select_workflow(self, query: str) -> str | None:
        experiment_terms = ("实验", "experiment", "baseline", "消融", "ablation", "指标", "metric")
        experiment_writing_terms = ("写", "写作", "methods", "experiments", "实验部分", "章节", "section")
        writing_terms = ("写作", "写", "润色", "draft", "introduction", "methods", "章节", "论文")
        grounding_terms = ("文献", "related work", "introduction", "引言", "背景", "论文")
        literature_terms = ("文献", "论文", "literature", "paper", "survey", "related work")
        review_terms = ("综述", "文献调研", "调研", "研究现状", "现状", "综述框架", "related work", "review", "整理", "梳理", "总结", "归纳", "框架")

        candidates: list[tuple[str, list[str]]] = []
        experiment_hits = self._matched_keywords(query, experiment_terms) + self._matched_keywords(query, experiment_writing_terms)
        if self._should_use_experiment_design_workflow(query):
            candidates.append(("experiment_design_workflow", experiment_hits))

        paper_hits = self._matched_keywords(query, writing_terms) + self._matched_keywords(query, grounding_terms)
        if self._should_use_paper_writing_workflow(query):
            candidates.append(("paper_writing_workflow", paper_hits))

        literature_hits = self._matched_keywords(query, literature_terms) + self._matched_keywords(query, review_terms)
        if self._should_use_literature_review_workflow(query):
            candidates.append(("literature_review_workflow", literature_hits))

        if not candidates:
            return None

        self._last_workflow_candidates = candidates
        return candidates[0][0]

    def _build_workflow_reason(self, workflow_name: str, query: str) -> str:
        lowered = query.lower()
        if workflow_name == "paper_writing_workflow":
            strong_terms = [term for term in ("写", "introduction", "related work") if term in lowered]
            joined = ", ".join(strong_terms) or "writing intent"
            return f"query contains stronger writing intent ({joined})"
        if workflow_name == "experiment_design_workflow":
            strong_terms = [term for term in ("实验", "experiments", "章节") if term in lowered]
            joined = ", ".join(strong_terms) or "experiment-writing intent"
            return f"query combines experiment planning and writing needs ({joined})"
        return "query is more aligned with literature synthesis intent"

    def _build_workflow(self, workflow_name: str):
        if workflow_name == "literature_review_workflow":
            return LiteratureReviewWorkflow(
                literature_agent=self.registry.get("literature_agent"),
                writing_agent=self.registry.get("writing_agent"),
                general_agent=self.registry.get("general_agent"),
                result_formatter=self.result_formatter,
            )
        if workflow_name == "experiment_design_workflow":
            return ExperimentDesignWorkflow(
                experiment_agent=self.registry.get("experiment_agent"),
                writing_agent=self.registry.get("writing_agent"),
                general_agent=self.registry.get("general_agent"),
                result_formatter=self.result_formatter,
            )
        if workflow_name == "paper_writing_workflow":
            return PaperWritingWorkflow(
                literature_agent=self.registry.get("literature_agent"),
                writing_agent=self.registry.get("writing_agent"),
                general_agent=self.registry.get("general_agent"),
                result_formatter=self.result_formatter,
            )
        raise LookupError(f"Unknown workflow: {workflow_name}")

    def handle(self, user_id: str, query: str) -> dict:
        ctx = TaskContext(user_id=user_id, query=query)
        ctx.shared_memory["model_provider"] = self.model_client.provider
        ctx.shared_memory["model_name"] = self.model_client.model_name
        ctx.log(f"Received query from user '{user_id}'")
        ctx.add_message("user", query)

        workflow_name = self._select_workflow(query)
        if workflow_name is not None:
            candidate_names = [name for name, _ in getattr(self, "_last_workflow_candidates", [])]
            ctx.log(f"Candidate workflows: {', '.join(candidate_names)}")
            for candidate_name, keywords in getattr(self, "_last_workflow_candidates", []):
                joined = ", ".join(dict.fromkeys(keywords))
                ctx.log(f"Workflow candidate matched by keywords: {joined} -> {candidate_name}")
            ctx.log(f"Selected workflow: {workflow_name}")
            ctx.log(f"Reason: {self._build_workflow_reason(workflow_name, query)}")
            plan = self.planner.generate_plan(workflow_name)
            ctx.shared_memory["task_plan"] = plan
            ctx.shared_memory["selected_workflow"] = workflow_name
            ctx.log(f"Generated execution plan for {workflow_name}")
            for item in plan:
                ctx.log(
                    f"Plan step {item['step']}: {item['agent']} -> {item['action']}"
                )
            workflow = self._build_workflow(workflow_name)
            workflow_output = workflow.run(ctx)
            self.short_term_memory.set("last_query", query)
            self.short_term_memory.set("last_mode", "workflow")
            self.short_term_memory.set("last_result", workflow_output["result"])
            ctx.add_message("assistant", workflow_output["result"])
            return {
                "selected_agent": "workflow",
                "workflow_triggered": True,
                "workflow_name": workflow_output["workflow_name"],
                "artifact": workflow_output.get("artifact"),
                "result": workflow_output["result"],
                "traces": ctx.traces,
                "shared_memory": workflow_output["shared_memory"],
            }

        agent = self.router.route(ctx)
        ctx.log(f"Executing agent: {agent.name}")
        result = agent.run(ctx)
        ctx.add_message("assistant", result)
        ctx.log("Execution finished")
        self.short_term_memory.set("last_query", query)
        self.short_term_memory.set("last_mode", "single_agent")
        self.short_term_memory.set("last_result", result)

        artifact = Artifact(
            title=f"{agent.name} Output",
            sections=[
                ArtifactSection(name="Primary Result", content=result),
            ],
            next_actions=["如需更细化输出，可进一步触发 workflow 协作。"],
            raw_text=result,
        )

        return {
            "selected_agent": agent.name,
            "workflow_triggered": False,
            "workflow_name": None,
            "artifact": artifact.to_dict(),
            "result": result,
            "traces": ctx.traces,
            "shared_memory": {},
        }
