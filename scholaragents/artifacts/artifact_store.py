from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any

from .exporters import export_artifact_to_json, export_artifact_to_markdown


class ArtifactStore:
    """Simple local file store for exported artifacts."""

    def __init__(self, root_dir: str | Path = "outputs") -> None:
        self.root_dir = Path(root_dir)
        self.markdown_dir = self.root_dir / "markdown"
        self.json_dir = self.root_dir / "json"
        self.index_path = self.root_dir / "artifact_index.json"

    def _slugify(self, name: str) -> str:
        cleaned = "".join(char.lower() if char.isalnum() else "_" for char in name)
        compact = "_".join(part for part in cleaned.split("_") if part)
        return compact or "artifact"

    def _build_base_name(self, workflow_name: str | None, case_name: str) -> str:
        workflow_slug = self._slugify(workflow_name or "single_agent")
        case_slug = self._slugify(case_name)
        return f"{workflow_slug}__{case_slug}"

    def _resolve_output_paths(self, workflow_name: str | None, case_name: str) -> tuple[Path, Path]:
        workflow_slug = self._slugify(workflow_name or "single_agent")
        base_name = self._build_base_name(workflow_name, case_name)
        markdown_path = self.markdown_dir / workflow_slug / f"{base_name}.md"
        json_path = self.json_dir / workflow_slug / f"{base_name}.json"
        return markdown_path, json_path

    def _load_index(self) -> list[dict[str, Any]]:
        if not self.index_path.exists():
            return []
        return json.loads(self.index_path.read_text(encoding="utf-8"))

    def _write_index(self, entries: list[dict[str, Any]]) -> None:
        self.index_path.parent.mkdir(parents=True, exist_ok=True)
        self.index_path.write_text(
            json.dumps(entries, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

    def _upsert_index_entry(self, entry: dict[str, Any]) -> None:
        entries = self._load_index()
        key = (entry["workflow_name"], entry["case_name"])
        updated = False

        for index, current in enumerate(entries):
            current_key = (current.get("workflow_name"), current.get("case_name"))
            if current_key == key:
                entries[index] = entry
                updated = True
                break

        if not updated:
            entries.append(entry)

        entries.sort(key=lambda item: (item.get("workflow_name", ""), item.get("case_name", "")))
        self._write_index(entries)

    def save_artifact(
        self,
        artifact: dict[str, Any],
        case_name: str,
        workflow_name: str | None = None,
        query: str | None = None,
        selected_writing_mode: str | None = None,
        task_plan: list[dict[str, Any]] | None = None,
    ) -> dict[str, str]:
        markdown_path, json_path = self._resolve_output_paths(workflow_name, case_name)

        saved_markdown = export_artifact_to_markdown(artifact, markdown_path)
        saved_json = export_artifact_to_json(artifact, json_path)
        exported_at = datetime.now().isoformat(timespec="seconds")

        self._upsert_index_entry(
            {
                "workflow_name": workflow_name or "single_agent",
                "case_name": case_name,
                "query": query,
                "selected_writing_mode": selected_writing_mode,
                "task_plan": task_plan or [],
                "artifact_title": artifact.get("title"),
                "exported_at": exported_at,
                "markdown_path": str(saved_markdown),
                "json_path": str(saved_json),
            }
        )

        return {
            "workflow_name": workflow_name or "single_agent",
            "case_name": case_name,
            "index": str(self.index_path),
            "markdown": str(saved_markdown),
            "json": str(saved_json),
        }
