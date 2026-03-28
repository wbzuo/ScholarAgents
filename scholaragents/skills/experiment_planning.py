from __future__ import annotations

from collections.abc import Callable

from scholaragents.models.base_model_client import BaseModelClient

from .base_skill import BaseSkill


class ExperimentPlanningSkill(BaseSkill):
    def __init__(self, model_client: BaseModelClient) -> None:
        super().__init__("experiment_planning")
        self.model_client = model_client

    def execute(
        self,
        task_description: str,
        trace: Callable[[str], None] | None = None,
        workflow_name: str | None = None,
        agent_name: str | None = None,
    ) -> dict:
        if trace is not None:
            trace(f"ExperimentPlanningSkill using model provider: {self.model_client.provider}")
            if self.model_client.provider == "openai":
                trace(f"OpenAI model: {self.model_client.model_name}")

        prompt = (
            "You are designing an experiment section for a research project.\n"
            f"Task description: {task_description}\n"
            "Return a concise planning summary for experiments."
        )
        model_text = self.model_client.generate(
            prompt,
            task_description=task_description,
            workflow_name=workflow_name,
            agent_name=agent_name,
            skill_name=self.name,
            mode="experiment_section",
        )

        content = {
            "task_description": task_description,
            "intro": model_text,
            "sections": [
                "任务目标：明确预测对象、数据范围与核心问题。",
                "Baseline：选择强基线、经典方法与可比较方案。",
                "指标：确定主指标、辅助指标与误差分析方式。",
                "消融设计：验证关键模块、输入变量和训练策略的贡献。",
            ],
        }
        return self.build_output(
            content=content,
            task_description=task_description,
            model_provider=self.model_client.provider,
            model_name=self.model_client.model_name,
        )
