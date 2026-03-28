from __future__ import annotations


class ModelClientError(RuntimeError):
    """Base error for model client failures."""


class MissingAPIKeyError(ModelClientError):
    """Raised when the selected provider requires an API key."""


class ModelRequestFailedError(ModelClientError):
    """Raised when a model request fails after retries."""


class ModelResponseParseError(ModelClientError):
    """Raised when model output cannot be normalized."""
