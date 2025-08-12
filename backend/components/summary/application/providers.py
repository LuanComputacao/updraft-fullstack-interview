import os
import time
from typing import Iterable, Optional

from components.shared.infrastructure.logger import logger
from components.shared.infrastructure.secrets_manager import secrets_manager
from components.shared.infrastructure.errors import NoConfigForTenant
from components.shared.infrastructure.tenant import get_current_tenant
from components.summary.application.prompts import (
    SYSTEM_INSTRUCTION_HTML,
    build_summary_prompt,
)


class SummaryProvider:
    def stream_summary(self, content_html: str, options: dict) -> Iterable[str]:
        raise NotImplementedError


class ProviderStreamError(Exception):
    pass


class MockProvider(SummaryProvider):
    def stream_summary(self, content_html: str, options: dict) -> Iterable[str]:
        # Very naive summary to avoid fixed placeholder text
        text = options.get(
            "mock_text",
            (content_html or "").strip()[:400] or "No content provided to summarize.",
        )
        for i, chunk in enumerate([text[:200], text[200:350], text[350:]]):
            logger.info(f"mock chunk {i}")
            time.sleep(0.15)
            if chunk:
                yield chunk


def _tenant_secret(keys: list[str]) -> Optional[str]:
    try:
        tenant_secrets = secrets_manager.get_tenant_secrets() or {}
    except Exception:
        tenant_secrets = {}
    for k in keys:
        v = tenant_secrets.get(k)
        if v:
            return str(v)
    return None


def _resolve_api_key() -> Optional[str]:
    # Prefer tenant-specific, then shared secret, then environment
    return (
        _tenant_secret(["GEMINI_API_KEY", "LLM_GOOGLE_API_KEY"])
        or secrets_manager.get_shared_secret("LLM_GOOGLE_API_KEY", default=None)
        or os.getenv("GEMINI_API_KEY")
    )


def _resolve_model() -> Optional[str]:
    # Model can come from tenant or env; provider will still apply a default if None
    return _tenant_secret(["LLM_GOOGLE_MODEL", "LLM_MODEL"]) or os.getenv(
        "LLM_GOOGLE_MODEL"
    )


class GeminiProvider(SummaryProvider):
    def __init__(self, api_key: Optional[str] = None, model: Optional[str] = None):
        self._use_new = False
        self._model_name = model or os.getenv("LLM_GOOGLE_MODEL")
        self._attempts = max(1, int(os.getenv("LLM_RETRY_ATTEMPTS", "2")))
        try:
            self._backoff = max(0.0, float(os.getenv("LLM_RETRY_BACKOFF_S", "0.5")))
        except ValueError:
            self._backoff = 0.5

        # Try new google-genai client first
        try:
            from google import genai  # type: ignore
            from google.genai import types  # type: ignore

            self._use_new = True
            self._genai = genai
            self._types = types
            # Prefer explicit key; else client picks GEMINI_API_KEY
            self._client = (
                self._genai.Client(api_key=api_key) if api_key else self._genai.Client()
            )
            if not self._model_name:
                self._model_name = "gemini-2.5-flash"
        except Exception:
            # Fallback to legacy google-generativeai (streaming supported)
            import google.generativeai as genai  # type: ignore

            self._genai = genai
            if api_key:
                self._genai.configure(api_key=api_key)
            else:
                # Also allow GEMINI_API_KEY env to be picked up by the SDK
                self._genai.configure()
            if not self._model_name:
                self._model_name = "gemini-1.5-flash"
            self._model = self._genai.GenerativeModel(
                model_name=self._model_name,
                generation_config={
                    "temperature": float(os.getenv("LLM_TEMPERATURE", "0.3")),
                    "max_output_tokens": int(
                        os.getenv("LLM_MAX_OUTPUT_TOKENS", "2048")
                    ),
                },
                system_instruction=SYSTEM_INSTRUCTION_HTML,
            )

    @staticmethod
    def _strip_code_fences(text: str, first_chunk: bool) -> tuple[str, bool]:
        if first_chunk:
            t = text.lstrip()
            if t.startswith("```"):
                t = t[3:]
                if t.startswith("html"):
                    t = t[4:]
                    if t.startswith("\n"):
                        t = t[1:]
            text = t
            first_chunk = False
        if "```" in text:
            text = text.replace("```", "")
        return text, first_chunk

    def _yield_in_chunks(self, text: str, size: int = 512) -> Iterable[str]:
        for i in range(0, len(text), size):
            chunk = text[i : i + size]
            if chunk:
                yield chunk

    def _build_new_config(self):
        try:
            thinking_budget = int(os.getenv("LLM_THINKING_BUDGET", "0"))
        except ValueError:
            thinking_budget = 0
        try:
            return self._types.GenerateContentConfig(
                temperature=float(os.getenv("LLM_TEMPERATURE", "0.3")),
                max_output_tokens=int(os.getenv("LLM_MAX_OUTPUT_TOKENS", "2048")),
                thinking_config=self._types.ThinkingConfig(
                    thinking_budget=thinking_budget
                ),
            )
        except Exception:
            return None

    def _request_new_client(self, prompt: str):
        config = self._build_new_config()
        if config is not None:
            return self._client.models.generate_content(
                model=self._model_name, contents=prompt, config=config
            )
        return self._client.models.generate_content(
            model=self._model_name, contents=prompt
        )

    def _stream_with_new_client(self, prompt: str) -> Iterable[str]:
        last_err: Optional[Exception] = None
        for attempt in range(self._attempts):
            try:
                resp = self._request_new_client(prompt)
                text = getattr(resp, "text", None) or ""
                first_chunk = True
                for part in self._yield_in_chunks(text, size=600):
                    part, first_chunk = self._strip_code_fences(part, first_chunk)
                    if part:
                        yield part
                return
            except Exception as e:
                last_err = e
                logger.warning("genai_client_retry", extra={"attempt": attempt + 1})
                if attempt < self._attempts - 1:
                    time.sleep(self._backoff * (2**attempt))
        logger.exception("genai_client_error", exc_info=True)
        raise ProviderStreamError(str(last_err) if last_err else "LLM request failed")

    def _stream_with_legacy(self, prompt: str) -> Iterable[str]:
        last_err: Optional[Exception] = None
        for attempt in range(self._attempts):
            try:
                stream = self._model.generate_content(prompt, stream=True)
                first_chunk = True
                for chunk in stream:
                    text = getattr(chunk, "text", None)
                    if not text:
                        continue
                    text, first_chunk = self._strip_code_fences(text, first_chunk)
                    if text:
                        yield text
                return
            except Exception as e:
                last_err = e
                logger.warning("gemini_stream_retry", extra={"attempt": attempt + 1})
                if attempt < self._attempts - 1:
                    time.sleep(self._backoff * (2**attempt))
        logger.exception("gemini_stream_error", exc_info=True)
        raise ProviderStreamError(str(last_err) if last_err else "LLM stream failed")

    def stream_summary(self, content_html: str, options: dict) -> Iterable[str]:
        instruction = options.get("instruction")
        prompt = build_summary_prompt(content_html, instruction)
        if self._use_new:
            yield from self._stream_with_new_client(prompt)
        else:
            yield from self._stream_with_legacy(prompt)


def get_provider() -> SummaryProvider:
    # Tenant-aware resolution with safe fallbacks, but require an API key
    api_key = _resolve_api_key()
    model = _resolve_model()
    if not api_key:
        tenant = get_current_tenant() or "unknown"
        raise NoConfigForTenant(tenant)
    return GeminiProvider(api_key=api_key, model=model)
