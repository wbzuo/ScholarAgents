from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass(slots=True)
class ArtifactSection:
    name: str
    content: str


@dataclass(slots=True)
class Artifact:
    title: str
    sections: list[ArtifactSection] = field(default_factory=list)
    next_actions: list[str] = field(default_factory=list)
    raw_text: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "title": self.title,
            "sections": [asdict(section) for section in self.sections],
            "next_actions": self.next_actions,
            "raw_text": self.raw_text,
        }
