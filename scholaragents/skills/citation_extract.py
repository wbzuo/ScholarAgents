from __future__ import annotations

from scholaragents.skills.base_skill import BaseSkill


class CitationExtractSkill(BaseSkill):
    def __init__(self) -> None:
        super().__init__("citation_extract")

    def execute(self, document: str) -> dict:
        return {
            "document": document,
            "citations": [],
        }
