from __future__ import annotations

import ast
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

REQUIRED_FILES = [
    "app.py",
    "src/ada_engine.py",
    "src/analytics.py",
    "src/card_engine.py",
    "src/intent_router.py",
    "src/llm_client.py",
    "src/context_builder.py",
    "src/response_guardian.py",
    "src/safety.py",
    "src/data_loader.py",
    "src/prompt_loader.py",
    "data/perfil_investidor.json",
    "data/produtos_financeiros.json",
    "data/transacoes.csv",
    "data/historico_atendimento.csv",
    "data/crm/clientes_atual_v4.csv",
    "data/crm/historico_12m_v4.csv",
    "data/crm/next_best_action_v4.csv",
    "data/crm/base_crm_preditiva_v4.json",
]

REQUIRED_APP_TERMS = [
    "st.tabs",
    "Chat Ada",
    "Cliente 360",
    "Simulador",
    "CRM Dashboard",
    "Next Best Action",
    "Segurança",
    "Prompt Center",
    "Multi-LLM",
    "LLM Provider",
]


def validate_python_syntax(path: Path):
    ast.parse(path.read_text(encoding="utf-8"))


def validate():
    for rel in REQUIRED_FILES:
        path = ROOT / rel
        assert path.exists(), f"Arquivo obrigatório ausente: {rel}"

    for rel in ["app.py", "src/ada_engine.py", "src/analytics.py", "src/card_engine.py", "src/intent_router.py"]:
        validate_python_syntax(ROOT / rel)

    app_content = (ROOT / "app.py").read_text(encoding="utf-8")
    for term in REQUIRED_APP_TERMS:
        assert term in app_content, f"Termo obrigatório ausente no app: {term}"

    print("Validação da aplicação Streamlit concluída com sucesso.")


if __name__ == "__main__":
    validate()
