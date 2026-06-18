from __future__ import annotations

from dataclasses import dataclass
from typing import Any
import os


SUPPORTED_PROVIDERS = {
    "mock": "Modo local determinístico, sem API externa.",
    "openai": "OpenAI / ChatGPT via OpenAI API.",
    "gemini": "Google Gemini via Google GenAI SDK.",
    "claude": "Anthropic Claude via Anthropic Messages API.",
    "qwen": "Qwen via API OpenAI-compatible da Alibaba Cloud/DashScope.",
    "openai_compatible": "Qualquer endpoint compatível com Chat Completions da OpenAI.",
}


DEFAULT_MODELS = {
    "mock": "local-mock",
    "openai": "gpt-5.5",
    "gemini": "gemini-3.5-flash",
    "claude": "claude-sonnet-4-6",
    "qwen": "qwen-plus",
    "openai_compatible": "model-name",
}


@dataclass
class LLMRequest:
    provider: str
    model: str
    system_prompt: str
    user_prompt: str
    temperature: float = 0.2
    max_tokens: int = 900


@dataclass
class LLMResponse:
    provider: str
    model: str
    text: str
    ok: bool
    error: str | None = None
    used_fallback: bool = False


class LLMConfigurationError(RuntimeError):
    pass


class LLMClient:
    """Provider-agnostic LLM client.

    The imports for each provider are intentionally lazy. This keeps the core
    Streamlit app working without installing every vendor SDK.
    """

    def __init__(self, provider: str = "mock", model: str | None = None):
        provider = (provider or "mock").lower().strip()
        if provider not in SUPPORTED_PROVIDERS:
            raise ValueError(f"Provider não suportado: {provider}")
        self.provider = provider
        self.model = model or DEFAULT_MODELS[provider]

    def generate(self, system_prompt: str, user_prompt: str, temperature: float = 0.2, max_tokens: int = 900) -> LLMResponse:
        request = LLMRequest(
            provider=self.provider,
            model=self.model,
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            temperature=temperature,
            max_tokens=max_tokens,
        )

        if self.provider == "mock":
            return self._mock_generate(request)

        try:
            if self.provider == "openai":
                return self._openai_generate(request)
            if self.provider == "gemini":
                return self._gemini_generate(request)
            if self.provider == "claude":
                return self._claude_generate(request)
            if self.provider == "qwen":
                return self._qwen_generate(request)
            if self.provider == "openai_compatible":
                return self._openai_compatible_generate(request)
        except Exception as exc:  # pragma: no cover - exercised only with real APIs
            return LLMResponse(
                provider=request.provider,
                model=request.model,
                text="",
                ok=False,
                error=f"{type(exc).__name__}: {exc}",
                used_fallback=True,
            )

        return LLMResponse(provider=request.provider, model=request.model, text="", ok=False, error="Provider não implementado.")

    def _mock_generate(self, request: LLMRequest) -> LLMResponse:
        text = (
            "Resposta mockada da camada LLM: a Ada usaria o provedor selecionado para reescrever a resposta "
            "com tom consultivo, premium e seguro. Como o modo mock está ativo, nenhum dado saiu do ambiente local."
        )
        return LLMResponse(provider=request.provider, model=request.model, text=text, ok=True)

    def _openai_generate(self, request: LLMRequest) -> LLMResponse:  # pragma: no cover
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise LLMConfigurationError("OPENAI_API_KEY não configurada.")

        from openai import OpenAI

        client = OpenAI(api_key=api_key)

        # Responses API keeps the implementation aligned with current OpenAI agentic patterns.
        response = client.responses.create(
            model=request.model,
            input=[
                {"role": "system", "content": request.system_prompt},
                {"role": "user", "content": request.user_prompt},
            ],
            temperature=request.temperature,
            max_output_tokens=request.max_tokens,
        )

        text = getattr(response, "output_text", None)
        if not text:
            text = str(response)
        return LLMResponse(provider=request.provider, model=request.model, text=text, ok=True)

    def _gemini_generate(self, request: LLMRequest) -> LLMResponse:  # pragma: no cover
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise LLMConfigurationError("GEMINI_API_KEY não configurada.")

        from google import genai

        client = genai.Client(api_key=api_key)
        prompt = (
            f"{request.system_prompt}\n\n"
            "Instrução: responda em português do Brasil, mantendo os guardrails do sistema.\n\n"
            f"Usuário:\n{request.user_prompt}"
        )
        response = client.models.generate_content(
            model=request.model,
            contents=prompt,
        )
        return LLMResponse(provider=request.provider, model=request.model, text=response.text or "", ok=True)

    def _claude_generate(self, request: LLMRequest) -> LLMResponse:  # pragma: no cover
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            raise LLMConfigurationError("ANTHROPIC_API_KEY não configurada.")

        from anthropic import Anthropic

        client = Anthropic(api_key=api_key)
        response = client.messages.create(
            model=request.model,
            max_tokens=request.max_tokens,
            temperature=request.temperature,
            system=request.system_prompt,
            messages=[{"role": "user", "content": request.user_prompt}],
        )
        parts = []
        for block in response.content:
            if getattr(block, "type", None) == "text":
                parts.append(block.text)
        return LLMResponse(provider=request.provider, model=request.model, text="\n".join(parts), ok=True)

    def _qwen_generate(self, request: LLMRequest) -> LLMResponse:  # pragma: no cover
        api_key = os.getenv("QWEN_API_KEY") or os.getenv("DASHSCOPE_API_KEY")
        if not api_key:
            raise LLMConfigurationError("QWEN_API_KEY ou DASHSCOPE_API_KEY não configurada.")

        base_url = os.getenv("QWEN_BASE_URL", "https://dashscope.aliyuncs.com/compatible-mode/v1")
        return self._chat_completions_openai_sdk(request, api_key=api_key, base_url=base_url)

    def _openai_compatible_generate(self, request: LLMRequest) -> LLMResponse:  # pragma: no cover
        api_key = os.getenv("OPENAI_COMPATIBLE_API_KEY")
        base_url = os.getenv("OPENAI_COMPATIBLE_BASE_URL")
        if not api_key or not base_url:
            raise LLMConfigurationError("OPENAI_COMPATIBLE_API_KEY e OPENAI_COMPATIBLE_BASE_URL devem estar configuradas.")

        return self._chat_completions_openai_sdk(request, api_key=api_key, base_url=base_url)

    def _chat_completions_openai_sdk(self, request: LLMRequest, api_key: str, base_url: str) -> LLMResponse:  # pragma: no cover
        from openai import OpenAI

        client = OpenAI(api_key=api_key, base_url=base_url)
        response = client.chat.completions.create(
            model=request.model,
            messages=[
                {"role": "system", "content": request.system_prompt},
                {"role": "user", "content": request.user_prompt},
            ],
            temperature=request.temperature,
            max_tokens=request.max_tokens,
        )
        text = response.choices[0].message.content or ""
        return LLMResponse(provider=request.provider, model=request.model, text=text, ok=True)


