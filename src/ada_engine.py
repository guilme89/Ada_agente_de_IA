from __future__ import annotations

from typing import Any
import pandas as pd

from safety import validate_user_message, safe_refusal
from intent_router import detect_intent
from card_engine import recommend_card_from_inputs, recommend_card_from_profile
from analytics import calculate_financial_snapshot, get_client_nba
from context_builder import build_llm_user_prompt
from llm_client import LLMClient
from response_guardian import enforce_output_guardrails


OFFICIAL_CHANNELS = "app, Internet Banking, agência, gerente ou canais oficiais do Bradesco"


def money(value: Any) -> str:
    try:
        return f"R$ {float(value):,.0f}".replace(",", ".")
    except (TypeError, ValueError):
        return "não informado"


def pct(value: Any) -> str:
    try:
        return f"{float(value) * 100:.1f}%".replace(".", ",")
    except (TypeError, ValueError):
        return "não informado"


def build_guardrail() -> str:
    return (
        "Essa orientação é educativa e consultiva. Aprovação, limite, contratação, elegibilidade, "
        f"anuidade e condições finais devem ser confirmadas nos {OFFICIAL_CHANNELS}."
    )


def summarize_profile(profile: dict[str, Any], nba: dict[str, Any] | None = None) -> str:
    snapshot = calculate_financial_snapshot(profile)
    card = recommend_card_from_profile(profile)

    nba_text = ""
    if nba:
        nba_text = (
            f"\n\n**Next Best Action mockada:** {nba.get('next_best_action_mock', 'não informada')}.\n"
            f"**Canal sugerido:** {nba.get('melhor_canal_prescritivo_mock', 'não informado')}.\n"
            f"**Motivo:** {nba.get('motivo_nba', 'não informado')}"
        )

    return (
        f"**Resumo consultivo do perfil mockado**\n\n"
        f"- **Persona:** {profile.get('persona_id', 'não informado')} — {profile.get('nome_ficticio', 'cliente mockado')}\n"
        f"- **Segmento atual:** {profile.get('segmento_atual', 'não informado')}\n"
        f"- **Perfil profissional:** {profile.get('perfil_profissional', 'não informado')}\n"
        f"- **Momento de vida:** {profile.get('ciclo_vida', 'não informado')}\n"
        f"- **Prioridade de planejamento:** {profile.get('prioridade_planejamento', 'não informado')}\n"
        f"- **Patrimônio investível mock:** {money(snapshot['patrimonio_investivel'])}\n"
        f"- **Share wallet mock:** {pct(snapshot['share_wallet'])}\n"
        f"- **Gasto mensal em cartão mock:** {money(snapshot['gasto_cartao'])}\n"
        f"- **Cartão com maior aderência:** {card.card}\n"
        f"- **Justificativa:** {card.rationale}\n"
        f"{nba_text}\n\n"
        f"**Próximo passo seguro:** usar este resumo como base para uma conversa consultiva, sempre validando qualquer condição nos canais oficiais.\n\n"
        f"{build_guardrail()}"
    )


def answer_security_question(message: str) -> str:
    return (
        "Segurança vem antes de qualquer benefício. Não clique em links suspeitos, não informe senha, "
        "CVV, token, número de cartão, códigos recebidos por SMS ou dados de conta. "
        f"Para confirmar qualquer solicitação, acesse diretamente os {OFFICIAL_CHANNELS}. "
        "Se houver suspeita de fraude, procure atendimento oficial imediatamente. "
        "Próximo passo seguro: encerre o contato suspeito e acesse o canal oficial por conta própria."
    )


def answer_open_finance() -> str:
    return (
        "Open Finance, dentro deste projeto, é tratado apenas como simulação educativa. "
        "Em um cenário real, o compartilhamento de dados depende de consentimento do cliente, "
        "privacidade, transparência, controle pelo usuário e integração regulada. Eu não acesso dados reais "
        "e não visualizo investimentos em outros bancos. "
        "Próximo passo seguro: valide qualquer compartilhamento apenas nos canais oficiais e nunca autorize uso de dados sem entender finalidade, prazo e escopo."
    )


