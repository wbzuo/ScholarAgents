from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class Message:
    role: str
    content: str


@dataclass(slots=True)
class TaskContext:
    user_id: str
    query: str
    history: list[Message] = field(default_factory=list)
    shared_memory: dict[str, Any] = field(default_factory=dict)
    traces: list[str] = field(default_factory=list)

    def add_message(self, role: str, content: str) -> None:
        self.history.append(Message(role=role, content=content))

    def log(self, text: str) -> None:
        self.traces.append(text)
