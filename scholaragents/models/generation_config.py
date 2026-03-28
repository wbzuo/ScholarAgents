from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class GenerationConfig:
    provider: str = "mock"
    model_name: str = "gpt-5.4"
    base_url: str | None = None
    temperature: float = 0.2
    max_output_tokens: int = 600
    timeout: float = 30.0
    top_p: float = 1.0
    fallback_to_mock: bool = True
    use_cache: bool = False
