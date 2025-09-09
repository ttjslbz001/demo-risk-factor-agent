from typing import List, TypedDict, Dict
from pathlib import Path
import re

from src.utils.app_logging import get_logger, log_json, start_timer, elapsed_ms


class Section(TypedDict, total=False):
    level: int
    title: str
    content: str
    summary: str


class RuleDocument(TypedDict):
    id: str
    title: str
    sections: List[Section]
    raw_markdown: str


logger = get_logger("rule_loader")
_HEADING_RE = re.compile(r"^(#{1,6})\s+(.*)$")


def _summarize(text: str, limit: int = 200) -> str:
    stripped = text.strip().replace("\n", " ")
    if len(stripped) <= limit:
        return stripped
    return stripped[:limit].rstrip() + "…"


def _parse_sections(markdown: str) -> List[Section]:
    lines = markdown.splitlines()
    sections: List[Section] = []
    current_title: str = ""
    current_level: int = 0
    current_content: List[str] = []

    def flush():
        if current_title or current_content:
            content_text = "\n".join(current_content).strip()
            sections.append(
                {
                    "level": current_level or 0,
                    "title": current_title or "",
                    "content": content_text,
                    "summary": _summarize(content_text or current_title),
                }
            )

    for line in lines:
        m = _HEADING_RE.match(line)
        if m:
            flush()
            current_level = len(m.group(1))
            current_title = m.group(2).strip()
            current_content = []
        else:
            current_content.append(line)
    flush()

    primary = [s for s in sections if s.get("level", 0) in (1, 2)]
    return primary if primary else sections


def load_rules(rules_dir: str) -> List[RuleDocument]:
    base = Path(rules_dir)
    if not base.exists() or not base.is_dir():
        raise FileNotFoundError(f"Rules directory not found: {rules_dir}")

    t0 = start_timer()
    log_json(logger, "rules.load.start", {"dir": str(base)})

    documents: List[RuleDocument] = []
    for md_file in sorted(base.glob("*.md")):
        raw = md_file.read_text(encoding="utf-8")
        sections = _parse_sections(raw)
        doc_title = next((s["title"] for s in sections if s.get("level") == 1 and s.get("title")), md_file.stem)
        documents.append(
            {
                "id": md_file.stem,
                "title": doc_title,
                "sections": sections,
                "raw_markdown": raw,
            }
        )
        log_json(
            logger,
            "rules.load.file",
            {"file": md_file.name, "sections": len(sections)},
        )

    log_json(
        logger,
        "rules.load.done",
        {"count": len(documents), "elapsed_ms": elapsed_ms(t0)},
    )
    return documents


if __name__ == "__main__":
    from pathlib import Path as _Path

    repo_root = _Path(__file__).resolve().parents[2]
    default_rules = repo_root / "docs/insurance_risk_factor_agent/demo_rules"
    docs = load_rules(str(default_rules))
    print(f"Loaded {len(docs)} rule documents from {default_rules}")
    for d in docs:
        print(f"- {d['id']}: {d['title']} (sections={len(d['sections'])})")
