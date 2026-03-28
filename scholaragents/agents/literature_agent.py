from __future__ import annotations

from scholaragents.core.base_agent import BaseAgent
from scholaragents.core.context import TaskContext
from scholaragents.skills.paper_search import PaperSearchSkill
from scholaragents.skills.paper_summary import PaperSummarySkill
from scholaragents.skills.result_formatting import ResultFormattingSkill


class LiteratureAgent(BaseAgent):
    def __init__(
        self,
        paper_search: PaperSearchSkill,
        paper_summary: PaperSummarySkill,
        result_formatter: ResultFormattingSkill,
    ) -> None:
        super().__init__(
            name="literature_agent",
            description="Handles literature review and paper analysis tasks.",
        )
        self.paper_search = paper_search
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
        ctx.log("LiteratureAgent calling PaperSearchSkill")
        search_output = self.paper_search.execute(query=ctx.query, top_k=3, trace=ctx.log)
        self._record_skill_call(ctx, search_output)
        search_content = search_output["content"]
        retrieved_papers = search_content.get("results", [])
        ctx.shared_memory["retrieved_papers"] = retrieved_papers

        paper_lines = []
        for index, paper in enumerate(retrieved_papers, start=1):
            paper_lines.append(
                f"{index}. {paper.get('title')} ({paper.get('year', 'n/a')}) - "
                f"{', '.join(paper.get('authors', []))}"
            )

        ctx.log("LiteratureAgent calling PaperSummarySkill")
        template_output = self.paper_summary.execute(
            topic=ctx.query,
            source_text="\n".join(paper_lines) if paper_lines else None,
            trace=ctx.log,
            workflow_name=ctx.shared_memory.get("workflow_name"),
            agent_name=self.name,
        )
        self._record_skill_call(ctx, template_output)
        template = template_output["content"]
        ctx.log("LiteratureAgent calling ResultFormattingSkill")
        formatted_output = self.result_formatter.execute(
            title="这是一个面向文献调研的初步响应：",
            sections=[
                f"候选论文：{'; '.join(paper_lines)}" if paper_lines else "候选论文：当前未检索到结果。",
                *template["sections"],
            ],
            intro=template.get("intro"),
        )
        self._record_skill_call(ctx, formatted_output)
        return formatted_output["content"]
