from __future__ import annotations

import os
from typing import Any

from scholaragents.models.base_model_client import BaseModelClient
from scholaragents.models.exceptions import MissingAPIKeyError, ModelClientError
from scholaragents.models.retry_policy import RetryPolicy


class OpenAIModelClient(BaseModelClient):
    provider = "openai"

    def __init__(
        self,
        *args: Any,
        retry_policy: RetryPolicy | None = None,
        fallback_client: BaseModelClient | None = None,
        **kwargs: Any,
    ) -> None:
        super().__init__(*args, **kwargs)
        self.retry_policy = retry_policy or RetryPolicy(max_retries=1, retry_delay=0.5)
        self.fallback_client = fallback_client
        self.api_key = os.getenv("OPENAI_API_KEY", "").strip()
        try:
            from openai import OpenAI
        except ImportError as exc:
            self._sdk_error = exc
            self._client = None
        else:
            self._sdk_error = None
            self._client = OpenAI(api_key=self.api_key, timeout=self.config.timeout) if self.api_key else None

    def _generate_once(self, prompt: str) -> str:
        if not self.api_key:
            raise MissingAPIKeyError("OPENAI_API_KEY is not set.")
        if self._client is None:
            if self._sdk_error is not None:
                raise ModelClientError(
                    "The openai package is not installed. Install it to use MODEL_PROVIDER=openai."
                ) from self._sdk_error
            raise ModelClientError("OpenAI client could not be initialized.")

        response = self._client.responses.create(
            model=self.model_name,
            input=prompt,
            temperature=self.config.temperature,
            top_p=self.config.top_p,
            max_output_tokens=self.config.max_output_tokens,
        )
        raw_text = getattr(response, "output_text", None)
        if raw_text:
            return self.parser.parse_text(raw_text)

        output = getattr(response, "output", None)
        if not output:
            raise ModelClientError("OpenAI Responses API returned no text output.")

        parts: list[str] = []
        for item in output:
            content_list = getattr(item, "content", []) or []
            for content_item in content_list:
                text_value = getattr(content_item, "text", None)
                if text_value:
                    parts.append(str(text_value))

        if not parts:
            raise ModelClientError("OpenAI Responses API returned output without text content.")
        return self.parser.parse_text("\n".join(parts))

    def generate(self, prompt: str, **kwargs: object) -> str:
        try:
            result = self.retry_policy.run(lambda: self._generate_once(prompt))
        except Exception as exc:
            self._record_usage(
                workflow_name=kwargs.get("workflow_name") if isinstance(kwargs.get("workflow_name"), str) else None,
                agent_name=kwargs.get("agent_name") if isinstance(kwargs.get("agent_name"), str) else None,
                skill_name=kwargs.get("skill_name") if isinstance(kwargs.get("skill_name"), str) else None,
                success=False,
                error_message=str(exc),
            )
            if self.config.fallback_to_mock and self.fallback_client is not None:
                return self.fallback_client.generate(prompt, **kwargs)
            raise

        self._record_usage(
            workflow_name=kwargs.get("workflow_name") if isinstance(kwargs.get("workflow_name"), str) else None,
            agent_name=kwargs.get("agent_name") if isinstance(kwargs.get("agent_name"), str) else None,
            skill_name=kwargs.get("skill_name") if isinstance(kwargs.get("skill_name"), str) else None,
            success=True,
        )
        return result
