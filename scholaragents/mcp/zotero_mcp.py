from __future__ import annotations

from typing import Any

from scholaragents.mcp.base_client import BaseMCPClient


class ZoteroMCPClient(BaseMCPClient):
    def search(self, query: str, **kwargs: Any) -> dict:
        return {
            "source": "zotero",
            "query": query,
            "results": [],
        }
