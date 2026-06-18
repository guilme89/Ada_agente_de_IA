from __future__ import annotations

from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
PROMPTS_DIR = PROJECT_ROOT / "prompts"


def load_prompt(filename: str) -> str:
    path = PROMPTS_DIR / filename
    return path.read_text(encoding="utf-8")


def load_all_prompts() -> dict[str, str]:
    prompts = {}
    for path in sorted(PROMPTS_DIR.glob("*.md")):
        prompts[path.stem] = path.read_text(encoding="utf-8")
    return prompts


def build_master_prompt() -> str:
    prompts = load_all_prompts()
    sections = []
    for name, content in prompts.items():
        sections.append(f"\n\n<!-- {name} -->\n{content}")
    return "\n".join(sections)


if __name__ == "__main__":
    prompts = load_all_prompts()
    print(f"Total de prompts carregados: {len(prompts)}")
    for name, content in prompts.items():
        print(f"{name}: {len(content)} caracteres")
