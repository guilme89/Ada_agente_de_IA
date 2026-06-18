from __future__ import annotations

from typing import Any
import json


MAX_CONTEXT_CHARS = 9000


def compact_dict(data: dict[str, Any], keys: list[str]) -> dict[str, Any]:
    return {key: data.get(key) for key in keys if key in data}


def build_profile_context(profile: dict[str, Any] | None) -> str:
    if not profile:
        return "Nenhuma persona mockada selecionada."

    keys = [
        "persona_id",
        "nome_ficticio",
        "segmento_atual",
        "segmento_alvo",
        "temperatura_lead",
        "score_potencial_principal_mock",
        "probabilidade_migracao_12m_pct_mock",
        "perfil_profissional",
        "ciclo_vida",
        "prioridade_planejamento",
        "segmentacao_psicologica_mock",
        "estilo_decisao_mock",
        "risco_churn_mock",
        "patrimonio_investivel_estimado_mock",
        "investimentos_bradesco_estimado_mock",
        "aporte_previsto_12m_mock",
        "gasto_mensal_cartao_estimado_mock",
        "viagens_internacionais_ano_mock",
        "interesse_sala_vip",
        "interesse_pontos_milhas",
        "interesse_isencao_anuidade",
        "cartao_recomendado_ada",
        "motivo_recomendacao_cartao",
        "proximo_passo_sugerido",
    ]
    return json.dumps(compact_dict(profile, keys), ensure_ascii=False, indent=2)


def build_products_context(products: list[dict[str, Any]] | None) -> str:
    if not products:
        return "Nenhum produto carregado."
    compact = []
    for item in products[:10]:
        compact.append(
            compact_dict(
                item,
                ["id", "nome", "categoria", "publico", "beneficios_resumidos", "indicado_para", "guardrail", "fonte_publica"],
            )
        )
    return json.dumps(compact, ensure_ascii=False, indent=2)


def build_nba_context(nba_row: dict[str, Any] | None) -> str:
    if not nba_row:
        return "Nenhuma Next Best Action mockada encontrada."
    keys = [
        "next_best_action_mock",
        "produto_ou_tema_prioritario",
        "melhor_canal_prescritivo_mock",
        "urgencia",
        "motivo_nba",
        "mensagem_consultiva_sugerida",
        "guardrail",
    ]
    return json.dumps(compact_dict(nba_row, keys), ensure_ascii=False, indent=2)


def build_llm_user_prompt(
    user_message: str,
    deterministic_answer: str,
    profile: dict[str, Any] | None = None,
    products: list[dict[str, Any]] | None = None,
    nba_row: dict[str, Any] | None = None,
) -> str:
    prompt = f"""
Você é a camada LLM da Ada — Principal Advisor.

Tarefa:
Reescreva ou complemente a resposta determinística abaixo mantendo o mesmo conteúdo factual, os guardrails e o tom consultivo premium.
Não invente taxas, regras, limites, elegibilidade, aprovação ou condições.
Não peça dados sensíveis.
Responda em português do Brasil.

Mensagem do usuário:
{user_message}

Resposta determinística segura:
{deterministic_answer}

Contexto da persona mockada:
{build_profile_context(profile)}

Produtos/serviços carregados:
{build_products_context(products)}

Next Best Action mockada:
{build_nba_context(nba_row)}

Saída esperada:
Uma resposta final pronta para o usuário, clara, consultiva e segura.
"""
    prompt = prompt.strip()
    if len(prompt) > MAX_CONTEXT_CHARS:
        prompt = prompt[:MAX_CONTEXT_CHARS] + "\n\n[Contexto truncado por segurança de tamanho.]"
    return prompt
