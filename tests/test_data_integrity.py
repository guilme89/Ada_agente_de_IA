from pathlib import Path
import csv
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT / "src"))

from safety import validate_user_message
from recommender import recommend_card


DATA = ROOT / "data"


def read_csv(path: Path):
    with path.open("r", encoding="utf-8-sig", newline="") as file:
        return list(csv.DictReader(file))


def test_required_files_exist():
    required = [
        "perfil_investidor.json",
        "produtos_financeiros.json",
        "transacoes.csv",
        "historico_atendimento.csv",
        "crm/clientes_atual_v4.csv",
        "crm/historico_12m_v4.csv",
        "crm/next_best_action_v4.csv",
        "crm/base_crm_preditiva_v4.json",
    ]
    for item in required:
        assert (DATA / item).exists()


def test_core_json_loads():
    perfil = json.loads((DATA / "perfil_investidor.json").read_text(encoding="utf-8"))
    produtos = json.loads((DATA / "produtos_financeiros.json").read_text(encoding="utf-8"))
    assert perfil["segmento_atual"] in {"Principal", "Prime"}
    assert len(produtos) >= 6


def test_crm_sizes():
    clientes = read_csv(DATA / "crm/clientes_atual_v4.csv")
    historico = read_csv(DATA / "crm/historico_12m_v4.csv")
    nba = read_csv(DATA / "crm/next_best_action_v4.csv")
    assert len(clientes) == 100
    assert len(historico) == 1200
    assert len(nba) == 100


def test_safety_blocks_sensitive_content():
    ok, refusal = validate_user_message("Meu CPF é 123.456.789-09")
    assert ok is False
    assert refusal is not None


def test_safety_allows_normal_question():
    ok, refusal = validate_user_message("Qual cartão tem mais aderência para quem viaja muito?")
    assert ok is True
    assert refusal is None


def test_recommender_returns_card():
    perfil = json.loads((DATA / "perfil_investidor.json").read_text(encoding="utf-8"))
    produtos = json.loads((DATA / "produtos_financeiros.json").read_text(encoding="utf-8"))
    result = recommend_card(perfil, produtos)
    assert result["cartao"] in {"Bradesco Principal", "Visa Aeternum", "The Platinum Card®"}
    assert "guardrail" in result
