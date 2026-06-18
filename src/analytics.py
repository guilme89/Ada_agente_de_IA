from __future__ import annotations

import pandas as pd
from typing import Any


def to_number(value: Any, default: float = 0.0) -> float:
    try:
        if value is None or value == "":
            return default
        return float(value)
    except (TypeError, ValueError):
        return default


def classify_temperature(score: float) -> str:
    if score >= 82:
        return "Quente"
    if score >= 68:
        return "Morno"
    return "Nutrição"


def calculate_financial_snapshot(profile: dict[str, Any]) -> dict[str, float]:
    renda = to_number(profile.get("renda_mensal_estimada_mock"))
    renda_familiar = to_number(profile.get("renda_familiar_mensal_mock"), renda)
    despesas = to_number(profile.get("despesas_mensais_estimadas_mock"))
    patrimonio = to_number(profile.get("patrimonio_investivel_estimado_mock"))
    investimentos = to_number(profile.get("investimentos_bradesco_estimado_mock"))
    gasto_cartao = to_number(profile.get("gasto_mensal_cartao_estimado_mock"))
    reserva = to_number(profile.get("reserva_emergencia_mock"))

    capacidade = renda_familiar - despesas
    taxa_poupanca = capacidade / renda_familiar if renda_familiar else 0
    share_wallet = investimentos / patrimonio if patrimonio else 0
    meses_reserva = reserva / despesas if despesas else 0
    gap = max(patrimonio - investimentos, 0)

    return {
        "renda_mensal": renda,
        "renda_familiar": renda_familiar,
        "despesas": despesas,
        "capacidade_poupanca": capacidade,
        "taxa_poupanca": taxa_poupanca,
        "patrimonio_investivel": patrimonio,
        "investimentos_bradesco": investimentos,
        "share_wallet": share_wallet,
        "gap_relacionamento": gap,
        "gasto_cartao": gasto_cartao,
        "reserva_emergencia": reserva,
        "meses_reserva": meses_reserva,
    }


def summarize_dataset(clientes: pd.DataFrame, historico: pd.DataFrame, nba: pd.DataFrame) -> dict[str, Any]:
    resumo = {
        "total_clientes": int(len(clientes)),
        "principal": int((clientes["segmento_atual"] == "Principal").sum()) if "segmento_atual" in clientes else 0,
        "prime": int((clientes["segmento_atual"] == "Prime").sum()) if "segmento_atual" in clientes else 0,
        "historico_registros": int(len(historico)),
        "nba_registros": int(len(nba)),
    }

    if "temperatura_lead" in clientes:
        resumo["temperatura"] = clientes["temperatura_lead"].value_counts().to_dict()
    else:
        resumo["temperatura"] = {}

    if "patrimonio_investivel_estimado_mock" in clientes:
        resumo["patrimonio_total_mock"] = float(pd.to_numeric(clientes["patrimonio_investivel_estimado_mock"], errors="coerce").fillna(0).sum())

    if "aporte_previsto_12m_mock" in clientes:
        resumo["aporte_previsto_mock"] = float(pd.to_numeric(clientes["aporte_previsto_12m_mock"], errors="coerce").fillna(0).sum())

    return resumo


def get_client_history(historico: pd.DataFrame, persona_id: str) -> pd.DataFrame:
    if historico.empty or "persona_id" not in historico.columns:
        return pd.DataFrame()
    data = historico[historico["persona_id"] == persona_id].copy()
    if "competencia" in data.columns:
        data = data.sort_values("competencia")
    return data


def get_client_nba(nba: pd.DataFrame, persona_id: str) -> dict[str, Any] | None:
    if nba.empty or "persona_id" not in nba.columns:
        return None
    rows = nba[nba["persona_id"] == persona_id]
    if rows.empty:
        return None
    return rows.iloc[0].to_dict()
