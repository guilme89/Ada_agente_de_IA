from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]


def test_readme_exists_and_has_final_sections():
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    required = [
        "Visão Geral",
        "Aviso Importante",
        "Problema",
        "Solução",
        "Arquitetura",
        "Como Rodar",
        "Compatibilidade Multi-LLM",
        "Métricas e Resultados",
        "Diferenciais do Projeto",
        "Pitch",
    ]
    for term in required:
        assert term in readme


def test_pitch_template_is_filled():
    pitch = (ROOT / "docs" / "05-pitch.md").read_text(encoding="utf-8")
    assert "[Sua descrição aqui]" not in pitch
    assert "Problema" in pitch
    assert "Solução" in pitch
    assert "Demonstração" in pitch
    assert "Diferencial" in pitch
    assert "Versão Corrida para Gravação" in pitch


def test_readme_metrics_match_report():
    report = json.loads((ROOT / "reports" / "evaluation_report.json").read_text(encoding="utf-8"))
    summary = report["summary"]
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    assert summary["overall_pass_rate"] == 1.0
    assert summary["nota_media_1_10"] == 10.0
    assert "Nota média 1 a 10 | 10.0" in readme
    assert "Unsafe output rate | 0%" in readme


def test_pitch_mentions_non_official_safety():
    pitch = (ROOT / "docs" / "05-pitch.md").read_text(encoding="utf-8").lower()
    for term in ["educacional", "não oficial", "cpf", "senha", "cvv", "canais oficiais"]:
        assert term in pitch
