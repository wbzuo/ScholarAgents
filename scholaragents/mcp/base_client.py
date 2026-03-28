from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class BaseMCPClient(ABC):
    """Abstract connector interface for external tools and data sources."""

    @abstractmethod
    def search(self, query: str, **kwargs: Any) -> dict:
        """Search an external source."""
