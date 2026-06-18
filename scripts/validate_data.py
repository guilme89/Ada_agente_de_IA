from __future__ import annotations

import csv
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"

REQUIRED_FILES = [
    DATA / "perfil_investidor.json",
    DATA / "produtos_financeiros.json",
    DATA / "transacoes.csv",
    DATA / "historico_atendimento.csv",
    DATA / "crm" / "clientes_atual_v4.csv",
    DATA / "crm" / "historico_12m_v4.csv",
    DATA / "crm" / "next_best_action_v4.csv",
    DATA / "crm" / "base_crm_preditiva_v4.json",
]

SENSITIVE_KEYS = {
    "cpf", "rg", "telefone", "email", "e-mail", "endereco", "endereço",
    "conta", "agencia", "agência", "cartao_numero", "numero_cartao",
    "senha", "cvv", "fatura_real", "extrato_real", "chave_pix"
}

SENSITIVE_PATTERNS = [
    re.compile(r"\b\d{3}\.?\d{3}\.?\d{3}-?\d{2}\b"),
    re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"),
]


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as file:
        return list(csv.DictReader(file))


def scan_for_sensitive_keys(obj, path="root"):
    if isinstance(obj, dict):
        for key, value in obj.items():
            if key.lower() in SENSITIVE_KEYS:
                raise AssertionError(f"Chave sensível encontrada: {path}.{key}")
            scan_for_sensitive_keys(value, f"{path}.{key}")
    elif isinstance(obj, list):
        for i, item in enumerate(obj):
            scan_for_sensitive_keys(item, f"{path}[{i}]")


def scan_text_for_sensitive_patterns(text: str):
    for pattern in SENSITIVE_PATTERNS:
        if pattern.search(text):
            raise AssertionError("Possível dado sensível encontrado por padrão regex.")


def validate():
    for file in REQUIRED_FILES:
        assert file.exists(), f"Arquivo obrigatório não encontrado: {file}"

    perfil = json.loads((DATA / "perfil_investidor.json").read_text(encoding="utf-8"))
    produtos = json.loads((DATA / "produtos_financeiros.json").read_text(encoding="utf-8"))
    crm_json = json.loads((DATA / "crm" / "base_crm_preditiva_v4.json").read_text(encoding="utf-8"))

    assert perfil["segmento_atual"] in {"Principal", "Prime"}
    assert len(produtos) >= 6
    assert "clientes_atual" in crm_json
    assert len(crm_json["clientes_atual"]) == 100

    clientes = read_csv(DATA / "crm" / "clientes_atual_v4.csv")
    historico = read_csv(DATA / "crm" / "historico_12m_v4.csv")
    nba = read_csv(DATA / "crm" / "next_best_action_v4.csv")

    assert len(clientes) == 100
    assert len(historico) == 1200
    assert len(nba) == 100

    texto_total = ""
    for file in REQUIRED_FILES:
        texto_total += file.read_text(encoding="utf-8", errors="ignore")[:200000]

    scan_text_for_sensitive_patterns(texto_total)
    scan_for_sensitive_keys(perfil)
    scan_for_sensitive_keys(produtos)
    scan_for_sensitive_keys(crm_json)

    print("Validação concluída com sucesso. Estrutura, dados e privacidade estão OK.")


if __name__ == "__main__":
    validate()
