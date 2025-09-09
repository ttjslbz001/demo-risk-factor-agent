from pathlib import Path
import json
import pytest

from src.utils.data_parser import parse_application


def test_parse_valid_demo_application():
    repo_root = Path(__file__).resolve().parents[1]
    demo_app = repo_root / "docs/insurance_risk_factor_agent/demo_application/user_appliction.json"
    raw = demo_app.read_text(encoding="utf-8")
    profile = parse_application(raw)
    assert isinstance(profile, dict)
    assert "household" in profile
    assert "drivers" in profile and isinstance(profile["drivers"], list)
    assert "vehicles" in profile and isinstance(profile["vehicles"], list)
    assert "issues" in profile and isinstance(profile["issues"], list)


def test_parse_invalid_json_raises_value_error():
    with pytest.raises(ValueError):
        parse_application("{invalid}")


def test_missing_sections_collect_issues():
    raw = json.dumps({})
    profile = parse_application(raw)
    assert len(profile["issues"]) >= 1
