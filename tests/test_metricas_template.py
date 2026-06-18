from pathlib import Path
import csv
import json

ROOT = Path(__file__).resolve().parents[1]


def test_docs_04_metricas_exists_and_is_complete():
    path = ROOT / "docs" / "04-metricas.md"
    assert path.exists()
    content = path.read_text(encoding="utf-8")
    for term in [
        "Avaliação 1 a 10",
        "Métricas Avançadas",
        "Feedback Humano",
        "Critério Final de Aprovação",
        "latency_ms_p95",
        "estimated_total_tokens",
    ]:
        assert term in content


def test_human_feedback_template_exists():
    path = ROOT / "data" / "evaluation" / "template_feedback_humano_1_10.csv"
    assert path.exists()
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        rows = list(csv.DictReader(f))
    assert rows
    expected_cols = {
        "nota_assertividade_1_10",
        "nota_seguranca_1_10",
        "nota_coerencia_1_10",
        "nota_clareza_1_10",
        "nota_utilidade_1_10",
        "nota_confianca_1_10",
    }
    assert expected_cols.issubset(set(rows[0].keys()))


def test_advanced_metrics_catalog_exists():
    path = ROOT / "data" / "evaluation" / "catalogo_metricas_avancadas.json"
    assert path.exists()
    data = json.loads(path.read_text(encoding="utf-8"))
    assert "categorias" in data
    for category in [
        "qualidade_conversacional",
        "seguranca_e_governanca",
        "anti_alucinacao_grounding",
        "observabilidade_operacional",
        "experiencia_usuario",
    ]:
        assert category in data["categorias"]


def test_simulated_human_feedback_examples_exist():
    path = ROOT / "data" / "evaluation" / "feedback_humano_exemplo_simulado_1_10.csv"
    assert path.exists()
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        rows = list(csv.DictReader(f))
    assert len(rows) >= 5
    assert all("Exemplo simulado" in row["avaliador"] for row in rows)
