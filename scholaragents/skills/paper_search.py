from __future__ import annotations

from collections.abc import Callable

from scholaragents.mcp.base_client import BaseMCPClient
from scholaragents.skills.base_skill import BaseSkill


class PaperSearchSkill(BaseSkill):
    def __init__(self, client: BaseMCPClient) -> None:
        super().__init__("paper_search")
        self.client = client

    def execute(
        self,
        query: str,
        top_k: int = 5,
        trace: Callable[[str], None] | None = None,
    ) -> dict:
        if trace is not None:
            trace(f"PaperSearchSkill using retrieval source: {self.client.__class__.__name__}")

        search_output = self.client.search(query=query, top_k=top_k)
        return self.build_output(
            content=search_output,
            query=query,
            top_k=top_k,
            retrieval_source=search_output.get("source", "unknown"),
            result_count=len(search_output.get("results", [])),
        )
