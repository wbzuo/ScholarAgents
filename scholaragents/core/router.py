from __future__ import annotations

from .base_agent import BaseAgent
from .context import TaskContext
from .registry import AgentRegistry


class AgentRouter:
    """Selects the first matching agent and falls back to the general agent."""

    def __init__(self, registry: AgentRegistry) -> None:
        self.registry = registry

    def route(self, ctx: TaskContext) -> BaseAgent:
        fallback = None

        for agent in self.registry.get_all():
            if agent.name == "general_agent":
                fallback = agent
                continue

            if agent.can_handle(ctx):
                ctx.log(f"Router selected agent: {agent.name}")
                return agent

        if fallback is not None:
            ctx.log("Router fell back to general_agent")
            return fallback

        raise LookupError("No suitable agent registered and no general agent available.")
