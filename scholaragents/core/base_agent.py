from __future__ import annotations

from abc import ABC, abstractmethod

from .context import TaskContext


class BaseAgent(ABC):
    """Base class for all agents in the framework."""

    def __init__(self, name: str, description: str = "") -> None:
        self.name = name
        self.description = description

    @abstractmethod
    def can_handle(self, ctx: TaskContext) -> bool:
        """Return True when this agent should handle the task."""

    @abstractmethod
    def run(self, ctx: TaskContext) -> str:
        """Execute the agent's logic for the given task context."""
