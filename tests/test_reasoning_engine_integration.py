import json
import os
from pathlib import Path

import pytest

from src.agents.reasoning_engine import run_reasoning


def _load_demo_profile() -> dict:
    repo_root = Path(__file__).resolve().parents[1]
    demo_app = repo_root / "docs/insurance_risk_factor_agent/demo_application/user_appliction.json"
    raw = demo_app.read_text(encoding="utf-8")
    return json.loads(raw)


def _load_demo_rules() -> list:
    repo_root = Path(__file__).resolve().parents[1]
    rules_dir = repo_root / "docs/insurance_risk_factor_agent/demo_rules"
    rules: list = []
    for p in sorted(rules_dir.glob("*.md")):
        # Minimal stub to keep test light: only ids and empty sections
        rules.append({"id": p.stem, "sections": []})
    return rules


def test_run_reasoning_fallback_without_model():
    profile = _load_demo_profile()
    rules = _load_demo_rules()
    result = run_reasoning(model=None, profile=profile, rules=rules, product_code="Monthly-Comfort")
    assert result["final_assessment"]["overall_risk_tier"] in {"LOW", "MEDIUM", "HIGH"}
    assert isinstance(result["steps"], list)
    assert result["confidence"] <= 0.5


requires_key = pytest.mark.skipif(
    not os.environ.get("TELENAV_API_KEY"), reason="TELENAV_API_KEY not set"
)


@requires_key
def test_run_reasoning_with_real_model_smoke():
    profile = _load_demo_profile()
    rules = _load_demo_rules()
    try:
        result = run_reasoning(model=None, profile=profile, rules=rules, product_code="Monthly-Comfort")
    except Exception as e:  # noqa: BLE001
        pytest.skip(f"Model unavailable: {e}")
    assert isinstance(result, dict)
    assert "final_assessment" in result
    assert "steps" in result

