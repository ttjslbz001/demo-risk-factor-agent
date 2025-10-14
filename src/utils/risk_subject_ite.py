from enum import Enum
from typing import Dict, Any, List
from dataclasses import dataclass
import json
import os

class RiskSubjectType(Enum):
    HOUSEHOLD = "household"
    DRIVER = "driver"
    VEHICLE = "vehicle"
    
class RiskSubject(Enum):
    risk_subject_type: RiskSubjectType
    risk_subject_id: str
    risk_subject_value: Dict[str, Any]
    
@dataclass
class RiskCalculationTable:
    risk_subject: Any
    risk_dimension: str
    risk_subject_type: RiskSubjectType
    context: Any
    
    
AZ_HARDCODE_RISK_SUBJECT_MAP = {
  "acq-exp-factor-ae1-risk-factor": "vehicle",
  "acq-exp-factor-ae2-risk-factor": "vehicle",
  "advance-quote-risk-factor": "vehicle",
  "annual-miles-risk-factor": "vehicle",
  "aux-symbol-risk-factor": "vehicle",
  "average-by-number-of-vehicles-risk-factor": "vehicle",
  "bad-debt-fr-risk-factor": "vehicle",
  "base-rates-risk-rate": "vehicle",
  "business-use-surcharge-risk-factor": "vehicle",
  "cont-ins-disc-risk-factor": "vehicle",
  "coverage-selection-coll-risk-factor": "vehicle",
  "coverage-selection-comp-risk-factor": "vehicle",
  "driver-age-risk-factor-bi-pd": "driver",
  "driver-age-risk-factor-coll": "driver",
  "driver-age-risk-factor-comp": "driver",
  "driver-age-risk-factor-med": "driver",
  "driver-class-risk-factor": "driver",
  "driver-license-type-risk-factor": "driver",
  "driver-training-disc-risk-factor": "driver",
  "driving-record-points-risk-point-bi-pd": "driver",
  "driving-record-points-risk-point-coll": "driver",
  "driving-record-points-risk-point-comp": "driver",
  "driving-record-points-risk-point-med": "driver",
  "excess-veh-risk-factor": "vehicle",
  "financial-resp-by-clean-risk-factor": "driver",
  "financial-resp-by-num-of-drivers-risk-factor": "vehicle",
  "financial-resp-filing-surcharge-risk-factor": "vehicle",
  "fr-tier-risk-factor": "vehicle",
  "full-cov-risk-factor": "vehicle",
  "garaging-location-risk-factor": "vehicle",
  "hh-member-risk-factor": "driver",
  "hh-structure-risk-factor": "vehicle",
  "home-mh-mc-disc-risk-factor": "vehicle",
  "late-renewal-risk-factor": "vehicle",
  "length-of-veh-ownership-risk-factor": "vehicle",
  "limit-and-ded-risk-factor-acpe": "vehicle",
  "limit-and-ded-risk-factor-bi": "vehicle",
  "limit-and-ded-risk-factor-coll": "vehicle",
  "limit-and-ded-risk-factor-comp": "vehicle",
  "limit-and-ded-risk-factor-loan": "vehicle",
  "limit-and-ded-risk-factor-med": "vehicle",
  "limit-and-ded-risk-factor-pd": "vehicle",
  "limit-and-ded-risk-factor-rent": "vehicle",
  "limit-and-ded-risk-factor-uim": "vehicle",
  "limit-and-ded-risk-factor-um": "vehicle",
  "luxury-veh-risk-factor": "vehicle",
  "minimum-premium-mapping-household": "household",
  "monthly-rate-risk-factor": "vehicle",
  "nb-five-yr-acc-free-claim-free-disc-risk-factor": "vehicle",
  "nb-nsp-disc-risk-factor": "vehicle",
  "new-business-rate-revision-effective-date-mapping-household": "household",
  "nsp-not-currently-monitoring-duration-mapping-vehicle": "vehicle",
  "nsp-safety-score-risk-factor": "vehicle",
  "occupation-education-risk-factor": "vehicle",
  "opex1-risk-factor": "vehicle",
  "opex2-risk-factor": "vehicle",
  "opex3-risk-factor": "vehicle",
  "opex5-risk-factor": "vehicle",
  "opex6-risk-factor": "vehicle",
  "opex8-risk-factor": "vehicle",
  "policy-term-risk-factor": "vehicle",
  "risk-group-code-risk-factor": "vehicle",
  "subtraction-of-unity-risk-point": "driver",
  "three-year-safe-dr-disc-risk-factor": "vehicle",
  "underwriting-tier-mapping-household": "household",
  "uw-tier-percent-risk-factor": "vehicle",
  "valid-garaging-zip-code-mapping-vehicle": "vehicle",
  "veh-symbol-risk-factor": "vehicle",
  "vehicle-age-coverage-risk-factor": "vehicle",
  "vehicle-age-risk-factor": "vehicle",
  "vehicle-attributes-rating-risk-factor": "vehicle",
  "vehicle-history-rating-risk-factor": "vehicle",
  "years-licensed-risk-factor": "driver",
  "youthful-driver-disc-risk-factor": "driver"
}
    
    

