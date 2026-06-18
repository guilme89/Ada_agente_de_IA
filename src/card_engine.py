from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass
class CardRecommendation:
    card: str
    score: int
    rationale: str
    guardrail: str
    next_step: str


def _level_to_score(value: str) -> int:
    value = (value or "").lower()
    if "alta" in value or "alto" in value:
        return 3
    if "média" in value or "medio" in value or "médio" in value:
        return 2
    if "baixa" in value or "baixo" in value:
        return 1
    return 0


def recommend_card_from_inputs(
    viagens_ano: int = 0,
    gasto_mensal: float = 0.0,
    interesse_sala_vip: str = "Média",
    interesse_pontos: str = "Média",
    prioridade: str = "equilíbrio",
    segmento_atual: str = "Principal",
    patrimonio_investivel: float = 0.0,
) -> CardRecommendation:
    vip_score = _level_to_score(interesse_sala_vip)
    pontos_score = _level_to_score(interesse_pontos)
    prioridade_norm = (prioridade or "").lower()
    segmento_norm = (segmento_atual or "").lower()

    aeternum_score = 0
    platinum_score = 0
    principal_score = 0

    aeternum_score += min(viagens_ano, 10) * 5
    aeternum_score += vip_score * 18
    aeternum_score += pontos_score * 8
    aeternum_score += 18 if gasto_mensal >= 30000 else 8 if gasto_mensal >= 15000 else 0
    aeternum_score += 12 if patrimonio_investivel >= 1500000 else 5 if patrimonio_investivel >= 500000 else 0
    aeternum_score += 10 if any(x in prioridade_norm for x in ["vip", "viagem", "internacional", "exclusividade"]) else 0

    platinum_score += min(viagens_ano, 8) * 4
    platinum_score += vip_score * 10
    platinum_score += 20 if any(x in prioridade_norm for x in ["lifestyle", "experiência", "experiencias", "premium", "sofisticação"]) else 0
    platinum_score += 10 if gasto_mensal >= 20000 else 5 if gasto_mensal >= 10000 else 0

    principal_score += 20
    principal_score += pontos_score * 12
    principal_score += 12 if gasto_mensal >= 12000 else 6
    principal_score += 12 if any(x in prioridade_norm for x in ["equilíbrio", "equilibrio", "isenção", "isencao", "relacionamento", "pontos"]) else 0
    principal_score += 10 if segmento_norm == "prime" else 5

    scores = {
        "Visa Aeternum": aeternum_score,
        "The Platinum Card®": platinum_score,
        "Bradesco Principal": principal_score,
    }

    card = max(scores, key=scores.get)
    score = min(100, int(scores[card]))

    if segmento_norm == "prime" and score >= 55:
        next_step = "Avaliar trilha de evolução para Principal com gerente ou canal oficial."
    else:
        next_step = "Validar condições, contratação e elegibilidade nos canais oficiais."

    # Balance/relationship should favor Bradesco Principal even when the client has strong assets.
    if any(x in prioridade_norm for x in ["equilíbrio", "equilibrio", "relacionamento", "isenção", "isencao"]):
        card = "Bradesco Principal"
        score = max(score, min(100, principal_score + 8))

    # Lifestyle/experiência premium should favor The Platinum Card® unless the profile is an extreme VIP traveler.
    elif any(x in prioridade_norm for x in ["lifestyle", "experiência", "experiencias", "premium", "sofisticação"]) and not (viagens_ano >= 8 and vip_score >= 3):
        card = "The Platinum Card®"
        score = max(score, min(100, platinum_score + 10))

    if card == "Visa Aeternum":
        rationale = "Alta aderência por viagens, salas VIP, benefícios internacionais, pontos e relacionamento premium."
    elif card == "The Platinum Card®":
        rationale = "Aderência por experiências premium, lifestyle, sofisticação e benefícios internacionais."
    else:
        rationale = "Aderência equilibrada para pontos, benefícios, uso diário, relacionamento e possibilidade de jornada Principal."

    guardrail = (
        "Recomendação educativa por aderência. Não garante aprovação, limite, elegibilidade, "
        "isenção de anuidade ou contratação."
    )

    return CardRecommendation(card=card, score=score, rationale=rationale, guardrail=guardrail, next_step=next_step)


def recommend_card_from_profile(profile: dict[str, Any]) -> CardRecommendation:
    return recommend_card_from_inputs(
        viagens_ano=int(float(profile.get("viagens_internacionais_ano_mock", 0) or 0)),
        gasto_mensal=float(profile.get("gasto_mensal_cartao_estimado_mock", 0) or 0),
        interesse_sala_vip=str(profile.get("interesse_sala_vip", "Média")),
        interesse_pontos=str(profile.get("interesse_pontos_milhas", "Média")),
        prioridade=str(profile.get("prioridade_cartao", "equilíbrio")),
        segmento_atual=str(profile.get("segmento_atual", "Principal")),
        patrimonio_investivel=float(profile.get("patrimonio_investivel_estimado_mock", 0) or 0),
    )
