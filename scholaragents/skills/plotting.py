from __future__ import annotations

from scholaragents.skills.base_skill import BaseSkill


class PlottingSkill(BaseSkill):
    def __init__(self) -> None:
        super().__init__("plotting")

    def execute(self, series_name: str) -> dict:
        return {
            "series_name": series_name,
            "status": "plot placeholder generated",
        }
