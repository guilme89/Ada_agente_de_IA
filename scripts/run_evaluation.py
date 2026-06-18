from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT / "src"))

from evaluator import run_evaluation, save_report


def main():
    report = run_evaluation()
    paths = save_report(report)

    summary = report["summary"]
    print("=== Ada — Relatório de Avaliação ===")
    print(f"Casos totais: {summary['total_cases']}")
    print(f"Aprovados: {summary['passed_cases']}")
    print(f"Taxa geral: {summary['overall_pass_rate']:.0%}")
    print(f"Taxa segurança: {summary['safety_pass_rate']:.0%}")
    print(f"Taxa críticos: {summary['critical_pass_rate']:.0%}")
    print(f"Acurácia recomendação: {summary['recommendation_accuracy']:.0%}")
    print(f"Status: {'APROVADO' if summary['approved'] else 'REPROVADO'}")
    print("")
    print("Arquivos gerados:")
    for key, path in paths.items():
        print(f"- {key}: {path}")

    if not summary["approved"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
