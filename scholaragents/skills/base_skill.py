from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class BaseSkill(ABC):
    """Base interface for reusable agent skills."""

    def __init__(self, name: str) -> None:
        self.name = name

    @abstractmethod
    def execute(self, **kwargs: Any) -> Any:
        """Execute the skill with arbitrary named inputs."""

    def build_output(self, content: Any, **metadata: Any) -> dict[str, Any]:
        return {
            "name": self.name,
            "metadata": metadata,
            "content": content,
        }
