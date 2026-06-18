from __future__ import annotations

from typing import Any


def recommend_card(profile: dict[str, Any], products: list[dict[str, Any]]) -> dict[str, str]:
    """Recomendação educativa por aderência. Não representa aprovação real."""
    cartoes = {item["id"]: item for item in products if item.get("categoria") == "cartao_credito_principal"}

    cartao_info = profile.get("cartoes", {})
    viagens = int(cartao_info.get("viagens_internacionais_ano_mock", 0))
    gasto = float(cartao_info.get("gasto_mensal_cartao_estimado_mock", 0))
    sala_vip = str(cartao_info.get("interesse_sala_vip", "")).lower()
    pontos = str(cartao_info.get("interesse_pontos_milhas", "")).lower()

    if viagens >= 6 and sala_vip == "alta":
        produto = cartoes.get("visa_aeternum")
    elif viagens >= 3 and gasto >= 25000:
        produto = cartoes.get("the_platinum_card")
    else:
        produto = cartoes.get("cartao_bradesco_principal")

    if not produto:
        return {
            "cartao": "Não identificado",
            "motivo": "Não encontrei produto aderente na base.",
            "guardrail": "Confirmar informações nos canais oficiais."
        }

    return {
        "cartao": produto["nome"],
        "motivo": produto["indicado_para"],
        "guardrail": produto["guardrail"]
    }


def format_recommendation(result: dict[str, str]) -> str:
    return (
        f"Com base no perfil informado, o cartão com maior aderência parece ser "
        f"{result['cartao']}. {result['motivo']} "
        f"{result['guardrail']}"
    )
