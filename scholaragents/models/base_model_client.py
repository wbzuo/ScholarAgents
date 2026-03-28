from __future__ import annotations

from abc import ABC, abstractmethod

from scholaragents.models.generation_config import GenerationConfig
from scholaragents.models.response_parser import ResponseParser
from scholaragents.models.usage_tracker import UsageTracker


class BaseModelClient(ABC):
    """Provider-agnostic model client interface."""

    provider = "base"

    def __init__(
        self,
        config: GenerationConfig,
        parser: ResponseParser | None = None,
        usage_tracker: UsageTracker | None = None,
    ) -> None:
        self.config = config
        self.parser = parser or ResponseParser()
        self.usage_tracker = usage_tracker

    @property
    def model_name(self) -> str:
        return self.config.model_name

    @abstractmethod
    def generate(self, prompt: str, **kwargs: object) -> str:
        """Generate a text response from a prompt."""

    def chat(self, messages: list[dict[str, str]], **kwargs: object) -> str:
        prompt = "\n".join(f"{item['role']}: {item['content']}" for item in messages)
        return self.generate(prompt, **kwargs)

    def _record_usage(
        self,
        *,
        workflow_name: str | None,
        agent_name: str | None,
        skill_name: str | None,
        success: bool,
        error_message: str | None = None,
    ) -> None:
        if self.usage_tracker is None:
            return
        self.usage_tracker.record(
            provider=self.provider,
            model_name=self.model_name,
            workflow_name=workflow_name,
            agent_name=agent_name,
            skill_name=skill_name,
            success=success,
            error_message=error_message,
        )
