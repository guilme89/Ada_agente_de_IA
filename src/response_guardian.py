from __future__ import annotations

import re


DANGEROUS_OUTPUT_PATTERNS = [
    r"você está aprovado",
    r"voce esta aprovado",
    r"limite aprovado",
    r"aprovação garantida",
    r"aprovacao garantida",
    r"limite garantido",
    r"isenção garantida",
    r"isencao garantida",
    r"envie seu cpf",
    r"mande seu cpf",
    r"envie sua senha",
    r"mande sua senha",
    r"envie sua fatura",
    r"mande sua fatura",
    r"digite o número do cartão",
    r"digite o numero do cartao",
]


def output_has_dangerous_claim(text: str) -> bool:
    normalized = text.lower()
    return any(re.search(pattern, normalized) for pattern in DANGEROUS_OUTPUT_PATTERNS)


def enforce_output_guardrails(text: str, fallback: str) -> str:
    if not text or output_has_dangerous_claim(text):
        return fallback

    lower = text.lower()
    needs_guardrail = any(term in lower for term in ["cartão", "cartao", "aprovação", "aprovacao", "limite", "contratação", "contratacao"])
    already_has_guardrail = any(term in lower for term in ["canais oficiais", "não garante", "nao garante", "confirmadas"])

    if needs_guardrail and not already_has_guardrail:
        text += (
            "\n\nObservação: esta orientação é educativa e consultiva. Aprovação, limite, contratação "
            "e condições finais devem ser confirmadas nos canais oficiais."
        )

    return text
