from __future__ import annotations

import time
from collections.abc import Callable
from typing import TypeVar

from scholaragents.models.exceptions import ModelRequestFailedError

T = TypeVar("T")


class RetryPolicy:
    """Very small retry wrapper for model requests."""

    def __init__(self, max_retries: int = 1, retry_delay: float = 0.5) -> None:
        self.max_retries = max_retries
        self.retry_delay = retry_delay

    def run(self, operation: Callable[[], T]) -> T:
        last_error: Exception | None = None
        for attempt in range(self.max_retries + 1):
            try:
                return operation()
            except Exception as exc:
                last_error = exc
                if attempt >= self.max_retries:
                    break
                time.sleep(self.retry_delay)

        raise ModelRequestFailedError(str(last_error) if last_error else "Unknown model request failure.")
