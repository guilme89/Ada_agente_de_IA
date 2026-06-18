from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROMPTS = ROOT / "prompts"

REQUIRED_FILES = [
    "system_prompt.md",
    "regras_recomendacao.md",
    "exemplos_interacao.md",
    "edge_cases.md",
]

REQUIRED_TERMS = [
    "Ada — Principal Advisor",
    "dados sensíveis",
    "canais oficiais",
    "aprovação",
    "aderência",
    "não oficial",
]


def validate():
    for filename in REQUIRED_FILES:
        path = PROMPTS / filename
        assert path.exists(), f"Prompt ausente: {filename}"
        content = path.read_text(encoding="utf-8")
        assert len(content) > 1000, f"Prompt muito curto: {filename}"

    combined = "\n".join((PROMPTS / f).read_text(encoding="utf-8") for f in REQUIRED_FILES)
    lower = combined.lower()

    for term in REQUIRED_TERMS:
        assert term.lower() in lower, f"Termo obrigatório ausente nos prompts: {term}"

    assert "não posso solicitar" in lower or "nao posso solicitar" in lower
    assert "não garante aprovação" in lower or "nao garante aprovacao" in lower or "não representa aprovação" in lower or "nunca representa aprovação" in lower

    print("Validação de prompts concluída com sucesso.")


if __name__ == "__main__":
    validate()
