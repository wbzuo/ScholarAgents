from __future__ import annotations

from scholaragents.models.base_model_client import BaseModelClient


class MockModelClient(BaseModelClient):
    provider = "mock"

    def generate(self, prompt: str, **kwargs: object) -> str:
        topic = str(kwargs.get("topic") or kwargs.get("task_description") or "当前任务")
        mode = str(kwargs.get("mode") or "generic")
        summary = (
            f"[mock:{self.model_name}] 围绕“{topic}”生成了一段可预测的{mode}响应，"
            "用于本地开发、回归测试和无 API key 环境。"
        )
        self._record_usage(
            workflow_name=kwargs.get("workflow_name") if isinstance(kwargs.get("workflow_name"), str) else None,
            agent_name=kwargs.get("agent_name") if isinstance(kwargs.get("agent_name"), str) else None,
            skill_name=kwargs.get("skill_name") if isinstance(kwargs.get("skill_name"), str) else None,
            success=True,
        )
        return self.parser.parse_text(summary)
