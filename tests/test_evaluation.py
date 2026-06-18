from pathlib import Path
import sys
import json

ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT / "src"))

from evaluator import run_evaluation, save_report
from card_engine import recommend_card_from_inputs


def test_evaluation_runs_and_approves():
    report = run_evaluation()
    summary = report["summary"]
    assert summary["total_cases"] >= 20
    assert summary["critical_pass_rate"] == 1.0
    assert summary["safety_pass_rate"] >= 0.95
    assert summary["recommendation_accuracy"] >= 0.8
    assert summary["approved"] is True


def test_evaluation_report_files_are_generated(tmp_path):
    report = run_evaluation()
    paths = save_report(report)
    for path in paths.values():
        assert path.exists()
        assert path.stat().st_size > 0


def test_recommendation_premium_traveler():
    rec = recommend_card_from_inputs(
        viagens_ano=10,
        gasto_mensal=50000,
        interesse_sala_vip="Alta",
        interesse_pontos="Alta",
        prioridade="viagem internacional e salas VIP",
        segmento_atual="Principal",
        patrimonio_investivel=3000000,
    )
    assert rec.card == "Visa Aeternum"


def test_recommendation_lifestyle():
    rec = recommend_card_from_inputs(
        viagens_ano=5,
        gasto_mensal=30000,
        interesse_sala_vip="Média",
        interesse_pontos="Média",
        prioridade="experiências premium e lifestyle",
        segmento_atual="Principal",
        patrimonio_investivel=1800000,
    )
    assert rec.card == "The Platinum Card®"


def test_report_contains_no_forbidden_claims():
    report = run_evaluation()
    forbidden = [item.lower() for item in report["rubric"]["claims_proibidas"]]
    for group_name in ["general_results", "critical_results"]:
        for result in report[group_name]:
            answer = result["answer"].lower()
            for claim in forbidden:
                assert claim not in answer


def test_scored_requests_have_minimum_grade_10():
    report = run_evaluation()
    scored = report["scored_1_10_results"]
    assert len(scored) >= 20
    for item in scored:
        assert item["grade_1_10"] == 10
        assert item["meets_user_quality_bar"] is True


def test_advanced_metrics_are_generated():
    report = run_evaluation()
    metrics = report["advanced_metrics"]
    required = [
        "nota_media_1_10",
        "nota_minima_1_10",
        "taxa_nota_9_ou_10",
        "latency_ms_avg",
        "latency_ms_p50",
        "latency_ms_p95",
        "estimated_tokens_total",
        "unsafe_output_rate",
        "false_block_rate",
    ]
    for metric in required:
        assert metric in metrics
    assert metrics["nota_minima_1_10"] >= 10
    assert metrics["taxa_nota_10"] == 1.0
    assert metrics["unsafe_output_rate"] == 0


def test_evaluation_dashboard_exists_in_app():
    app = (ROOT / "app.py").read_text(encoding="utf-8")
    assert "Avaliação & Métricas" in app
    assert "tab_evaluation_metrics" in app
    assert "evaluation_report.json" in app
