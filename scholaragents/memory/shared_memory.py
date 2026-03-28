from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class SharedMemory:
    task_info: dict[str, Any] = field(default_factory=dict)
    task_plan: list[dict[str, Any]] = field(default_factory=list)
    intermediate_results: dict[str, Any] = field(default_factory=dict)
    skill_records: dict[str, Any] = field(default_factory=dict)
    final_result: Any = None

    def set_task_info(self, key: str, value: Any) -> None:
        self.task_info[key] = value

    def get_task_info(self, key: str, default: Any = None) -> Any:
        return self.task_info.get(key, default)

    def set_task_plan(self, plan: list[dict[str, Any]]) -> None:
        self.task_plan = plan

    def get_task_plan(self) -> list[dict[str, Any]]:
        return self.task_plan

    def set_result(self, step_name: str, value: Any) -> None:
        self.intermediate_results[step_name] = value

    def get_result(self, step_name: str, default: Any = None) -> Any:
        return self.intermediate_results.get(step_name, default)

    def add_skill_record(self, step_name: str, record: dict[str, Any]) -> None:
        self.skill_records.setdefault(step_name, []).append(record)

    def get_skill_records(self, step_name: str, default: Any = None) -> Any:
        return self.skill_records.get(step_name, default)

    def set_final_result(self, value: Any) -> None:
        self.final_result = value

    def to_dict(self) -> dict[str, Any]:
        return {
            "task_info": self.task_info,
            "task_plan": self.task_plan,
            "intermediate_results": self.intermediate_results,
            "skill_records": self.skill_records,
            "final_result": self.final_result,
        }
