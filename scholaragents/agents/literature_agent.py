from __future__ import annotations

from scholaragents.core.base_agent import BaseAgent
from scholaragents.core.context import TaskContext
from scholaragents.skills.paper_summary import PaperSummarySkill
from scholaragents.skills.result_formatting import ResultFormattingSkill


class LiteratureAgent(BaseAgent):
    def __init__(
        self,
        paper_summary: PaperSummarySkill,
        result_formatter: ResultFormattingSkill,
    ) -> None:
        super().__init__(
            name="literature_agent",
            description="Handles literature review and paper analysis tasks.",
        )
        self.paper_summary = paper_summary
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
            "文献",
            "论文",
            "综述",
            "related work",
            "literature",
            "paper",
            "survey",
        )
        query = ctx.query.lower()
        return any(word in query for word in keywords)

    def run(self, ctx: TaskContext) -> str:
        ctx.log("LiteratureAgent generated a literature-review response template")
        ctx.log("LiteratureAgent calling PaperSummarySkill")
        template_output = self.paper_summary.execute(
            topic=ctx.query,
            trace=ctx.log,
            workflow_name=ctx.shared_memory.get("workflow_name"),
            agent_name=self.name,
        )
        self._record_skill_call(ctx, template_output)
        template = template_output["content"]
        ctx.log("LiteratureAgent calling ResultFormattingSkill")
        formatted_output = self.result_formatter.execute(
            title="这是一个面向文献调研的初步响应：",
            sections=template["sections"],
            intro=template.get("intro"),
        )
        self._record_skill_call(ctx, formatted_output)
        return formatted_output["content"]
