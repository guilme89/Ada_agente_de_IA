from __future__ import annotations

import re


FORBIDDEN_PATTERNS = {
    "cpf": r"\b\d{3}\.?\d{3}\.?\d{3}-?\d{2}\b",
    "cartao": r"\b(?:\d[ -]*?){13,19}\b",
    "email": r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b",
    "telefone": r"\b(?:\+55\s?)?(?:\(?\d{2}\)?\s?)?9?\d{4}[-\s]?\d{4}\b",
}

DISCLOSURE_PATTERNS = [
    r"\bmeu\s+cpf\s+(é|e|eh|:)",
    r"\bminha\s+senha\s+(é|e|eh|:)",
    r"\bmeu\s+cvv\s+(é|e|eh|:)",
    r"\bmeu\s+código\s+de\s+segurança\s+(é|e|eh|:)",
    r"\bmeu\s+codigo\s+de\s+segurança\s+(é|e|eh|:)",
    r"\bmeu\s+cart[aã]o\s+(é|e|eh|:)",
    r"\bminha\s+conta\s+(é|e|eh|:)",
    r"\bminha\s+ag[eê]ncia\s+(é|e|eh|:)",
]

OPERATIONAL_SENSITIVE_REQUESTS = [
    "acesse minha conta",
    "verifique minha conta",
    "verifique meu cartão",
    "verifique meu cartao",
    "consulte minha fatura",
    "consulte meu extrato",
    "veja minha fatura",
    "veja meu extrato",
    "usar minha senha",
    "usar meu cpf",
    "usar meu cartão",
    "usar meu cartao",
]

SENSITIVE_TERMS = [
    "senha", "cvv", "código de segurança", "codigo de segurança",
    "número do cartão", "numero do cartao", "fatura real",
    "extrato", "agência", "agencia", "conta corrente", "chave pix"
]

SECURITY_EDUCATION_TERMS = [
    "golpe", "fraude", "link suspeito", "suspeito", "phishing", "falsa central",
    "motoboy", "segurança", "seguranca", "o que faço", "o que faco",
    "não informar", "nao informar", "pedindo cvv", "pedindo senha",
    "ligou", "ligação", "ligacao", "posso passar", "cancelar uma compra", "falsa central"
]


def _has_regex_sensitive_value(text: str) -> bool:
    return any(re.search(pattern, text) for pattern in FORBIDDEN_PATTERNS.values())


def _looks_like_sensitive_disclosure(normalized: str) -> bool:
    return any(re.search(pattern, normalized) for pattern in DISCLOSURE_PATTERNS)


def _is_security_education_context(normalized: str) -> bool:
    return any(term in normalized for term in SECURITY_EDUCATION_TERMS)


def contains_sensitive_data(text: str) -> bool:
    normalized = text.lower()

    if _has_regex_sensitive_value(text):
        return True

    if _looks_like_sensitive_disclosure(normalized):
        return True

    if any(term in normalized for term in OPERATIONAL_SENSITIVE_REQUESTS):
        return True

    # If the user is asking how to stay safe, mentioning "CVV" or "senha" is allowed.
    if _is_security_education_context(normalized):
        return False

    # Sensitive terms outside a security-education context are blocked conservatively.
    if any(term in normalized for term in SENSITIVE_TERMS):
        return True

    return False


def safe_refusal() -> str:
    return (
        "Por segurança, não posso solicitar, armazenar ou analisar dados pessoais, "
        "bancários ou sensíveis. Para informações da sua conta, limite, contratação "
        "ou elegibilidade, consulte os canais oficiais do Bradesco."
    )


def validate_user_message(text: str) -> tuple[bool, str | None]:
    if contains_sensitive_data(text):
        return False, safe_refusal()
    return True, None
