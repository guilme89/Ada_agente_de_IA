from pathlib import Path
import sys
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT / "src"))

from ada_engine import generate_response, summarize_profile
from card_engine import recommend_card_from_inputs
from analytics import calculate_financial_snapshot
from data_loader import load_crm_data


def test_card_engine_recommends_known_card():
    rec = recommend_card_from_inputs(
        viagens_ano=8,
        gasto_mensal=45000,
        interesse_sala_vip="Alta",
        interesse_pontos="Alta",
        prioridade="viagem internacional",
        segmento_atual="Principal",
        patrimonio_investivel=2500000,
    )
    assert rec.card in {"Visa Aeternum", "The Platinum Card®", "Bradesco Principal"}
    assert rec.score > 0
    assert "Não garante" in rec.guardrail or "não garante" in rec.guardrail


def test_ada_blocks_sensitive_data():
    response = generate_response("Meu CPF é 123.456.789-09 e quero limite aprovado")
    assert response["blocked"] is True
    assert response["intent"] == "bloqueio_seguranca"


def test_ada_answers_security_question():
    response = generate_response("Recebi um link suspeito pedindo CVV, o que faço?")
    assert response["blocked"] is False
    assert "Não clique" in response["answer"] or "não clique" in response["answer"]


def test_ada_answers_limit_with_guardrail():
    response = generate_response("Qual limite eu tenho aprovado?")
    assert response["blocked"] is False
    assert "Não tenho acesso" in response["answer"] or "não tenho acesso" in response["answer"]


def test_profile_summary_works_with_crm():
    crm = load_crm_data()
    profile = crm["clientes"][0]
    nba_df = pd.DataFrame(crm["next_best_action"])
    summary = summarize_profile(profile, nba_df.iloc[0].to_dict())
    assert "Resumo consultivo" in summary
    assert "Cartão com maior aderência" in summary


def test_financial_snapshot_has_expected_keys():
    crm = load_crm_data()
    profile = crm["clientes"][0]
    snapshot = calculate_financial_snapshot(profile)
    for key in ["patrimonio_investivel", "share_wallet", "gasto_cartao"]:
        assert key in snapshot
