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
    - Input: raw_json (str) with insurance application data containing policy, driver, and vehicle risk subjects
    - Output: RiskProfile standardized object with policy, drivers, and vehicles risk subjects
    - Errors: ValueError(格式错误), ValidationError(结构/必填项), returns with issues list.
    """
    issues: List[str] = []

    try:
        parsed = json.loads(raw_json)
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON: {e}") from e

    # Handle different input formats:
    # 1) Direct riskProfile object
    # 2) Array of riskProfile objects (use first)
    # 3) Nested session.data structure
    data = _extract_risk_profile_data(parsed)
    
    # Extract Policy Risk Subject
    policy = _extract_policy_risk_subject(data, issues)
    
    # Extract Driver Risk Subjects
    drivers = _extract_driver_risk_subjects(data, issues)
    
    # Extract Vehicle Risk Subjects  
    vehicles = _extract_vehicle_risk_subjects(data, issues)

    profile: RiskProfile = {
        "policy": policy,
        "drivers": drivers,
        "vehicles": vehicles,
        "issues": issues,
    }
    return profile


def _extract_risk_profile_data(parsed: Any) -> Dict[str, Any]:
    """Extract risk profile data from various input formats."""
    if isinstance(parsed, list) and parsed:
        # Array format - use first element
        data = parsed[0]
    elif isinstance(parsed, dict):
        data = parsed['session']['data']
    else:
        return {}
    
    # Check for nested session.data structure
    if "session" in data and "data" in data["session"]:
        return data["session"]["data"]
    
    # Check for direct riskProfile structure
    if "riskProfile" in data:
        return data["riskProfile"]
    
    return data


def _extract_policy_risk_subject(data: Dict[str, Any], issues: List[str]) -> Dict[str, Any]:
    """Extract policy-level risk subject information."""
    policy = _safe_dict(data.get("policy"))
    
    if not policy:
        # Try to extract from household riskAttributeValues if available
        household = _safe_dict(data.get("household"))
        if household and "riskAttributeValues" in household:
            policy = _safe_dict(household["riskAttributeValues"])
        
        if not policy:
            issues.append("Missing or invalid 'policy' risk subject, defaulting to {}")
    
    return policy


def _extract_driver_risk_subjects(data: Dict[str, Any], issues: List[str]) -> List[Dict[str, Any]]:
    """Extract driver-level risk subjects."""
    drivers = _safe_list(data.get('policy').get('line').get("drivers"))
    
    if not drivers:
        issues.append("Missing or invalid 'drivers' risk subjects, defaulting to []")
    
    # Validate each driver has required risk attributes
    validated_drivers = []
    for i, driver in enumerate(drivers):
        if not isinstance(driver, dict):
            issues.append(f"Driver {i} is not a valid object")
            continue
            
        # Extract risk attributes from driver
        risk_attrs = _safe_dict(driver.get("riskAttributeValues", {}))
        if not risk_attrs:
            issues.append(f"Driver {i} missing riskAttributeValues")
        
        validated_driver = {
            "id": driver.get("id", f"driver_{i}"),
            "type": driver.get("type", "driver"),
            "riskAttributeValues": risk_attrs
        }
        validated_drivers.append(validated_driver)
    
    return validated_drivers


def _extract_vehicle_risk_subjects(data: Dict[str, Any], issues: List[str]) -> List[Dict[str, Any]]:
    """Extract vehicle-level risk subjects."""
    vehicles = _safe_list(data.get('policy').get('line').get("risk")[0].get("vehicles"))
    
    if not vehicles:
        issues.append("Missing or invalid 'vehicles' risk subjects, defaulting to []")
    
    # Validate each vehicle has required risk attributes
    validated_vehicles = []
    for i, vehicle in enumerate(vehicles):
        if not isinstance(vehicle, dict):
            issues.append(f"Vehicle {i} is not a valid object")
            continue
            
        # Extract risk attributes from vehicle
        risk_attrs = _safe_dict(vehicle.get("riskAttributeValues", {}))
        if not risk_attrs:
            issues.append(f"Vehicle {i} missing riskAttributeValues")
        
        validated_vehicle = {
            "id": vehicle.get("id", f"vehicle_{i}"),
            "type": vehicle.get("type", "vehicle"),
            "riskAttributeValues": risk_attrs
        }
        validated_vehicles.append(validated_vehicle)
    
    return validated_vehicles