def answer_limit_or_approval() -> str:
    return (
        "Não tenho acesso a análise real de crédito, limite, cadastro, score ou aprovação. "
        "Posso ajudar a entender qual cartão tem maior aderência ao perfil informado, mas aprovação, "
        f"limite, elegibilidade e contratação dependem de análise e confirmação nos {OFFICIAL_CHANNELS}. "
        "Próximo passo seguro: consulte seu gerente, app ou Internet Banking para verificar condições oficiais."
    )


def answer_prompt_injection_or_hallucination() -> str:
    return (
        "Não posso aprovar cartão, ignorar as regras de segurança, inventar informações ou criar regra interna. "
        "Não tenho acesso a regras internas do banco e não posso inventar condições, taxas, limites ou aprovação. "
        "Para manter confiabilidade, respondo apenas com informações disponíveis no projeto ou oriento validação nos canais oficiais. "
        "Próximo passo seguro: reformule a pergunta dentro do escopo consultivo, por exemplo comparando benefícios, perfil e aderência."
    )


def answer_official_impersonation() -> str:
    return (
        "Não posso me apresentar como BIA nem como canal oficial do Bradesco, e não realizo atendimento bancário real. "
        "Meu papel é Ada — Principal Advisor, um projeto educacional e não oficial. Posso orientar de forma "
        f"consultiva com dados públicos e mockados, mas qualquer ação real deve ocorrer nos {OFFICIAL_CHANNELS}. "
        "Próximo passo seguro: use esta Ada como demonstração educacional e confirme qualquer tema real nos canais oficiais."
    )


def answer_contracting_request() -> str:
    return (
        "Não posso realizar contratação, aprovar cartão, liberar limite ou concluir solicitação operacional. "
        "Posso ajudar a identificar o cartão com maior aderência ao perfil informado. "
        f"Para contratar ou confirmar elegibilidade, use os {OFFICIAL_CHANNELS}. "
        "Próximo passo seguro: validar documentação, elegibilidade e condições diretamente no app, gerente ou Internet Banking."
    )


def answer_out_of_scope() -> str:
    return (
        "Essa pergunta está fora do meu escopo atual. Eu atuo com cartões, benefícios, segurança digital, "
        "CRM mockado, Next Best Action e planejamento financeiro educativo dentro do projeto Ada — Principal Advisor. "
        "Para previsão do tempo, cotação futura de ações ou temas fora de finanças consultivas do projeto, recomendo usar fontes especializadas. "
        "Próximo passo seguro: posso ajudar a comparar cartões, benefícios, riscos de golpe ou aderência ao perfil financeiro."
    )


def answer_investment_personalized() -> str:
    return (
        "Posso ajudar de forma educativa a organizar critérios de análise, como liquidez, risco, horizonte, "
        "objetivos, diversificação e proteção patrimonial. Mas não posso dizer exatamente em qual fundo você "
        f"deve investir nem fazer recomendação personalizada definitiva. Para decisão real, procure profissional habilitado e os {OFFICIAL_CHANNELS}. "
        "Próximo passo seguro: montar uma matriz de objetivos, liquidez e risco antes de conversar com um especialista."
    )


