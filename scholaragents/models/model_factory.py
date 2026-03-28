from __future__ import annotations

from scholaragents.models.base_model_client import BaseModelClient
from scholaragents.models.generation_config import GenerationConfig
from scholaragents.models.mock_client import MockModelClient
from scholaragents.models.openai_client import OpenAIModelClient
from scholaragents.models.response_parser import ResponseParser
from scholaragents.models.retry_policy import RetryPolicy
from scholaragents.models.usage_tracker import UsageTracker


def create_model_client(
    provider: str | None = None,
    config: GenerationConfig | None = None,
    parser: ResponseParser | None = None,
    usage_tracker: UsageTracker | None = None,
    retry_policy: RetryPolicy | None = None,
) -> BaseModelClient:
    effective_config = config or GenerationConfig(provider=provider or "mock")
    resolved_provider = (provider or effective_config.provider or "mock").lower()
    effective_parser = parser or ResponseParser()

    if resolved_provider == "openai":
        fallback_client = None
        if effective_config.fallback_to_mock:
            fallback_client = MockModelClient(
                config=GenerationConfig(
                    provider="mock",
                    model_name="mock-default",
                    temperature=effective_config.temperature,
                    max_output_tokens=effective_config.max_output_tokens,
                    timeout=effective_config.timeout,
                    top_p=effective_config.top_p,
                    fallback_to_mock=False,
                    use_cache=effective_config.use_cache,
                ),
                parser=effective_parser,
                usage_tracker=usage_tracker,
            )
        return OpenAIModelClient(
            config=effective_config,
            parser=effective_parser,
            usage_tracker=usage_tracker,
            retry_policy=retry_policy,
            fallback_client=fallback_client,
        )

    return MockModelClient(
        config=effective_config,
        parser=effective_parser,
        usage_tracker=usage_tracker,
    )
