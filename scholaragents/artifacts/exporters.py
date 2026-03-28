from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def export_artifact_to_markdown(artifact: dict[str, Any], output_path: str | Path) -> Path:
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    lines = [f"# {artifact['title']}", ""]
    for section in artifact.get("sections", []):
        lines.append(f"## {section['name']}")
        lines.append(section["content"])
        lines.append("")

    lines.append("## Next Actions")
    for action in artifact.get("next_actions", []):
        lines.append(f"- {action}")
    lines.append("")

    path.write_text("\n".join(lines), encoding="utf-8")
    return path


def export_artifact_to_json(artifact: dict[str, Any], output_path: str | Path) -> Path:
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(artifact, ensure_ascii=False, indent=2), encoding="utf-8")
    return path