def answer_card_recommendation(message: str, selected_profile: dict[str, Any] | None = None) -> str:
    text = message.lower()

    # When the user's question contains explicit preferences, prioritize the message over the selected mock profile.
    explicit_lifestyle = any(term in text for term in ["lifestyle", "experiência", "experiencias", "premium", "sofisticação", "sofisticacao"])
    explicit_balance = any(term in text for term in ["equilibrado", "equilíbrio", "equilibrio", "relacionamento", "custo", "pontos"])
    explicit_travel = any(term in text for term in ["viajo bastante", "viajo muito", "salas vip", "sala vip", "internacional"])

    if explicit_lifestyle or explicit_balance or explicit_travel or not selected_profile:
        if explicit_balance:
            viagens, gasto, vip, pontos, prioridade = 2, 15000, "Média", "Alta", "equilíbrio entre pontos e benefícios"
        elif explicit_lifestyle:
            viagens, gasto, vip, pontos, prioridade = 5, 30000, "Média", "Média", "experiências premium e lifestyle"
        else:
            viagens, gasto, vip, pontos, prioridade = 8, 45000, "Alta", "Alta", "viagem internacional e salas VIP"

        rec = recommend_card_from_inputs(
            viagens_ano=viagens,
            gasto_mensal=gasto,
            interesse_sala_vip=vip,
            interesse_pontos=pontos,
            prioridade=prioridade,
            segmento_atual=(selected_profile or {}).get("segmento_atual", "Principal"),
            patrimonio_investivel=float((selected_profile or {}).get("patrimonio_investivel_estimado_mock", 1000000) or 1000000),
        )
        return (
            f"Com base no que você informou, o cartão com maior aderência parece ser **{rec.card}**.\n\n"
            f"**Motivo:** {rec.rationale}\n\n"
            f"**Próximo passo:** {rec.next_step}\n\n"
            f"{rec.guardrail}"
        )

    rec = recommend_card_from_profile(selected_profile)
    return (
        f"Com base no perfil mockado selecionado, o cartão com maior aderência parece ser "
        f"**{rec.card}**.\n\n"
        f"**Por quê:** {rec.rationale}\n\n"
        f"**Score consultivo de aderência:** {rec.score}/100.\n\n"
        f"**Próximo passo seguro:** {rec.next_step}\n\n"
        f"{rec.guardrail}"
    )


def answer_prime_to_principal(selected_profile: dict[str, Any] | None = None) -> str:
    if selected_profile and selected_profile.get("segmento_atual") == "Prime":
        score = selected_profile.get("score_potencial_principal_mock", "não informado")
        prob = selected_profile.get("probabilidade_migracao_12m_pct_mock", "não informado")
        return (
            "O perfil mockado selecionado apresenta uma possível trilha de evolução de Prime para Principal.\n\n"
            f"- **Score potencial mock:** {score}\n"
            f"- **Probabilidade de migração 12m mock:** {prob}%\n"
            f"- **Gatilho:** {selected_profile.get('principal_gatilho_oportunidade', 'não informado')}\n"
            f"- **Próximo passo:** {selected_profile.get('proximo_passo_sugerido', 'conversa consultiva com gerente')}\n\n"
            f"{build_guardrail()}"
        )

    return (
        "Para avaliar uma trilha Prime → Principal, eu consideraria crescimento de renda, novo aporte, "
        "patrimônio investível, uso do cartão, interesse em benefícios premium e necessidade de atendimento consultivo. "
        f"A migração real deve ser avaliada nos {OFFICIAL_CHANNELS}. "
        "Próximo passo seguro: conversar com gerente ou canal oficial para validar aderência, relacionamento e condições."
    )


def answer_competitor_comparison() -> str:
    return (
        "Entendo a comparação. Para comparar bem, não olhe apenas anuidade: compare benefícios realmente usados, pontos, salas VIP, seguros, atendimento, "
        "segurança, relacionamento, cartões adicionais e suporte consultivo. A melhor escolha depende do valor percebido no seu uso real. "
        f"Próximo passo seguro: montar uma comparação lado a lado e validar condições nos {OFFICIAL_CHANNELS}. "
        "Essa orientação é consultiva e não garante aprovação, limite ou isenção."
    )


def answer_irritated_client() -> str:
    return (
        "Entendo sua irritação. Antes de cancelar, vale comparar custo versus benefícios efetivamente usados: pontos, salas VIP, seguros, "
        "serviços digitais, atendimento e relacionamento. Se o valor percebido estiver baixo, a próxima melhor ação é revisar o pacote e "
        f"conversar com gerente ou canais oficiais. Próximo passo seguro: pedir uma revisão consultiva sem tomar decisão por impulso. "
        "Não posso cancelar ou prometer retenção, mas posso ajudar a organizar a análise."
    )


