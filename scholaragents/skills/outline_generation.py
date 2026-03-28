from __future__ import annotations

from collections.abc import Callable

from scholaragents.models.base_model_client import BaseModelClient

from .base_skill import BaseSkill


class OutlineGenerationSkill(BaseSkill):
    def __init__(self, model_client: BaseModelClient) -> None:
        super().__init__("outline_generation")
        self.model_client = model_client

    def execute(
        self,
        topic: str,
        mode: str = "method_section",
        previous_result: str | None = None,
        trace: Callable[[str], None] | None = None,
        workflow_name: str | None = None,
        agent_name: str | None = None,
    ) -> dict:
        intro_map = {
            "literature_review": "已基于前一步文献整理结果生成综述骨架：",
            "introduction_related_work": "已结合研究背景与相关工作需求生成 introduction/related work 骨架：",
            "experiment_section": "已基于实验设计结果生成 experiments 章节骨架：",
            "method_section": "已根据主题生成 methods 章节骨架：",
        }
        sections_map = {
            "literature_review": [
                "研究主题与问题边界：界定综述范围与关键词体系。",
                "相关研究脉络：按方法类别或应用场景组织代表工作。",
                "优势与局限对比：提炼各类工作的贡献、假设与不足。",
                "研究空白与切入点：指出尚未解决的问题并承接本文定位。",
            ],
            "introduction_related_work": [
                "研究背景：交代问题的重要性、应用价值与现实动机。",
                "核心问题：明确现有工作仍未解决的关键挑战。",
                "相关研究：概述主流方法路线与代表性工作。",
                "研究空白：指出现有研究在数据、方法或泛化上的不足。",
                "本文贡献：总结本文方法、实验和预期贡献点。",
            ],
            "experiment_section": [
                "实验目标：说明实验要验证的假设与核心问题。",
                "Baseline 设置：列出强基线、经典方法与对比方案。",
                "评价指标：明确主指标、辅助指标与统计方式。",
                "实验设置：交代数据集、划分方式、训练配置与实现细节。",
                "消融设计：验证关键模块、输入变量与训练策略贡献。",
                "误差分析：规划案例分析、失败样本与可视化展示。",
            ],
            "method_section": [
                "章节目标：交代本节要解决的问题、输入输出和研究动机。",
                "核心方法：说明模型结构、关键模块和信息流转过程。",
                "实现细节：补充训练设置、参数选择和工程细节。",
                "承接关系：用一句话连接前文背景与后文实验验证。",
            ],
        }

        if trace is not None:
            trace(f"OutlineGenerationSkill using model provider: {self.model_client.provider}")
            if self.model_client.provider == "openai":
                trace(f"OpenAI model: {self.model_client.model_name}")

        prompt = (
            "You are generating an academic writing outline.\n"
            f"Mode: {mode}\n"
            f"Topic: {topic}\n"
            "Return a concise paragraph that captures the writing direction."
        )
        if previous_result:
            prompt += f"\nPrevious result:\n{previous_result}"

        model_text = self.model_client.generate(
            prompt,
            topic=topic,
            workflow_name=workflow_name,
            agent_name=agent_name,
            skill_name=self.name,
            mode=mode,
        )

        intro_prefix = intro_map.get(mode, intro_map["method_section"])
        if previous_result:
            intro = f"{intro_prefix}\n{model_text}\n参考上一步结果：\n{previous_result}"
        else:
            intro = f"{intro_prefix}{model_text}"

        content = {
            "topic": topic,
            "mode": mode,
            "intro": intro,
            "sections": sections_map.get(mode, sections_map["method_section"]),
        }
        return self.build_output(
            content=content,
            topic=topic,
            mode=mode,
            based_on_previous_result=previous_result is not None,
            has_previous_result=previous_result is not None,
            model_provider=self.model_client.provider,
            model_name=self.model_client.model_name,
        )
