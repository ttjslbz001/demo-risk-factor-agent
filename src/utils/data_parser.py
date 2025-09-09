import json
from typing import Any, Dict, List

from src.models.risk_profile import RiskProfile


def _safe_dict(value: Any) -> Dict[str, Any]:
    return value if isinstance(value, dict) else {}


def _safe_list(value: Any) -> List[Dict[str, Any]]:
    if isinstance(value, list):
        return [v if isinstance(v, dict) else {} for v in value]
    return []


def parse_application(raw_json: str) -> RiskProfile:
    """
    Contract:
    - Input: raw_json (str) 与示例结构一致，含 household/drivers/vehicles.
    - Output: RiskProfile 标准化对象；字段缺失需提供安全默认与校验错误集合。
    - Errors: ValueError(格式错误), ValidationError(结构/必填项), returns with issues list.
    """
    issues: List[str] = []

    try:
        parsed = json.loads(raw_json)
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON: {e}") from e

    # Accept three shapes:
    # 1) Dict with household/drivers/vehicles at top-level
    # 2) Dict with 'riskProfile' containing those keys
    # 3) List of such dicts (use the first element)
    if isinstance(parsed, list):
        data = parsed[0] if parsed else {}
    elif isinstance(parsed, dict):
        data = parsed
    else:
        data = {}

    root = data.get("riskProfile") if isinstance(data, dict) else None
    container = root if isinstance(root, dict) else data if isinstance(data, dict) else {}

    # Household
    household = _safe_dict(container.get("household"))
    if not household:
        issues.append("Missing or invalid 'household', defaulting to {}")

    # Drivers
    drivers = _safe_list(container.get("drivers"))
    if not drivers:
        issues.append("Missing or invalid 'drivers', defaulting to []")

    # Vehicles
    vehicles = _safe_list(container.get("vehicles"))
    if not vehicles:
        issues.append("Missing or invalid 'vehicles', defaulting to []")

    profile: RiskProfile = {
        "household": household,
        "drivers": drivers,
        "vehicles": vehicles,
        "issues": issues,
    }
    return profile
