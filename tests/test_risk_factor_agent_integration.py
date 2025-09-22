import json
from pathlib import Path

import pytest

from src.utils.data_parser import parse_application
from src.agents.risk_factor_agent import assess


def _load_demo_profile() -> dict:
    repo_root = Path(__file__).resolve().parents[1]
    demo_app = repo_root / "docs/insurance_risk_factor_agent/demo_application/user_appliction.json"
    raw = demo_app.read_text(encoding="utf-8")
    return parse_application(raw)


def test_assess_integration_smoke():
    profile = _load_demo_profile()
    result = assess(profile, product_code="Monthly-Comfort")

    assert isinstance(result, dict)

    # Top-level fields from reasoning normalization
    assert "final_assessment" in result
    assert "steps" in result
    assert "confidence" in result

    # Added by risk_factor_agent wrapper
    assert result.get("risk_factor") == "3 year claim free discount"

    # Validate normalized structure values
    tier = result["final_assessment"].get("overall_risk_tier")
    assert tier in {"LOW", "MEDIUM", "HIGH"}

    assert isinstance(result["final_assessment"].get("key_factors", []), list)
    assert isinstance(result["steps"], list)
    assert isinstance(result["confidence"], (int, float))


@pytest.mark.parametrize("product_code", ["Monthly-Economy", "Monthly-Comfort", "Monthly-Turbo"])
def test_assess_multiple_product_codes(product_code: str):
    profile = _load_demo_profile()
    result = assess(profile, product_code=product_code)

    assert result["final_assessment"]["overall_risk_tier"] in {"LOW", "MEDIUM", "HIGH"}
    assert isinstance(result["steps"], list)
    assert result.get("risk_factor") == "3 year claim free discount"
