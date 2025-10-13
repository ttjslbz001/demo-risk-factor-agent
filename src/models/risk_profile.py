from typing import Any, Dict, List, TypedDict


class RiskProfile(TypedDict, total=False):
    # Policy-level risk subject
    policy: Dict[str, Any]
    # Driver-level risk subjects
    drivers: List[Dict[str, Any]]
    # Vehicle-level risk subjects  
    vehicles: List[Dict[str, Any]]
    # Parsing issues and validation errors
    issues: List[str]
