"""ScholarAgents package."""

from .core.artifact import Artifact, ArtifactSection
from .core.context import Message, TaskContext
from .core.orchestrator import MultiAgentSystem
from .core.registry import AgentRegistry
from .core.router import AgentRouter

__all__ = [
    "AgentRegistry",
    "AgentRouter",
    "Artifact",
    "ArtifactSection",
    "Message",
    "MultiAgentSystem",
    "TaskContext",
]