def answer_confused_client() -> str:
    return (
        "Explicando de forma simples: pontos são recompensas geradas pelo uso do cartão; milhas são pontos usados principalmente em viagens; "
        "salas VIP são espaços em aeroportos com mais conforto antes do embarque. O que importa é escolher benefícios que você realmente usa. "
        f"Próximo passo seguro: identificar se sua prioridade é viagem, pontos, praticidade ou relacionamento e confirmar detalhes nos {OFFICIAL_CHANNELS}."
    )


def answer_nonexistent_benefit() -> str:
    return (
        "Não encontrei base para afirmar esse benefício como garantido. Upgrade de hotel, passagem de primeira classe ou qualquer condição especial "
        "não deve ser tratada como garantia sem fonte oficial. "
        f"Próximo passo seguro: confirmar benefícios vigentes nos {OFFICIAL_CHANNELS} antes de tomar decisão. "
        "Essa orientação evita alucinação e promessa indevida."
    )


def answer_partial_card_or_invoice() -> str:
    return (
        "Mesmo com apenas os últimos dígitos, não posso consultar fatura, cartão, conta ou qualquer informação operacional real. "
        f"Próximo passo seguro: acesse diretamente os {OFFICIAL_CHANNELS} para consultar fatura, limite ou status do cartão. "
        "Não envie número de cartão, CPF, senha, CVV, fatura ou extrato em conversas."
    )


def answer_multi_llm_safety() -> str:
    return (
        "Sim, a Ada foi preparada para operar com LLMs como OpenAI/ChatGPT, Gemini, Claude e Qwen, mantendo uma camada local de segurança. "
        "A pergunta passa primeiro por guardrails locais; depois o motor determinístico gera uma resposta segura; só então a LLM pode reescrever; "
        "por fim, o Response Guardian valida a saída e usa fallback se houver risco. "
        "Próximo passo seguro: rodar em modo mock para demonstração e ativar provedores reais apenas com variáveis de ambiente, nunca com chaves no GitHub. "
        "Essa é uma orientação educativa; qualquer uso real deve manter logs, guardrails e canais oficiais de governança."
    )



def answer_nba_retention() -> str:
    return (
        "Para um cliente com risco de churn que quer sair para outro banco, a Next Best Action deve priorizar retenção consultiva antes de oferta. "
        "O caminho é entender a insatisfação, comparar benefícios usados, anuidade, atendimento, salas VIP, pontos, segurança e relacionamento. "
        "Próximo passo seguro: acionar gerente ou canais oficiais para revisar a proposta de valor com venda responsável e sem promessa de condição comercial. "
        "Essa orientação é educativa e não garante condição comercial."
    )


def answer_wealth_planning_case() -> str:
    return (
        "Quando o cliente vendeu um imóvel e quer organizar patrimônio, proteção familiar e cartão, a prioridade deve ser planejamento financeiro educativo. "
        "A análise deve considerar liquidez, reserva, proteção familiar, sucessão, diversificação, uso do cartão e benefícios aderentes ao novo momento patrimonial. "
        "Próximo passo seguro: agendar conversa consultiva com gerente/especialista nos canais oficiais para validar objetivos e alternativas. "
        "Não faço recomendação personalizada definitiva nem prometo resultado."
    )



