from pathlib import Path
import json

from src.utils.data_parser import parse_application
from src.agents.risk_factor_agent import assess


def test_agent_assess_dry_run():
    repo_root = Path(__file__).resolve().parents[1]
    demo_app = repo_root / "docs/insurance_risk_factor_agent/demo_application/user_appliction.json"
    raw = demo_app.read_text(encoding="utf-8")
    profile = parse_application(raw)

    result = assess(profile, product_code="Monthly-Comfort")
    assert result["product_code"] == "Monthly-Comfort"
    assert result["overall_risk_tier"] in {"LOW", "MEDIUM", "HIGH"}
    assert isinstance(result["key_factors"], list)
    assert isinstance(result["reasoning_steps"], list)
