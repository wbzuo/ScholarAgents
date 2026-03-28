from __future__ import annotations

from scholaragents.core.base_agent import BaseAgent
from scholaragents.core.context import TaskContext
from scholaragents.skills.experiment_planning import ExperimentPlanningSkill
from scholaragents.skills.result_formatting import ResultFormattingSkill


class ExperimentAgent(BaseAgent):
    def __init__(
        self,
        experiment_planning: ExperimentPlanningSkill,
        result_formatter: ResultFormattingSkill,
    ) -> None:
        super().__init__(
            name="experiment_agent",
            description="Handles experiment planning and evaluation design tasks.",
        )
        self.experiment_planning = experiment_planning
        self.result_formatter = result_formatter

    def _record_skill_call(self, ctx: TaskContext, skill_output: dict) -> None:
        ctx.shared_memory.setdefault("skill_records", {}).setdefault(self.name, []).append(
            {
                "skill_name": skill_output["name"],
                "metadata": skill_output["metadata"],
            }
        )

    def can_handle(self, ctx: TaskContext) -> bool:
        keywords = (
            "实验",
            "baseline",
            "指标",
            "消融",
            "ablation",
            "experiment",
            "metric",
            "evaluation",
        )
        query = ctx.query.lower()
        return any(word in query for word in keywords)

    def run(self, ctx: TaskContext) -> str:
        ctx.log("ExperimentAgent generated an experiment-design response template")
        ctx.log("ExperimentAgent calling ExperimentPlanningSkill")
        plan_output = self.experiment_planning.execute(
            task_description=ctx.query,
            trace=ctx.log,
            workflow_name=ctx.shared_memory.get("workflow_name"),
            agent_name=self.name,
        )
        self._record_skill_call(ctx, plan_output)
        plan = plan_output["content"]
        ctx.log("ExperimentAgent calling ResultFormattingSkill")
        formatted_output = self.result_formatter.execute(
            title="这是一个面向实验设计的初步响应：",
            sections=plan["sections"],
            intro=plan.get("intro"),
        )
        self._record_skill_call(ctx, formatted_output)
        return formatted_output["content"]
