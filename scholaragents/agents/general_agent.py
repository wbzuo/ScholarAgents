from __future__ import annotations

from scholaragents.core.base_agent import BaseAgent
from scholaragents.core.context import TaskContext


class GeneralAgent(BaseAgent):
    def __init__(self) -> None:
        super().__init__(
            name="general_agent",
            description="Fallback agent for broad planning and general requests.",
        )

    def can_handle(self, ctx: TaskContext) -> bool:
        return True

    def run(self, ctx: TaskContext) -> str:
        ctx.log("GeneralAgent handled the query as a fallback")
        workflow_name = ctx.shared_memory.get("selected_workflow") or ctx.shared_memory.get("workflow_name")
        if workflow_name:
            ctx.log(f"GeneralAgent running in summary mode for workflow={workflow_name}")
            if workflow_name == "literature_review_workflow":
                return (
                    "建议下一步将上述内容整理为 related work 初稿，"
                    "按研究方向分段写作，并在每段结尾补一句与本文工作的差异。"
                )
            if workflow_name == "paper_writing_workflow":
                return (
                    "建议下一步扩写 introduction：先写问题背景，再接相关研究，"
                    "最后用一段明确研究空白和本文贡献。"
                )
            if workflow_name == "experiment_design_workflow":
                return (
                    "建议下一步按 experiments 章节组织内容：实验目标、baseline、指标、"
                    "实验设置、消融结果与误差分析依次展开。"
                )
        literature_notes = ctx.shared_memory.get("literature_review_notes")
        writing_notes = ctx.shared_memory.get("structured_review_draft")
        if literature_notes and writing_notes:
            return "已完成文献整理与综述结构化写作，可继续扩展为正式 related work 初稿。"

        return (
            "这是一个通用响应：我可以先帮你拆解需求、整理系统模块，"
            "再进一步细化为 agent、workflow 和后续扩展计划。"
        )
