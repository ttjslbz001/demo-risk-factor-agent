from pathlib import Path

from src.utils.rule_loader import load_rules


def test_load_demo_rules():
    repo_root = Path(__file__).resolve().parents[1]
    rules_dir = repo_root / "docs/insurance_risk_factor_agent/demo_rules"
    docs = load_rules(str(rules_dir))
    assert len(docs) >= 1
    for d in docs:
        assert "id" in d and d["id"]
        assert "title" in d and d["title"]
        assert isinstance(d["sections"], list)
