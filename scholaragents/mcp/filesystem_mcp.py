from __future__ import annotations

from pathlib import Path
from typing import Any

from scholaragents.mcp.base_client import BaseMCPClient


class FilesystemMCPClient(BaseMCPClient):
    def __init__(self, root: str | Path = ".") -> None:
        self.root = Path(root)

    def search(self, query: str, **kwargs: Any) -> dict:
        matches = [str(path) for path in self.root.rglob("*") if query.lower() in path.name.lower()]
        return {
            "source": "filesystem",
            "query": query,
            "results": matches,
        }
