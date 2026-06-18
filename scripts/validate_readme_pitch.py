from __future__ import annotations

from pathlib import Path
import ast

ROOT = Path(__file__).resolve().parents[1]

REQUIRED_FILES = [
    "README.md",
    "docs/05-pitch.md",
    "app.py",
    "requirements.txt",
    "src/ada_engine.py",
    "src/evaluator.py",
    "reports/evaluation_report.json",
]

README_REQUIRED_TERMS = [
    "Ada — Principal Advisor",
    "projeto educacional",
    "não oficial",
    "Streamlit",
    "Multi-LLM",
    "OpenAI",
    "Gemini",
    "Claude",
    "Qwen",
    "Guardrails",
    "Métricas",
    "100%",
    "39 passed",
]

PITCH_REQUIRED_TERMS = [
    "O Problema",
    "A Solução",
    "Demonstração",
    "Diferencial e Impacto",
    "Checklist do Pitch",
    "Link do Vídeo",
    "3 minutos",
    "Cliente 360",
    "Next Best Action",
    "Avaliação & Métricas",
]


def validate():
    for rel in REQUIRED_FILES:
        assert (ROOT / rel).exists(), f"Arquivo obrigatório ausente: {rel}"

    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    pitch = (ROOT / "docs" / "05-pitch.md").read_text(encoding="utf-8")

    readme_lower = readme.lower()
    pitch_lower = pitch.lower()

    for term in README_REQUIRED_TERMS:
        assert term.lower() in readme_lower, f"Termo obrigatório ausente no README: {term}"

    for term in PITCH_REQUIRED_TERMS:
        assert term.lower() in pitch_lower, f"Termo obrigatório ausente no pitch: {term}"

    assert len(readme) > 9000, "README muito curto para entrega final."
    assert len(pitch) > 5000, "Pitch muito curto ou incompleto."

    # Basic Python syntax validation of current app/core files.
    for rel in ["app.py", "src/ada_engine.py", "src/evaluator.py"]:
        ast.parse((ROOT / rel).read_text(encoding="utf-8"))

    print("Validação de README e Pitch concluída com sucesso.")


if __name__ == "__main__":
    validate()