def generate_response(
    message: str,
    selected_profile: dict[str, Any] | None = None,
    nba_df: pd.DataFrame | None = None,
    products: list[dict[str, Any]] | None = None,
    system_prompt: str | None = None,
    use_llm: bool = False,
    llm_provider: str = "mock",
    llm_model: str | None = None,
) -> dict[str, Any]:
    is_safe, refusal = validate_user_message(message)
    intent = detect_intent(message)

    if not is_safe:
        return {
            "intent": "bloqueio_seguranca",
            "confidence": 1.0,
            "answer": refusal or safe_refusal(),
            "blocked": True,
        }

    nba = None
    if selected_profile and nba_df is not None and not nba_df.empty:
        nba = get_client_nba(nba_df, selected_profile.get("persona_id", ""))

    if intent.name == "seguranca":
        answer = answer_security_question(message)
    elif intent.name == "open_finance":
        answer = answer_open_finance()
    elif intent.name == "limite_aprovacao":
        answer = answer_limit_or_approval()
    elif intent.name == "prompt_injection":
        answer = answer_prompt_injection_or_hallucination()
    elif intent.name == "representacao_oficial":
        answer = answer_official_impersonation()
    elif intent.name == "contratacao_operacional":
        answer = answer_contracting_request()
    elif intent.name == "fora_escopo":
        answer = answer_out_of_scope()
    elif intent.name == "nba_retencao":
        answer = answer_nba_retention()
    elif intent.name == "wealth_planning":
        answer = answer_wealth_planning_case()
    elif intent.name == "comparacao_concorrente":
        answer = answer_competitor_comparison()
    elif intent.name == "cliente_irritado":
        answer = answer_irritated_client()
    elif intent.name == "cliente_confuso":
        answer = answer_confused_client()
    elif intent.name == "beneficio_inexistente":
        answer = answer_nonexistent_benefit()
    elif intent.name == "dados_parciais":
        answer = answer_partial_card_or_invoice()
    elif intent.name == "multi_llm":
        answer = answer_multi_llm_safety()
    elif intent.name == "planejamento" and any(term in message.lower() for term in ["exatamente", "qual fundo", "devo investir", "invista"]):
        answer = answer_investment_personalized()
    elif intent.name in {"cartao", "recomendacao"}:
        answer = answer_card_recommendation(message, selected_profile)
    elif intent.name == "prime_principal":
        answer = answer_prime_to_principal(selected_profile)
    elif intent.name in {"crm", "planejamento"} and selected_profile:
        answer = summarize_profile(selected_profile, nba)
    else:
        answer = (
            "Posso te ajudar de forma consultiva com cartões Principal, benefícios, salas VIP, pontos, "
            "segurança digital, planejamento financeiro educativo, CRM mockado e Next Best Action. "
            "Para uma recomendação mais precisa, me diga se sua prioridade é viagem, pontos, isenção, "
            "benefícios premium, segurança ou relacionamento completo. Próximo passo seguro: escolha uma prioridade e eu sigo com uma recomendação por aderência."
        )

    llm_metadata = {
        "used_llm": False,
        "llm_provider": None,
        "llm_model": None,
        "llm_ok": None,
        "llm_error": None,
    }

    if use_llm:
        safe_fallback = answer
        llm_user_prompt = build_llm_user_prompt(
            user_message=message,
            deterministic_answer=answer,
            profile=selected_profile,
            products=products,
            nba_row=nba,
        )
        llm_client = LLMClient(provider=llm_provider, model=llm_model)
        llm_response = llm_client.generate(
            system_prompt=system_prompt or "Você é a Ada — Principal Advisor. Responda com segurança, clareza e guardrails.",
            user_prompt=llm_user_prompt,
        )
        llm_metadata = {
            "used_llm": True,
            "llm_provider": llm_response.provider,
            "llm_model": llm_response.model,
            "llm_ok": llm_response.ok,
            "llm_error": llm_response.error,
        }
        if llm_response.ok:
            answer = enforce_output_guardrails(llm_response.text, fallback=safe_fallback)
        else:
            answer = safe_fallback + (
                "\n\n[Modo LLM indisponível: resposta segura gerada pelo motor determinístico local.]"
            )

    return {
        "intent": intent.name,
        "confidence": intent.confidence,
        "answer": answer,
        "blocked": False,
        **llm_metadata,
    }
