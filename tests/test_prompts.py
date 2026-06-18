from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT / "src"))

from prompt_loader import load_all_prompts, build_master_prompt


def test_prompt_files_exist_and_load():
    prompts = load_all_prompts()
    assert len(prompts) >= 13
    for content in prompts.values():
        assert len(content) > 700


def test_master_prompt_builds():
    master_prompt = build_master_prompt()
    assert "Ada — Principal Advisor" in master_prompt
    assert len(master_prompt) > 15000


def test_system_prompt_has_core_guardrails():
    prompt = load_all_prompts()["system_prompt"].lower()
    required = [
        "dados sensíveis",
        "canais oficiais",
        "não oficial",
        "não aprova",
        "anti-alucinação",
        "aderência",
    ]
    for term in required:
        assert term in prompt


def test_edge_cases_cover_sensitive_data():
    prompt = load_all_prompts()["edge_cases"].lower()
    for term in ["cpf", "número de cartão", "limite", "aprovação", "senha"]:
        assert term in prompt


def test_recommendation_rules_include_cards():
    prompt = load_all_prompts()["regras_recomendacao"].lower()
    for term in ["visa aeternum", "the platinum card", "bradesco principal", "prime para principal"]:
        assert term in prompt


def test_advanced_prompts_cover_key_topics():
    prompts = load_all_prompts()
    required_files = [
        "guardrails_privacidade_lgpd",
        "guardrails_anti_alucinacao",
        "roteiro_diagnostico_consultivo",
        "nba_playbook",
        "politica_handoff",
        "vendas_consultivas_responsaveis",
        "seguranca_golpes",
        "avaliador_respostas",
        "resumo_cliente_crm",
    ]
    for file_stem in required_files:
        assert file_stem in prompts


def test_forbidden_promises_are_documented_as_prohibited_language():
    combined = build_master_prompt().lower()
    assert "linguagem proibida" in combined or "não pode dizer" in combined
    for phrase in ["você está aprovado", "seu limite será", "garantido"]:
        assert phrase in combined
    assert "não garante aprovação" in combined or "não representa aprovação" in combined


def test_handoff_policy_has_official_channels():
    prompt = load_all_prompts()["politica_handoff"].lower()
    for term in ["app", "internet banking", "gerente", "canais oficiais"]:
        assert term in prompt
