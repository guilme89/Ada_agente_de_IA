from pathlib import Path
import json
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]


def test_final_docs_exist():
    required = [
        "README.md",
        "CHECKLIST_ENTREGA.md",
        "docs/05-pitch.md",
        "docs/07-revisao-final-github.md",
    ]
    for rel in required:
        assert (ROOT / rel).exists()


def test_final_report_is_approved():
    report = json.loads((ROOT / "reports" / "evaluation_report.json").read_text(encoding="utf-8"))
    summary = report["summary"]
    assert summary["approved"] is True
    assert summary["overall_pass_rate"] == 1.0
    assert summary["nota_media_1_10"] == 10.0
    assert summary["unsafe_output_rate"] == 0.0


def test_final_package_validator_runs():
    result = subprocess.run(
        [sys.executable, "scripts/validate_final_package.py"],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
        timeout=30,
    )
    assert result.returncode == 0, result.stdout + result.stderr


def test_gitignore_blocks_secret_files():
    gitignore = (ROOT / ".gitignore").read_text(encoding="utf-8")
    assert ".env" in gitignore
    assert ".streamlit/secrets.toml" in gitignore
    assert "*.key" in gitignore


def test_checklist_mentions_github_publication():
    checklist = (ROOT / "CHECKLIST_ENTREGA.md").read_text(encoding="utf-8").lower()
    assert "github" in checklist
    assert "não oficial" in checklist
    assert "python scripts/validate_final_package.py" in checklist
