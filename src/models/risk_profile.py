from typing import Any, Dict, List, TypedDict


class RiskProfile(TypedDict, total=False):
    household: Dict[str, Any]
    drivers: List[Dict[str, Any]]
    vehicles: List[Dict[str, Any]]
    issues: List[str]
