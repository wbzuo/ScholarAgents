from __future__ import annotations

from typing import Any

from scholaragents.mcp.base_client import BaseMCPClient


class GitHubMCPClient(BaseMCPClient):
    def search(self, query: str, **kwargs: Any) -> dict:
        return {
            "source": "github",
            "query": query,
            "results": [],
        }
