from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT / "src"))

from llm_client import LLMClient, SUPPORTED_PROVIDERS, DEFAULT_MODELS, get_provider_status
from context_builder import build_llm_user_prompt
from response_guardian import output_has_dangerous_claim, enforce_output_guardrails
from ada_engine import generate_response


def test_supported_providers_are_available():
    for provider in ["mock", "openai", "gemini", "claude", "qwen", "openai_compatible"]:
        assert provider in SUPPORTED_PROVIDERS
        assert provider in DEFAULT_MODELS


def test_mock_llm_generates_without_api_key():
    client = LLMClient(provider="mock")
    response = client.generate(system_prompt="Você é Ada.", user_prompt="Olá")
    assert response.ok is True
    assert response.provider == "mock"
    assert "mock" in response.text.lower()


def test_provider_status_contains_env_requirements():
    status = get_provider_status()
    assert status["mock"]["ready"] is True
    assert "OPENAI_API_KEY" in status["openai"]["env"]
    assert "GEMINI_API_KEY" in status["gemini"]["env"]
    assert "ANTHROPIC_API_KEY" in status["claude"]["env"]


def test_context_builder_includes_profile_and_guardrail():
    profile = {
        "persona_id": "PRI-001",
        "segmento_atual": "Principal",
        "cartao_recomendado_ada": "Visa Aeternum",
    }
    prompt = build_llm_user_prompt(
        user_message="Qual cartão combina?",
        deterministic_answer="Com base no perfil informado...",
        profile=profile,
        products=[{"nome": "Visa Aeternum", "guardrail": "Confirmar canais oficiais"}],
        nba_row={"next_best_action_mock": "Apresentar cartão"},
    )
    assert "PRI-001" in prompt
    assert "Visa Aeternum" in prompt
    assert "Não peça dados sensíveis" in prompt


def test_response_guardian_blocks_dangerous_claim():
    bad = "Você está aprovado e seu limite garantido é alto."
    fallback = "Resposta segura."
    assert output_has_dangerous_claim(bad) is True
    assert enforce_output_guardrails(bad, fallback=fallback) == fallback


def test_ada_mock_llm_path_returns_safe_response():
    response = generate_response(
        "Qual cartão combina com quem viaja muito?",
        use_llm=True,
        llm_provider="mock",
        llm_model="local-mock",
        system_prompt="Você é Ada. Não invente informações.",
    )
    assert response["blocked"] is False
    assert response["used_llm"] is True
    assert response["llm_provider"] == "mock"


def test_sensitive_data_blocked_before_llm_call():
    response = generate_response(
        "Meu CPF é 123.456.789-09. Veja meu limite.",
        use_llm=True,
        llm_provider="mock",
    )
    assert response["blocked"] is True
    assert "used_llm" not in response or response.get("used_llm") is None
