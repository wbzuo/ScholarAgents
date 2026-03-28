from __future__ import annotations

from scholaragents.skills.base_skill import BaseSkill


class ExperimentDesignSkill(BaseSkill):
    def __init__(self) -> None:
        super().__init__("experiment_design")

    def execute(self, goal: str) -> dict:
        return {
            "goal": goal,
            "steps": [
                "Define hypotheses",
                "Select datasets",
                "Choose metrics",
                "Plan ablations",
                "Document expected outcomes",
            ],
        }
