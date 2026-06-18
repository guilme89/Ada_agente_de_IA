from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROMPTS = ROOT / "prompts"

MIN_PROMPT_FILES = 12

REQUIRED_FILES = [
    "system_prompt.md",
    "regras_recomendacao.md",
    "exemplos_interacao.md",
    "edge_cases.md",
    "guardrails_privacidade_lgpd.md",
    "guardrails_anti_alucinacao.md",
    "roteiro_diagnostico_consultivo.md",
    "nba_playbook.md",
    "politica_handoff.md",
    "vendas_consultivas_responsaveis.md",
    "seguranca_golpes.md",
    "avaliador_respostas.md",
    "resumo_cliente_crm.md",
]

REQUIRED_CONCEPTS = [
    "Ada — Principal Advisor",
    "dados sensíveis",
    "canais oficiais",
    "não oficial",
    "aderência",
    "aprovação",
    "limite",
    "Next Best Action",
    "Open Finance",
    "LGPD",
    "anti-alucinação",
    "handoff",
    "segurança digital",
    "CRM",
    "mockado",
]

REQUIRED_DENIALS = [
    "não posso solicitar",
    "não garante aprovação",
    "não inventar",
]


def validate():
    files = list(PROMPTS.glob("*.md"))
    assert len(files) >= MIN_PROMPT_FILES, f"Esperado pelo menos {MIN_PROMPT_FILES} prompts, encontrado {len(files)}."

    for filename in REQUIRED_FILES:
        path = PROMPTS / filename
        assert path.exists(), f"Prompt obrigatório ausente: {filename}"
        content = path.read_text(encoding="utf-8")
        assert len(content) > 700, f"Prompt muito curto ou incompleto: {filename}"

    combined = "\n".join(path.read_text(encoding="utf-8") for path in files)
    lower = combined.lower()

    for concept in REQUIRED_CONCEPTS:
        assert concept.lower() in lower, f"Conceito obrigatório ausente: {concept}"

    # O projeto deve conter negações explícitas de promessas indevidas.
    assert "não garante aprovação" in lower or "nao garante aprovacao" in lower or "não representa aprovação" in lower
    assert "não posso solicitar" in lower or "nao posso solicitar" in lower
    assert "não inventar" in lower or "não invente" in lower or "nao inventar" in lower

    # Prohibited phrases may appear only as examples of what Ada must not say.
    assert "linguagem proibida" in lower or "não pode dizer" in lower or "nao pode dizer" in lower

    print("Validação avançada da suíte de prompts concluída com sucesso.")


if __name__ == "__main__":
    validate()
