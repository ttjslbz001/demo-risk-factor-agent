"""
Data Lookup Agent - Multi-Agent System

This agent is responsible for:
1. Providing mapping values during risk calculation
2. Mapping risk tiers to specific values
3. Providing coverage values for premium calculation
4. Maintaining lookup tables and mappings
"""

import logging
from typing import Any, Dict, List, Optional, Union
from dataclasses import dataclass
from enum import Enum

from src.gateway.agent_factory import init_agent

logger = logging.getLogger(__name__)


class RiskTier(Enum):
    """Risk tier enumeration."""
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    VERY_HIGH = "VERY_HIGH"


@dataclass
class LookupMapping:
    """Represents a lookup mapping entry."""
    key: str
    value: Any
    description: str
    category: str


class DataLookupAgent:
    """
    Agent responsible for providing lookup tables and mapping values
    for risk calculations and premium computations.
    """
    
    def __init__(self):
        """Initialize the data lookup agent."""
        self.agent = init_agent()
        self.lookup_tables: Dict[str, Dict[str, Any]] = {}
        self._initialize_lookup_tables()
        
    def _initialize_lookup_tables(self) -> None:
        """Initialize all lookup tables with default values."""
        try:
            # Risk tier to multiplier mappings
            self.lookup_tables["risk_tier_multipliers"] = {
                "LOW": 0.8,
                "MEDIUM": 1.0,
                "HIGH": 1.3,
                "VERY_HIGH": 1.6
            }
            
            # Three-year claim-free discount mappings
            self.lookup_tables["claim_free_discount"] = {
                "0_years": {"discount": 0.0, "tier": "HIGH"},
                "1_year": {"discount": 0.05, "tier": "MEDIUM"},
                "2_years": {"discount": 0.10, "tier": "MEDIUM"},
                "3_years": {"discount": 0.15, "tier": "LOW"},
                "4_years": {"discount": 0.18, "tier": "LOW"},
                "5_plus_years": {"discount": 0.20, "tier": "LOW"}
            }
            
            # Driver classification mappings
            self.lookup_tables["driver_classification"] = {
                "young_inexperienced": {"base_rate": 1.5, "tier": "HIGH"},
                "young_experienced": {"base_rate": 1.2, "tier": "MEDIUM"},
                "adult_inexperienced": {"base_rate": 1.1, "tier": "MEDIUM"},
                "adult_experienced": {"base_rate": 1.0, "tier": "LOW"},
                "senior_experienced": {"base_rate": 1.1, "tier": "MEDIUM"},
                "senior_inexperienced": {"base_rate": 1.3, "tier": "HIGH"}
            }
            
            # Driving record classification mappings
            self.lookup_tables["driving_record"] = {
                "clean": {"multiplier": 0.9, "tier": "LOW"},
                "minor_violations": {"multiplier": 1.1, "tier": "MEDIUM"},
                "major_violations": {"multiplier": 1.4, "tier": "HIGH"},
                "multiple_violations": {"multiplier": 1.7, "tier": "VERY_HIGH"},
                "recent_claims": {"multiplier": 1.3, "tier": "HIGH"},
                "multiple_claims": {"multiplier": 1.8, "tier": "VERY_HIGH"}
            }
            
            # Coverage value mappings by product
            self.lookup_tables["coverage_values"] = {
                "Monthly-Economy": {
                    "liability": {"base": 25000, "premium_factor": 0.8},
                    "comprehensive": {"base": 15000, "premium_factor": 0.7},
                    "collision": {"base": 15000, "premium_factor": 0.7}
                },
                "Monthly-Comfort": {
                    "liability": {"base": 50000, "premium_factor": 1.0},
                    "comprehensive": {"base": 30000, "premium_factor": 1.0},
                    "collision": {"base": 30000, "premium_factor": 1.0},
                    "rental_car": {"base": 1500, "premium_factor": 0.1}
                },
                "Monthly-Turbo": {
                    "liability": {"base": 100000, "premium_factor": 1.3},
                    "comprehensive": {"base": 75000, "premium_factor": 1.3},
                    "collision": {"base": 75000, "premium_factor": 1.3},
                    "rental_car": {"base": 3000, "premium_factor": 0.15},
                    "roadside_assistance": {"base": 500, "premium_factor": 0.05}
                }
            }
            
            # Base premium rates by product
            self.lookup_tables["base_premiums"] = {
                "Monthly-Economy": 120.0,
                "Monthly-Comfort": 180.0,
                "Monthly-Turbo": 280.0
            }
            
            # Vehicle type multipliers
            self.lookup_tables["vehicle_type_multipliers"] = {
                "sedan": 1.0,
                "suv": 1.1,
                "truck": 1.2,
                "sports_car": 1.5,
                "luxury": 1.3,
                "hybrid": 0.95,
                "electric": 0.9
            }
            
            # Age group multipliers
            self.lookup_tables["age_multipliers"] = {
                "16-20": 1.8,
                "21-25": 1.4,
                "26-35": 1.0,
                "36-50": 0.9,
                "51-65": 0.95,
                "65+": 1.1
            }
            
            logger.info(f"Initialized {len(self.lookup_tables)} lookup tables")
            
        except Exception as e:
            logger.error(f"Failed to initialize lookup tables: {e}")
            raise RuntimeError(f"LookupTableInitializationError: {e}") from e
            
    def lookup_risk_tier_multiplier(self, risk_tier: Union[str, RiskTier]) -> float:
        """
        Get the multiplier value for a given risk tier.
        
        Args:
            risk_tier: The risk tier (string or enum)
            
        Returns:
            Multiplier value for the risk tier
        """
        if isinstance(risk_tier, RiskTier):
            risk_tier = risk_tier.value
            
        multiplier = self.lookup_tables["risk_tier_multipliers"].get(risk_tier, 1.0)
        logger.debug(f"Risk tier {risk_tier} -> multiplier {multiplier}")
        return multiplier
        
    def lookup_claim_free_discount(self, years_claim_free: int) -> Dict[str, Any]:
        """
        Get claim-free discount information based on years without claims.
        
        Args:
            years_claim_free: Number of years without claims
            
        Returns:
            Dictionary with discount rate and risk tier
        """
        if years_claim_free >= 5:
            key = "5_plus_years"
        elif years_claim_free >= 3:
            key = f"{years_claim_free}_years"
        elif years_claim_free in [1, 2]:
            key = f"{years_claim_free}_year{'s' if years_claim_free > 1 else ''}"
        else:
            key = "0_years"
            
        result = self.lookup_tables["claim_free_discount"].get(key, {"discount": 0.0, "tier": "HIGH"})
        logger.debug(f"Claim-free years {years_claim_free} -> {result}")
        return result
        
    def lookup_driver_classification(self, classification: str) -> Dict[str, Any]:
        """
        Get driver classification information.
        
        Args:
            classification: Driver classification key
            
        Returns:
            Dictionary with base rate and risk tier
        """
        result = self.lookup_tables["driver_classification"].get(
            classification, 
            {"base_rate": 1.0, "tier": "MEDIUM"}
        )
        logger.debug(f"Driver classification {classification} -> {result}")
        return result
        
    def lookup_driving_record(self, record_type: str) -> Dict[str, Any]:
        """
        Get driving record multiplier and tier.
        
        Args:
            record_type: Type of driving record
            
        Returns:
            Dictionary with multiplier and risk tier
        """
        result = self.lookup_tables["driving_record"].get(
            record_type,
            {"multiplier": 1.0, "tier": "MEDIUM"}
        )
        logger.debug(f"Driving record {record_type} -> {result}")
        return result
        
    def lookup_coverage_values(self, product_code: str) -> Dict[str, Any]:
        """
        Get coverage values for premium calculation.
        
        Args:
            product_code: Product code (e.g., "Monthly-Comfort")
            
        Returns:
            Dictionary of coverage values and premium factors
        """
        coverage_values = self.lookup_tables["coverage_values"].get(product_code, {})
        logger.debug(f"Coverage values for {product_code}: {list(coverage_values.keys())}")
        return coverage_values
        
    def lookup_base_premium(self, product_code: str) -> float:
        """
        Get base premium for a product.
        
        Args:
            product_code: Product code
            
        Returns:
            Base premium amount
        """
        base_premium = self.lookup_tables["base_premiums"].get(product_code, 150.0)
        logger.debug(f"Base premium for {product_code}: {base_premium}")
        return base_premium
        
    def lookup_vehicle_multiplier(self, vehicle_type: str) -> float:
        """
        Get vehicle type multiplier.
        
        Args:
            vehicle_type: Type of vehicle
            
        Returns:
            Vehicle type multiplier
        """
        multiplier = self.lookup_tables["vehicle_type_multipliers"].get(vehicle_type.lower(), 1.0)
        logger.debug(f"Vehicle type {vehicle_type} -> multiplier {multiplier}")
        return multiplier
        
    def lookup_age_multiplier(self, age: int) -> float:
        """
        Get age-based multiplier.
        
        Args:
            age: Driver age
            
        Returns:
            Age-based multiplier
        """
        if age <= 20:
            age_group = "16-20"
        elif age <= 25:
            age_group = "21-25"
        elif age <= 35:
            age_group = "26-35"
        elif age <= 50:
            age_group = "36-50"
        elif age <= 65:
            age_group = "51-65"
        else:
            age_group = "65+"
            
        multiplier = self.lookup_tables["age_multipliers"].get(age_group, 1.0)
        logger.debug(f"Age {age} ({age_group}) -> multiplier {multiplier}")
        return multiplier
        
    def get_all_mappings(self, category: Optional[str] = None) -> Dict[str, Any]:
        """
        Get all lookup mappings, optionally filtered by category.
        
        Args:
            category: Optional category filter
            
        Returns:
            Dictionary of all or filtered mappings
        """
        if category:
            return self.lookup_tables.get(category, {})
        return self.lookup_tables.copy()
        
    def add_custom_mapping(self, category: str, key: str, value: Any, description: str = "") -> None:
        """
        Add a custom mapping to the lookup tables.
        
        Args:
            category: Category of the mapping
            key: Mapping key
            value: Mapping value
            description: Optional description
        """
        if category not in self.lookup_tables:
            self.lookup_tables[category] = {}
            
        self.lookup_tables[category][key] = value
        logger.info(f"Added custom mapping: {category}.{key} = {value}")
        
    def validate_lookup_tables(self) -> Dict[str, Any]:
        """
        Validate the integrity of lookup tables.
        
        Returns:
            Validation result with status and issues
        """
        validation_result = {
            "valid": True,
            "issues": [],
            "warnings": [],
            "table_count": len(self.lookup_tables),
            "total_entries": sum(len(table) for table in self.lookup_tables.values())
        }
        
        # Check for empty tables
        for table_name, table_data in self.lookup_tables.items():
            if not table_data:
                validation_result["warnings"].append(f"Empty lookup table: {table_name}")
                
        # Check for required tables
        required_tables = ["risk_tier_multipliers", "base_premiums", "coverage_values"]
        for required_table in required_tables:
            if required_table not in self.lookup_tables:
                validation_result["issues"].append(f"Missing required table: {required_table}")
                
        validation_result["valid"] = len(validation_result["issues"]) == 0
        
        logger.info(f"Lookup table validation: {'valid' if validation_result['valid'] else 'invalid'}")
        return validation_result
