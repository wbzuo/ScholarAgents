from __future__ import annotations

from typing import Any

from scholaragents.mcp.base_client import BaseMCPClient


class ArxivMCPClient(BaseMCPClient):
    """Stub arXiv connector for local development."""

    def search(self, query: str, **kwargs: Any) -> dict:
        top_k = int(kwargs.get("top_k", 5))
        results = [
            {
                "title": f"Mock arXiv paper {index + 1} for {query}",
                "source": "arxiv",
            }
            for index in range(top_k)
        ]
        return {
            "source": "arxiv",
            "query": query,
            "results": results,
        }
