from __future__ import annotations

from scholaragents.core.base_agent import BaseAgent
from scholaragents.core.context import TaskContext
from scholaragents.skills.outline_generation import OutlineGenerationSkill
from scholaragents.skills.result_formatting import ResultFormattingSkill


class WritingAgent(BaseAgent):
    def __init__(
        self,
        outline_generation: OutlineGenerationSkill,
        result_formatter: ResultFormattingSkill,
    ) -> None:
        super().__init__(
            name="writing_agent",
            description="Handles academic writing and polishing tasks.",
        )
        self.outline_generation = outline_generation
        self.result_formatter = result_formatter

    def _record_skill_call(self, ctx: TaskContext, skill_output: dict) -> None:
        ctx.shared_memory.setdefault("skill_records", {}).setdefault(self.name, []).append(
            {
                "skill_name": skill_output["name"],
                "metadata": skill_output["metadata"],
            }
        )

    def _select_mode(self, ctx: TaskContext) -> str:
        selected_mode = ctx.shared_memory.get("selected_writing_mode")
        if selected_mode:
            return selected_mode

        query = ctx.query.lower()
        if ctx.shared_memory.get("experiment_design_notes"):
            return "experiment_section"
        if ctx.shared_memory.get("literature_review_notes"):
            return "literature_review"
        if any(word in query for word in ("introduction", "related work", "引言", "背景")):
            return "introduction_related_work"
        if any(word in query for word in ("method", "methods", "方法")):
            return "method_section"
        return "method_section"

    def can_handle(self, ctx: TaskContext) -> bool:
        keywords = (
            "写",
            "润色",
            "methods",
            "introduction",
            "related work",
            "method",
            "draft",
            "outline",
        )
        query = ctx.query.lower()
        return any(word in query for word in keywords)

    def run(self, ctx: TaskContext) -> str:
        ctx.log("WritingAgent generated a writing-assistance response template")
        mode = self._select_mode(ctx)
        ctx.shared_memory["selected_writing_mode"] = mode
        ctx.log(f"WritingAgent selected mode={mode}")
        experiment_notes = ctx.shared_memory.get("experiment_design_notes")
        if experiment_notes:
            ctx.log(f"WritingAgent calling OutlineGenerationSkill with mode={mode}")
            outline_output = self.outline_generation.execute(
                topic=f"{ctx.query} | experiments and methods framing",
                mode=mode,
                previous_result=experiment_notes,
                trace=ctx.log,
                workflow_name=ctx.shared_memory.get("workflow_name"),
                agent_name=self.name,
            )
            self._record_skill_call(ctx, outline_output)
            outline = outline_output["content"]
            ctx.log("WritingAgent calling ResultFormattingSkill")
            formatted_output = self.result_formatter.execute(
                title="这是一个面向实验与写作衔接的结构化结果：",
                sections=outline["sections"],
                intro=outline.get("intro"),
            )
            self._record_skill_call(ctx, formatted_output)
            return formatted_output["content"]

        literature_notes = ctx.shared_memory.get("literature_review_notes")
        if literature_notes:
            ctx.log(f"WritingAgent calling OutlineGenerationSkill with mode={mode}")
            outline_output = self.outline_generation.execute(
                topic=ctx.query,
                mode=mode,
                previous_result=literature_notes,
                trace=ctx.log,
                workflow_name=ctx.shared_memory.get("workflow_name"),
                agent_name=self.name,
            )
            self._record_skill_call(ctx, outline_output)
            outline = outline_output["content"]
            ctx.log("WritingAgent calling ResultFormattingSkill")
            formatted_output = self.result_formatter.execute(
                title="这是一个面向综述写作的结构化结果：",
                sections=outline["sections"],
                intro=outline.get("intro"),
            )
            self._record_skill_call(ctx, formatted_output)
            return formatted_output["content"]

        ctx.log(f"WritingAgent calling OutlineGenerationSkill with mode={mode}")
        outline_output = self.outline_generation.execute(
            topic=ctx.query,
            mode=mode,
            trace=ctx.log,
            workflow_name=ctx.shared_memory.get("workflow_name"),
            agent_name=self.name,
        )
        self._record_skill_call(ctx, outline_output)
        outline = outline_output["content"]
        ctx.log("WritingAgent calling ResultFormattingSkill")
        formatted_output = self.result_formatter.execute(
            title="这是一个由写作 skill 生成的结构化写作结果：",
            sections=outline["sections"],
            intro=outline.get("intro"),
        )
        self._record_skill_call(ctx, formatted_output)
        return formatted_output["content"]
