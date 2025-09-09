from typing import Any, Dict, List, TypedDict


class AssessmentResult(TypedDict, total=False):
    product_code: str
    overall_risk_tier: str
    key_factors: List[str]
    driver_analysis: List[Dict[str, Any]]
    vehicle_analysis: List[Dict[str, Any]]
    policy_analysis: Dict[str, Any]
    reasoning_steps: List[Dict[str, Any]]
    confidence: float
