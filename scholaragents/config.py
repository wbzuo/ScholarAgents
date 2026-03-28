from __future__ import annotations

import os

from scholaragents.models.generation_config import GenerationConfig


def load_generation_config() -> GenerationConfig:
    provider = os.getenv("MODEL_PROVIDER", "mock").strip().lower() or "mock"
    if provider == "openai":
        model_name = os.getenv("OPENAI_MODEL", "gpt-5.4").strip() or "gpt-5.4"
    else:
        model_name = os.getenv("MOCK_MODEL_NAME", "mock-default").strip() or "mock-default"
    return GenerationConfig(
        provider=provider,
        model_name=model_name,
        temperature=float(os.getenv("MODEL_TEMPERATURE", "0.2")),
        max_output_tokens=int(os.getenv("MODEL_MAX_OUTPUT_TOKENS", "600")),
        timeout=float(os.getenv("MODEL_TIMEOUT", "30")),
        top_p=float(os.getenv("MODEL_TOP_P", "1.0")),
        fallback_to_mock=os.getenv("MODEL_FALLBACK_TO_MOCK", "true").lower() != "false",
        use_cache=os.getenv("MODEL_USE_CACHE", "false").lower() == "true",
    )
