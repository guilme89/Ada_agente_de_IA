from __future__ import annotations

from pathlib import Path
import ast
import json
import re

ROOT = Path(__file__).resolve().parents[1]

REQUIRED_FILES = [
    "README.md",
    "CHECKLIST_ENTREGA.md",
    ".gitignore",
    ".env.example",
    "app.py",
    "requirements.txt",
    "requirements-llm.txt",
    "docs/01-documentacao-agente.md",
    "docs/02-base-conhecimento.md",
    "docs/03-prompts.md",
    "docs/03-prompts-avancados.md",
    "docs/04-metricas.md",
    "docs/04-aplicacao-streamlit.md",
    "docs/05-pitch.md",
    "docs/05-compatibilidade-multi-llm.md",
    "docs/06-metricas-avaliacao.md",
    "docs/07-revisao-final-github.md",
    "src/ada_engine.py",
    "src/card_engine.py",
    "src/llm_client.py",
    "src/evaluator.py",
    "src/safety.py",
    "scripts/run_evaluation.py",
    "scripts/validate_data.py",
    "scripts/validate_prompts.py",
    "scripts/validate_app.py",
    "scripts/validate_llm_compatibility.py",
    "scripts/validate_evaluation.py",
    "scripts/validate_readme_pitch.py",
    "tests/test_app_core.py",
    "tests/test_evaluation.py",
    "reports/evaluation_report.json",
]

REQUIRED_DIRS = [
    "data",
    "data/crm",
    "data/evaluation",
    "docs",
    "prompts",
    "reports",
    "scripts",
    "src",
    "tests",
]

FORBIDDEN_FILE_NAMES = {
    ".env",
    "secrets.toml",
}

SECRET_PATTERNS = [
    r"OPENAI_API_KEY\s*=\s*sk-",
    r"ANTHROPIC_API_KEY\s*=\s*sk-",
    r"GEMINI_API_KEY\s*=\s*AIza",
    r"DASHSCOPE_API_KEY\s*=\s*\w{20,}",
    r"QWEN_API_KEY\s*=\s*\w{20,}",
    r"sk-[A-Za-z0-9]{20,}",
]

SENSITIVE_PATTERNS = [
    r"\b\d{3}\.?\d{3}\.?\d{3}-?\d{2}\b",
    r"\b(?:\d[ -]*?){13,19}\b",
]

ALLOWED_SENSITIVE_EXAMPLE_FILES = {
    "app.py",
    "src/safety.py",
    "tests/test_app_core.py",
    "tests/test_llm_compatibility.py",
    "tests/test_evaluation.py",
    "tests/test_data_integrity.py",
    "data/evaluation/casos_criticos.csv",
    "data/evaluation/perguntas_teste.csv",
    "docs/03-prompts-avancados.md",
    "prompts/edge_cases.md",
    "prompts/exemplos_interacao.md",
    "prompts/guardrails_privacidade_lgpd.md",
    "prompts/seguranca_golpes.md",
    "reports/evaluation_report.json",
    "reports/evaluation_results.csv",
}


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT)).replace("\\", "/")


def validate_required_structure():
    for directory in REQUIRED_DIRS:
        assert (ROOT / directory).is_dir(), f"Pasta obrigatória ausente: {directory}"

    for file in REQUIRED_FILES:
        assert (ROOT / file).is_file(), f"Arquivo obrigatório ausente: {file}"


def validate_python_syntax():
    for path in list((ROOT / "src").glob("*.py")) + list((ROOT / "scripts").glob("*.py")) + list((ROOT / "tests").glob("*.py")):
        ast.parse(path.read_text(encoding="utf-8"))


def validate_no_forbidden_files():
    for path in ROOT.rglob("*"):
        if path.is_file() and path.name in FORBIDDEN_FILE_NAMES:
            raise AssertionError(f"Arquivo proibido encontrado: {rel(path)}")


def validate_no_secrets():
    allowed_literal_examples = {
        "scripts/validate_final_package.py",
        "scripts/validate_llm_compatibility.py",
        "tests/test_final_package.py",
    }

    for path in ROOT.rglob("*"):
        if not path.is_file():
            continue
        if any(part in {".git", ".pytest_cache", "__pycache__"} for part in path.parts):
            continue
        relative = rel(path)
        if relative in allowed_literal_examples:
            continue

        text = path.read_text(encoding="utf-8", errors="ignore")
        for pattern in SECRET_PATTERNS:
            assert not re.search(pattern, text), f"Possível segredo encontrado em {relative}"


def validate_sensitive_examples_only_in_allowed_files():
    offenders = []
    for path in ROOT.rglob("*"):
        if not path.is_file():
            continue
        if path.suffix.lower() not in {".py", ".md", ".csv", ".json", ".txt", ".example"}:
            continue
        relative = rel(path)
        text = path.read_text(encoding="utf-8", errors="ignore")
        if any(re.search(pattern, text) for pattern in SENSITIVE_PATTERNS):
            if relative not in ALLOWED_SENSITIVE_EXAMPLE_FILES:
                offenders.append(relative)
    assert not offenders, f"Possíveis dados sensíveis fora dos exemplos permitidos: {offenders}"


def validate_report_status():
    report = json.loads((ROOT / "reports" / "evaluation_report.json").read_text(encoding="utf-8"))
    summary = report["summary"]
    assert summary["approved"] is True
    assert summary["overall_pass_rate"] == 1.0
    assert summary["critical_pass_rate"] == 1.0
    assert summary["safety_pass_rate"] == 1.0
    assert summary["recommendation_accuracy"] == 1.0
    assert summary["nota_media_1_10"] == 10.0
    assert summary["nota_minima_1_10"] == 10
    assert summary["unsafe_output_rate"] == 0.0


def validate_readme_final_quality():
    readme = (ROOT / "README.md").read_text(encoding="utf-8").lower()
    required_terms = [
        "ada — principal advisor",
        "projeto educacional",
        "não oficial",
        "como rodar",
        "multi-llm",
        "guardrails",
        "métricas",
        "pitch",
        "streamlit",
        "pytest",
    ]
    for term in required_terms:
        assert term in readme, f"README sem termo obrigatório: {term}"


def validate():
    validate_required_structure()
    validate_python_syntax()
    validate_no_forbidden_files()
    validate_no_secrets()
    validate_sensitive_examples_only_in_allowed_files()
    validate_report_status()
    validate_readme_final_quality()
    print("Validação final do pacote concluída com sucesso.")


if __name__ == "__main__":
    validate()
