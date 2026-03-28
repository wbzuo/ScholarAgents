from __future__ import annotations

from scholaragents.agents.general_agent import GeneralAgent
from scholaragents.agents.literature_agent import LiteratureAgent
from scholaragents.agents.writing_agent import WritingAgent
from scholaragents.core.artifact import Artifact, ArtifactSection
from scholaragents.core.context import TaskContext
from scholaragents.memory.shared_memory import SharedMemory
from scholaragents.skills.result_formatting import ResultFormattingSkill


class PaperWritingWorkflow:
    """Workflow for writing-oriented tasks, optionally grounded in literature."""

    name = "paper_writing_workflow"

    def __init__(
        self,
        writing_agent: WritingAgent,
        general_agent: GeneralAgent,
        result_formatter: ResultFormattingSkill,
        literature_agent: LiteratureAgent | None = None,
    ) -> None:
        self.writing_agent = writing_agent
        self.general_agent = general_agent
        self.result_formatter = result_formatter
        self.literature_agent = literature_agent

    def _copy_skill_records(self, ctx: TaskContext, shared_memory: SharedMemory, step_name: str) -> None:
        for record in ctx.shared_memory.get("skill_records", {}).get(step_name, []):
            shared_memory.add_skill_record(step_name, record)

    def run(self, ctx: TaskContext) -> dict:
        shared_memory = SharedMemory()
        shared_memory.set_task_info("user_id", ctx.user_id)
        shared_memory.set_task_info("query", ctx.query)
        shared_memory.set_task_info("workflow_name", self.name)
        shared_memory.set_task_info("selected_workflow", self.name)
        shared_memory.set_task_info("selected_writing_mode", "introduction_related_work")
        shared_memory.set_task_info("model_provider", ctx.shared_memory.get("model_provider"))
        shared_memory.set_task_info("model_name", ctx.shared_memory.get("model_name"))
        shared_memory.set_task_plan(ctx.shared_memory.get("task_plan", []))
        ctx.shared_memory["workflow_name"] = self.name
        ctx.shared_memory["selected_workflow"] = self.name
        ctx.shared_memory["selected_writing_mode"] = "introduction_related_work"
        ctx.log(f"Workflow started: {self.name}")

        lowered = ctx.query.lower()
        needs_literature = any(term in lowered for term in ("文献", "related work", "introduction", "引言"))

        literature_result = None
        if needs_literature and self.literature_agent is not None:
            ctx.log("Workflow step 1: LiteratureAgent")
            literature_result = self.literature_agent.run(ctx)
            shared_memory.set_result("literature_agent", literature_result)
            shared_memory.set_result("retrieved_papers", ctx.shared_memory.get("retrieved_papers", []))
            ctx.shared_memory["literature_review_notes"] = literature_result
            self._copy_skill_records(ctx, shared_memory, "literature_agent")

        ctx.log("Workflow step 2: WritingAgent" if literature_result else "Workflow step 1: WritingAgent")
        writing_result = self.writing_agent.run(ctx)
        shared_memory.set_result("writing_agent", writing_result)
        ctx.shared_memory["structured_writing_draft"] = writing_result
        self._copy_skill_records(ctx, shared_memory, "writing_agent")

        ctx.log("Workflow step 3: GeneralAgent" if literature_result else "Workflow step 2: GeneralAgent")
        general_result = self.general_agent.run(ctx)
        shared_memory.set_result("general_agent", general_result)

        sections = []
        if literature_result:
            sections.append(f"文献支撑结果：{literature_result}")
        sections.extend(
            [
                f"论文写作结果：{writing_result}",
                f"综合建议：{general_result}",
            ]
        )

        ctx.log("Workflow formatting final result with ResultFormattingSkill")
        final_result_output = self.result_formatter.execute(
            title="这是 paper writing workflow 的最终结果：",
            sections=sections,
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
            title="Paper Writing Artifact",
            sections=[
                ArtifactSection(name="文献支撑结果", content=literature_result or "未单独调用 LiteratureAgent"),
                ArtifactSection(name="论文写作结果", content=writing_result),
                ArtifactSection(name="综合建议", content=general_result),
            ],
            next_actions=[
                "扩写 introduction 的开头背景段。",
                "补充 related work 与研究空白之间的过渡句。",
                "将本文贡献整理成 2-3 条清晰陈述。",
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