def get_provider_status() -> dict[str, dict[str, Any]]:
    return {
        "mock": {"ready": True, "env": [], "description": SUPPORTED_PROVIDERS["mock"]},
        "openai": {"ready": bool(os.getenv("OPENAI_API_KEY")), "env": ["OPENAI_API_KEY"], "description": SUPPORTED_PROVIDERS["openai"]},
        "gemini": {"ready": bool(os.getenv("GEMINI_API_KEY")), "env": ["GEMINI_API_KEY"], "description": SUPPORTED_PROVIDERS["gemini"]},
        "claude": {"ready": bool(os.getenv("ANTHROPIC_API_KEY")), "env": ["ANTHROPIC_API_KEY"], "description": SUPPORTED_PROVIDERS["claude"]},
        "qwen": {"ready": bool(os.getenv("QWEN_API_KEY") or os.getenv("DASHSCOPE_API_KEY")), "env": ["QWEN_API_KEY", "DASHSCOPE_API_KEY", "QWEN_BASE_URL"], "description": SUPPORTED_PROVIDERS["qwen"]},
        "openai_compatible": {"ready": bool(os.getenv("OPENAI_COMPATIBLE_API_KEY") and os.getenv("OPENAI_COMPATIBLE_BASE_URL")), "env": ["OPENAI_COMPATIBLE_API_KEY", "OPENAI_COMPATIBLE_BASE_URL"], "description": SUPPORTED_PROVIDERS["openai_compatible"]},
    }
