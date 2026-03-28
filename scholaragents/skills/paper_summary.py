from __future__ import annotations

from collections.abc import Callable

from scholaragents.models.base_model_client import BaseModelClient

from .base_skill import BaseSkill


class PaperSummarySkill(BaseSkill):
    def __init__(self, model_client: BaseModelClient) -> None:
        super().__init__("paper_summary")
        self.model_client = model_client

    def execute(
        self,
        topic: str,
        source_text: str | None = None,
        trace: Callable[[str], None] | None = None,
        workflow_name: str | None = None,
        agent_name: str | None = None,
    ) -> dict:
        if trace is not None:
            trace(f"PaperSummarySkill using model provider: {self.model_client.provider}")
            if self.model_client.provider == "openai":
                trace(f"OpenAI model: {self.model_client.model_name}")

        prompt = (
            "You are helping with a literature review.\n"
            f"Topic: {topic}\n"
            "Return a concise synthesis that can support a related work section."
        )
        if source_text:
            prompt += f"\nSource text:\n{source_text}"

        model_text = self.model_client.generate(
            prompt,
            topic=topic,
            workflow_name=workflow_name,
            agent_name=agent_name,
            skill_name=self.name,
            mode="literature_review",
        )

        content = {
            "topic": topic,
            "intro": model_text,
            "sections": [
                "明确研究主题与关键词范围。",
                "按研究问题、方法路线和数据来源整理代表性论文。",
                "提炼每篇工作的核心贡献、局限与可借鉴点。",
                "最后输出一版适合写入 related work 的综述框架。",
            ],
        }
        return self.build_output(
            content=content,
            topic=topic,
            has_source_text=source_text is not None,
            model_provider=self.model_client.provider,
            model_name=self.model_client.model_name,
        )
