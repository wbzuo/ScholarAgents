from __future__ import annotations

from scholaragents.mcp.base_client import BaseMCPClient
from scholaragents.skills.base_skill import BaseSkill


class PaperSearchSkill(BaseSkill):
    def __init__(self, client: BaseMCPClient) -> None:
        super().__init__("paper_search")
        self.client = client

    def execute(self, query: str, top_k: int = 5) -> dict:
        return self.client.search(query=query, top_k=top_k)
