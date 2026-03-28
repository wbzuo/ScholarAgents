from __future__ import annotations

from .base_agent import BaseAgent


class AgentRegistry:
    """Stores and exposes available agents."""

    def __init__(self) -> None:
        self._agents: dict[str, BaseAgent] = {}

    def register(self, agent: BaseAgent) -> None:
        self._agents[agent.name] = agent

    def get(self, name: str) -> BaseAgent:
        return self._agents[name]

    def get_all(self) -> list[BaseAgent]:
        return list(self._agents.values())
