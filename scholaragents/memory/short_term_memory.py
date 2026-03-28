from __future__ import annotations


class ShortTermMemory:
    """Simple dict-backed short-term memory."""

    def __init__(self) -> None:
        self._storage: dict[str, object] = {}

    def set(self, key: str, value: object) -> None:
        self._storage[key] = value

    def get(self, key: str, default: object = None) -> object:
        return self._storage.get(key, default)

    def has(self, key: str) -> bool:
        return key in self._storage
