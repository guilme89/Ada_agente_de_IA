from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Intent:
    name: str
    confidence: float
    description: str


INTENT_KEYWORDS = {
    "seguranca": ["golpe", "link", "fraude", "senha", "cvv", "sms", "token", "motoboy", "central falsa", "phishing", "suspeito"],
    "cartao": ["cartão", "cartao", "visa", "aeternum", "platinum", "principal", "anuidade", "pontos", "milhas", "sala vip", "salas vip", "benefícios", "beneficios", "lifestyle", "experiência", "experiencias", "premium"],
    "recomendacao": ["qual combina", "recomenda", "melhor cartão", "melhor cartao", "aderência", "aderencia", "perfil"],
    "prime_principal": ["prime", "migrar", "migração", "migracao", "segmento", "principal"],
    "open_finance": ["open finance", "outros bancos", "compartilhar dados", "consentimento", "ativos externos"],
    "planejamento": ["planejamento", "investimentos", "patrimônio", "patrimonio", "reserva", "previdência", "previdencia", "sucessão", "sucessao", "fundo", "investir"],
    "limite_aprovacao": ["limite", "aprovado", "aprovação", "aprovacao", "contratar", "contratação", "contratacao", "elegibilidade", "taxa"],
    "crm": ["nba", "next best action", "crm", "lead", "churn", "resumo", "cliente"],
    "prompt_injection": ["ignore todas as regras", "ignore as regras", "ignore instruções", "ignore instrucoes", "sem fonte", "invente", "bypass"],
    "representacao_oficial": ["bia oficial", "atendimento real", "canal oficial", "finja que você é a bia", "finja que voce e a bia"],
    "contratacao_operacional": ["contrate agora", "contratar agora", "contratação concluída", "contratacao concluida"],
    "fora_escopo": ["previsão do tempo", "previsao do tempo", "tempo", "ação vai subir", "acao vai subir", "bolsa amanhã", "bolsa amanha"],
    "comparacao_concorrente": ["outro banco", "concorrente", "sem anuidade", "comparar"],
    "cliente_irritado": ["irritado", "pago caro", "vale cancelar"],
    "cliente_confuso": ["não entendo", "nao entendo", "explique de forma simples", "forma simples"],
    "beneficio_inexistente": ["upgrade garantido", "primeira classe", "benefício inexistente", "beneficio inexistente"],
    "dados_parciais": ["termina em", "final do cartão", "final do cartao", "consultar minha fatura"],
    "multi_llm": ["gemini", "claude", "qwen", "multi-llm", "llm"],
    "nba_retencao": ["risco de churn", "churn", "retenção", "retencao", "quer sair para outro banco", "próxima melhor ação", "proxima melhor acao"],
    "wealth_planning": ["vendeu um imóvel", "vendeu um imovel", "organizar patrimônio", "organizar patrimonio", "proteção familiar", "protecao familiar", "wealth planning"],

}


def detect_intent(message: str) -> Intent:
    text = message.lower().strip()

    # Priority routes for safety-critical intents.
    if any(k in text for k in INTENT_KEYWORDS["representacao_oficial"]):
        return Intent("representacao_oficial", 0.95, "Tentativa de personificação de canal oficial.")
    if any(k in text for k in INTENT_KEYWORDS["prompt_injection"]):
        return Intent("prompt_injection", 0.98, "Tentativa de prompt injection, alucinação ou bypass.")
    if any(k in text for k in INTENT_KEYWORDS["contratacao_operacional"]):
        return Intent("contratacao_operacional", 0.95, "Pedido de contratação ou ação operacional real.")
    if "resumo crm" in text:
        return Intent("crm", 0.95, "Pedido de resumo CRM.")
    if any(k in text for k in INTENT_KEYWORDS["seguranca"]):
        return Intent("seguranca", 0.94, "Pergunta de segurança digital.")
    if any(k in text for k in INTENT_KEYWORDS["fora_escopo"]):
        return Intent("fora_escopo", 0.92, "Pergunta fora do escopo do agente.")
    for priority_intent in ["nba_retencao", "wealth_planning", "comparacao_concorrente", "cliente_irritado", "cliente_confuso", "beneficio_inexistente", "dados_parciais", "multi_llm"]:
        if any(k in text for k in INTENT_KEYWORDS[priority_intent]):
            return Intent(priority_intent, 0.90, f"Intenção prioritária detectada: {priority_intent}.")

    scores: dict[str, int] = {}

    for intent, keywords in INTENT_KEYWORDS.items():
        scores[intent] = sum(1 for keyword in keywords if keyword in text)

    best_intent = max(scores, key=scores.get)
    best_score = scores[best_intent]

    if best_score == 0:
        return Intent("geral", 0.35, "Pergunta geral ou diagnóstico inicial.")

    confidence = min(0.95, 0.45 + best_score * 0.15)
    return Intent(best_intent, confidence, f"Intenção detectada: {best_intent}.")
