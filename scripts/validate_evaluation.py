from __future__ import annotations

import ast
from pathlib import Path
import csv
import json

ROOT = Path(__file__).resolve().parents[1]
EVAL_DIR = ROOT / "data" / "evaluation"

REQUIRED_FILES = [
    "data/evaluation/perguntas_teste.csv",
    "data/evaluation/casos_criticos.csv",
    "data/evaluation/cenarios_recomendacao_cartoes.csv",
    "data/evaluation/rubrica_avaliacao.json",
    "data/evaluation/solicitacoes_nota_1_10.csv",
    "data/evaluation/template_feedback_humano_1_10.csv",
    "data/evaluation/feedback_humano_exemplo_simulado_1_10.csv",
    "data/evaluation/catalogo_metricas_avancadas.json",
    "src/evaluator.py",
    "scripts/run_evaluation.py",
    "docs/06-metricas-avaliacao.md",
]

MIN_GENERAL_CASES = 10
MIN_CRITICAL_CASES = 10
MIN_RECOMMENDATION_SCENARIOS = 5
MIN_SCORED_CASES = 20


def read_csv(path: Path):
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def validate():
    for rel in REQUIRED_FILES:
        assert (ROOT / rel).exists(), f"Arquivo obrigatório ausente: {rel}"

    ast.parse((ROOT / "src" / "evaluator.py").read_text(encoding="utf-8"))
    ast.parse((ROOT / "scripts" / "run_evaluation.py").read_text(encoding="utf-8"))

    perguntas = read_csv(EVAL_DIR / "perguntas_teste.csv")
    criticos = read_csv(EVAL_DIR / "casos_criticos.csv")
    cenarios = read_csv(EVAL_DIR / "cenarios_recomendacao_cartoes.csv")
    scored = read_csv(EVAL_DIR / "solicitacoes_nota_1_10.csv")
    rubrica = json.loads((EVAL_DIR / "rubrica_avaliacao.json").read_text(encoding="utf-8"))
    catalogo = json.loads((EVAL_DIR / "catalogo_metricas_avancadas.json").read_text(encoding="utf-8"))

    assert len(perguntas) >= MIN_GENERAL_CASES
    assert len(criticos) >= MIN_CRITICAL_CASES
    assert len(cenarios) >= MIN_RECOMMENDATION_SCENARIOS
    assert len(scored) >= MIN_SCORED_CASES
    assert "criterios_aprovacao" in rubrica
    assert "claims_proibidas" in rubrica
    assert "categorias" in catalogo
    assert "observabilidade_operacional" in catalogo["categorias"]

    for row in perguntas + criticos + scored:
        assert row.get("case_id")
        assert row.get("pergunta")
        assert row.get("must_contain")
        assert row.get("must_not_contain")

    print("Validação da estrutura de avaliação concluída com sucesso.")


if __name__ == "__main__":
    validate()
