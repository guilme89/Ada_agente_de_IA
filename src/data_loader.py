from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Any


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "data"


def load_json(relative_path: str) -> Any:
    path = DATA_DIR / relative_path
    with path.open("r", encoding="utf-8") as file:
        return json.load(file)


def load_csv(relative_path: str) -> list[dict[str, str]]:
    path = DATA_DIR / relative_path
    with path.open("r", encoding="utf-8-sig", newline="") as file:
        return list(csv.DictReader(file))


def load_core_data() -> dict[str, Any]:
    return {
        "perfil": load_json("perfil_investidor.json"),
        "produtos": load_json("produtos_financeiros.json"),
        "transacoes": load_csv("transacoes.csv"),
        "historico_atendimento": load_csv("historico_atendimento.csv"),
    }


def load_crm_data() -> dict[str, Any]:
    return {
        "clientes": load_csv("crm/clientes_atual_v4.csv"),
        "historico_12m": load_csv("crm/historico_12m_v4.csv"),
        "next_best_action": load_csv("crm/next_best_action_v4.csv"),
        "base_consolidada": load_json("crm/base_crm_preditiva_v4.json"),
    }


if __name__ == "__main__":
    core = load_core_data()
    crm = load_crm_data()
    print("Arquivos principais carregados:", core.keys())
    print("CRM carregado:", crm.keys())