def risk_subject_iter(risk_subject_mapping: Dict[str, List[str]]) -> Dict[str, Any]:
    """
    Iterate over the risk subjects in the profile.
    Categorizes risk factors into 'driver' and 'vehicle' based on AZ_HARDCODE_RISK_SUBJECT_MAP.
    
    Args:
        profile: The profile data containing risk factors
        risk_subject_mapping: Mapping of risk subjects to their identifiers
        
    Returns:
        Dictionary with 'driver' and 'vehicle' keys containing their respective risk factors
    """
    result = {
        'driver': [],
        'vehicle': []
    }
    
    # Iterate over all risk factors in the hardcoded map
    for risk_factor_name, subject_type in risk_subject_mapping.items():
        # If risk factor is household or driver, add to result['driver']
        if subject_type in ['household', 'driver']:
            result['driver'].append({
                'risk_dimension_name': risk_factor_name,
                'subject_type': subject_type
            })
        # Otherwise (vehicle), add to result['vehicle']
        else:
            result['vehicle'].append({
                'risk_dimension_name': risk_factor_name,
                'subject_type': subject_type
            })
    
    return result


def prepare_risk_calculation_tables(application: Any, ris_dimension: Dict[str, Any]) -> List[RiskCalculationTable]:
    # Process driver risk dimensions
    risk_calculation_tables: List[RiskCalculationTable] = []
    print(f"\n📊 Processing driver risk dimensions...")
    for risk_dimension in ris_dimension['driver']:
        risk_dimension_name = risk_dimension['risk_dimension_name']
        drivers = application['riskProfile']['drivers']
        for driver in drivers:
            risk_calculation_tables.append(
                RiskCalculationTable(
                    risk_subject=driver,
                    risk_dimension=risk_dimension_name,
                    risk_subject_type=RiskSubjectType.DRIVER,
                    context=application['riskProfile']
                )
            )
    
    # Process vehicle risk dimensions
    print(f"📊 Processing vehicle risk dimensions...")
    for risk_dimension in ris_dimension['vehicle']:
        risk_dimension_name = risk_dimension['risk_dimension_name']
        vehicles = application['riskProfile']['vehicles']
        for vehicle in vehicles:
            risk_calculation_tables.append(
                RiskCalculationTable(
                    risk_subject=vehicle,
                    risk_dimension=risk_dimension_name,
                    risk_subject_type=RiskSubjectType.VEHICLE,
                    context=application['riskProfile']
                )
            )
    return risk_calculation_tables


if __name__ == "__main__":
    # Load application data from economy.json
    json_path = os.path.join(os.path.dirname(__file__), '../../docs/insurance_risk_factor_agent/demo_application/economy.json')
    
    print(f"Loading application data from: {json_path}")
    with open(json_path, 'r') as f:
        application = json.load(f)
    
    print(f"✅ Application loaded successfully")
    print(f"   Drivers: {len(application.get('riskProfile', {}).get('drivers', []))}")
    print(f"   Vehicles: {len(application.get('riskProfile', {}).get('vehicles', []))}")
    
    # Get risk dimensions
    ris_dimension = risk_subject_iter(AZ_HARDCODE_RISK_SUBJECT_MAP)
    risk_calculation_tables: List[RiskCalculationTable] = prepare_risk_calculation_tables(application, ris_dimension)
    
    print(f"\n✅ Total risk calculation tables created: {len(risk_calculation_tables)}")
    
    # Calculate breakdown
    driver_tables = sum(1 for t in risk_calculation_tables if t.risk_subject_type == RiskSubjectType.DRIVER)
    vehicle_tables = sum(1 for t in risk_calculation_tables if t.risk_subject_type == RiskSubjectType.VEHICLE)
    
    print(f"\n📈 Breakdown:")
    print(f"   Driver tables: {driver_tables} ({len(ris_dimension['driver'])} dimensions × {len(application['riskProfile']['drivers'])} drivers)")
    print(f"   Vehicle tables: {vehicle_tables} ({len(ris_dimension['vehicle'])} dimensions × {len(application['riskProfile']['vehicles'])} vehicles)")
    
    # Show a few examples
    print(f"\n📋 Sample risk calculation tables:")
    for i, table in enumerate(risk_calculation_tables[250:], 1):
        print(f"\n   {i}. Type: {table.risk_subject_type.value}")
        print(f"      Dimension: {table.risk_dimension}")
        if table.risk_subject_type == RiskSubjectType.DRIVER:
            driver_id =  table.risk_subject.get('id', '')
            print(f"      Driver: {driver_id.strip()}")
        else:
            vin = table.risk_subject.get('id', '')
            print(f"      Vehicle: {vin.strip()} ")
    
    if len(risk_calculation_tables) > 3:
        print(f"\n   ... and {len(risk_calculation_tables) - 3} more tables")