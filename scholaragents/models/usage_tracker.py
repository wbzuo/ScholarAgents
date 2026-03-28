from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime


@dataclass
class UsageRecord:
    provider: str
    model_name: str
    workflow_name: str | None
    agent_name: str | None
    skill_name: str | None
    success: bool
    error_message: str | None
    timestamp: str


class UsageTracker:
    """In-memory tracker for model requests."""

    def __init__(self) -> None:
        self.records: list[UsageRecord] = []

    def record(
        self,
        *,
        provider: str,
        model_name: str,
        workflow_name: str | None,
        agent_name: str | None,
        skill_name: str | None,
        success: bool,
        error_message: str | None = None,
    ) -> None:
        self.records.append(
            UsageRecord(
                provider=provider,
                model_name=model_name,
                workflow_name=workflow_name,
                agent_name=agent_name,
                skill_name=skill_name,
                success=success,
                error_message=error_message,
                timestamp=datetime.now().isoformat(timespec="seconds"),
            )
        )

    def to_list(self) -> list[dict[str, object]]:
        return [asdict(record) for record in self.records]
