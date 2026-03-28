from __future__ import annotations

from scholaragents.skills.base_skill import BaseSkill


class PDFSummarySkill(BaseSkill):
    def __init__(self) -> None:
        super().__init__("pdf_summary")

    def execute(self, document: str) -> dict:
        return {
            "document": document,
            "summary": f"Placeholder summary for '{document}'.",
        }
