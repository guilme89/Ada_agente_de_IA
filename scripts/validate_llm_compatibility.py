from __future__ import annotations

import ast
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

REQUIRED_FILES = [
    "src/llm_client.py",
    "src/context_builder.py",
    "src/response_guardian.py",
    "requirements-llm.txt",
    ".env.example",
    "docs/05-compatibilidade-multi-llm.md",
]

REQUIRED_PROVIDERS = ["mock", "openai", "gemini", "claude", "qwen", "openai_compatible"]

FORBIDDEN_SECRET_PATTERNS = [
    "sk-",
    "AIza",
    "ANTHROPIC_API_KEY=sk-",
    "OPENAI_API_KEY=sk-",
]


def validate_python(path: Path):
    ast.parse(path.read_text(encoding="utf-8"))


def validate():
    for rel in REQUIRED_FILES:
        path = ROOT / rel
        assert path.exists(), f"Arquivo obrigatório ausente: {rel}"

    for rel in ["src/llm_client.py", "src/context_builder.py", "src/response_guardian.py"]:
        validate_python(ROOT / rel)

    llm_content = (ROOT / "src" / "llm_client.py").read_text(encoding="utf-8")
    for provider in REQUIRED_PROVIDERS:
        assert f'"{provider}"' in llm_content, f"Provider ausente em llm_client.py: {provider}"

    env_example = (ROOT / ".env.example").read_text(encoding="utf-8")
    for env in ["OPENAI_API_KEY", "GEMINI_API_KEY", "ANTHROPIC_API_KEY", "QWEN_API_KEY", "DASHSCOPE_API_KEY"]:
        assert env in env_example, f"Variável ausente no .env.example: {env}"

    project_text = ""
    for rel in REQUIRED_FILES:
        project_text += (ROOT / rel).read_text(encoding="utf-8", errors="ignore")

    for forbidden in FORBIDDEN_SECRET_PATTERNS:
        assert forbidden not in project_text, f"Possível segredo/chave real encontrado: {forbidden}"

    print("Validação de compatibilidade Multi-LLM concluída com sucesso.")


if __name__ == "__main__":
    validate()
