from __future__ import annotations

from scholaragents.models.exceptions import ModelResponseParseError


class ResponseParser:
    """Small post-processor that keeps model output stable for skills."""

    NOISE_PREFIXES = (
        "here is",
        "here's",
        "sure,",
        "certainly,",
    )

    def parse_text(self, raw_text: object) -> str:
        if raw_text is None:
            raise ModelResponseParseError("Model returned empty output.")

        text = str(raw_text).strip()
        if not text:
            raise ModelResponseParseError("Model returned blank output.")

        normalized_lines = [line.strip() for line in text.splitlines() if line.strip()]
        normalized = "\n".join(normalized_lines)
        lowered = normalized.lower()
        for prefix in self.NOISE_PREFIXES:
            if lowered.startswith(prefix):
                parts = normalized.split(":", maxsplit=1)
                if len(parts) == 2 and parts[1].strip():
                    normalized = parts[1].strip()
                break

        return normalized or text
