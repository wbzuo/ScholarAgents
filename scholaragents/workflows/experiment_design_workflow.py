from __future__ import annotations

from scholaragents.agents.experiment_agent import ExperimentAgent
from scholaragents.agents.general_agent import GeneralAgent
from scholaragents.agents.writing_agent import WritingAgent
from scholaragents.core.artifact import Artifact, ArtifactSection
from scholaragents.core.context import TaskContext
from scholaragents.memory.shared_memory import SharedMemory
from scholaragents.skills.result_formatting import ResultFormattingSkill


class ExperimentDesignWorkflow:
    """Workflow for turning experiment planning into paper-ready structure."""

    name = "experiment_design_workflow"

    def __init__(
        self,
        experiment_agent: ExperimentAgent,
        writing_agent: WritingAgent,
        general_agent: GeneralAgent,
        result_formatter: ResultFormattingSkill,
    ) -> None:
        self.experiment_agent = experiment_agent
        self.writing_agent = writing_agent
        self.general_agent = general_agent
        self.result_formatter = result_formatter

    def _copy_skill_records(self, ctx: TaskContext, shared_memory: SharedMemory, step_name: str) -> None:
        for record in ctx.shared_memory.get("skill_records", {}).get(step_name, []):
            shared_memory.add_skill_record(step_name, record)

    def run(self, ctx: TaskContext) -> dict:
        shared_memory = SharedMemory()
        shared_memory.set_task_info("user_id", ctx.user_id)
        shared_memory.set_task_info("query", ctx.query)
        shared_memory.set_task_info("workflow_name", self.name)
        shared_memory.set_task_info("selected_workflow", self.name)
        shared_memory.set_task_info("selected_writing_mode", "experiment_section")
        shared_memory.set_task_info("model_provider", ctx.shared_memory.get("model_provider"))
        shared_memory.set_task_info("model_name", ctx.shared_memory.get("model_name"))
        shared_memory.set_task_plan(ctx.shared_memory.get("task_plan", []))
        ctx.shared_memory["workflow_name"] = self.name
        ctx.shared_memory["selected_workflow"] = self.name
        ctx.shared_memory["selected_writing_mode"] = "experiment_section"
        ctx.log(f"Workflow started: {self.name}")

        ctx.log("Workflow step 1: ExperimentAgent")
        experiment_result = self.experiment_agent.run(ctx)
        shared_memory.set_result("experiment_agent", experiment_result)
        ctx.shared_memory["experiment_design_notes"] = experiment_result
        self._copy_skill_records(ctx, shared_memory, "experiment_agent")

        ctx.log("Workflow step 2: WritingAgent")
        writing_result = self.writing_agent.run(ctx)
        shared_memory.set_result("writing_agent", writing_result)
        ctx.shared_memory["structured_experiment_draft"] = writing_result
        self._copy_skill_records(ctx, shared_memory, "writing_agent")

        ctx.log("Workflow step 3: GeneralAgent")
        general_result = self.general_agent.run(ctx)
        shared_memory.set_result("general_agent", general_result)

        ctx.log("Workflow formatting final result with ResultFormattingSkill")
        final_result_output = self.result_formatter.execute(
            title="这是 experiment design workflow 的最终结果：",
            sections=[
                f"实验设计结果：{experiment_result}",
                f"论文写作框架：{writing_result}",
                f"综合建议：{general_result}",
            ],
        )
        shared_memory.add_skill_record(
            "workflow_final_formatting",
            {
                "skill_name": final_result_output["name"],
                "metadata": final_result_output["metadata"],
            },
        )
        final_result = final_result_output["content"]
        shared_memory.set_final_result(final_result)
        artifact = Artifact(
            title="Experiment Design Artifact",
            sections=[
                ArtifactSection(name="实验设计结果", content=experiment_result),
                ArtifactSection(name="论文写作框架", content=writing_result),
                ArtifactSection(name="综合建议", content=general_result),
            ],
            next_actions=[
                "将实验目标与假设写成 experiments 小节开头。",
                "把 baseline、指标和设置拆成独立段落。",
                "预留消融与误差分析的小节标题。",
            ],
            raw_text=final_result,
        )

        ctx.shared_memory.update(shared_memory.to_dict())
        ctx.log(f"Workflow finished: {self.name}")

        return {
            "workflow_name": self.name,
            "artifact": artifact.to_dict(),
            "result": final_result,
            "shared_memory": shared_memory.to_dict(),
        }
