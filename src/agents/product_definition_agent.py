"""
Product Definition Agent - Multi-Agent System

This agent is responsible for:
1. Defining required risk factors for products
2. Providing risk factor definitions <risk_subject, risk_factor_name>[]
3. Supplying assessment rules for each risk factor
4. Maintaining product-specific rule configurations
5. Defining how risk factors should be evaluated
"""

import logging
from typing import Any, Dict, List, Tuple, Optional
from dataclasses import dataclass

from src.utils.rule_loader import load_rules
from src.gateway.agent_factory import init_agent

logger = logging.getLogger(__name__)


@dataclass
class RiskFactorDefinition:
    """Definition of a risk factor for a product."""
    risk_subject: str  # e.g., "driver", "vehicle", "policy"
    risk_factor_name: str  # e.g., "three_year_claim_free_discount"
    description: str
    evaluation_rules: List[str]
    required: bool = True
    weight: float = 1.0


@dataclass
class ProductDefinition:
    """Complete product definition with risk factors and rules."""
    product_code: str
    product_name: str
    risk_factors: List[RiskFactorDefinition]
    assessment_rules: Dict[str, Any]
    coverage_options: Dict[str, Any]


class ProductDefinitionAgent:
    """
    Agent responsible for defining products, risk factors, and assessment rules.
    """
    
    def __init__(self, rules_dir: str = "docs/insurance_risk_factor_agent/3_year_claim_free_discount"):
        """Initialize the product definition agent."""
        self.agent = init_agent()
        self.rules_dir = rules_dir
        self.product_definitions: Dict[str, ProductDefinition] = {}
        self._load_product_definitions()
        
    def _load_product_definitions(self) -> None:
        """Load product definitions and rules."""
        try:
            # Load rules from the rules directory
            rules = load_rules(self.rules_dir)
            
            # Define the Monthly-Comfort product (demo product)
            comfort_product = ProductDefinition(
                product_code="Monthly-Comfort",
                product_name="Monthly Comfort Package",
                risk_factors=[
                    RiskFactorDefinition(
                        risk_subject="driver",
                        risk_factor_name="three_year_claim_free_discount",
                        description="Three-year claim-free driving discount assessment",
                        evaluation_rules=[rule["id"] for rule in rules],
                        required=True,
                        weight=1.0
                    ),
                    RiskFactorDefinition(
                        risk_subject="driver",
                        risk_factor_name="driving_record_classification",
                        description="Driver record classification based on violations and claims",
                        evaluation_rules=["D04_Driving_Record_Classification"],
                        required=True,
                        weight=1.2
                    ),
                    RiskFactorDefinition(
                        risk_subject="driver",
                        risk_factor_name="driver_classification",
                        description="Basic driver classification by age and experience",
                        evaluation_rules=["D03_Driver_Classification"],
                        required=True,
                        weight=0.8
                    )
                ],
                assessment_rules={rule["id"]: rule for rule in rules},
                coverage_options={
                    "liability_coverage": {"min": 25000, "max": 100000, "default": 50000},
                    "comprehensive": {"available": True, "deductible_options": [250, 500, 1000]},
                    "collision": {"available": True, "deductible_options": [250, 500, 1000]}
                }
            )
            
            self.product_definitions["Monthly-Comfort"] = comfort_product
            
            # Add other product definitions (placeholders for future expansion)
            self._add_economy_product()
            self._add_turbo_product()
            
            logger.info(f"Loaded {len(self.product_definitions)} product definitions")
            
        except Exception as e:
            logger.error(f"Failed to load product definitions: {e}")
            raise RuntimeError(f"ProductDefinitionLoadError: {e}") from e
            
    def _add_economy_product(self) -> None:
        """Add Monthly-Economy product definition (placeholder)."""
        economy_product = ProductDefinition(
            product_code="Monthly-Economy",
            product_name="Monthly Economy Package",
            risk_factors=[
                RiskFactorDefinition(
                    risk_subject="driver",
                    risk_factor_name="basic_driver_assessment",
                    description="Basic driver assessment for economy package",
                    evaluation_rules=["basic_rules"],
                    required=True,
                    weight=1.0
                )
            ],
            assessment_rules={},
            coverage_options={
                "liability_coverage": {"min": 15000, "max": 50000, "default": 25000}
            }
        )
        self.product_definitions["Monthly-Economy"] = economy_product
        
    def _add_turbo_product(self) -> None:
        """Add Monthly-Turbo product definition (placeholder)."""
        turbo_product = ProductDefinition(
            product_code="Monthly-Turbo",
            product_name="Monthly Turbo Package",
            risk_factors=[
                RiskFactorDefinition(
                    risk_subject="driver",
                    risk_factor_name="comprehensive_risk_assessment",
                    description="Comprehensive risk assessment for turbo package",
                    evaluation_rules=["comprehensive_rules"],
                    required=True,
                    weight=1.5
                )
            ],
            assessment_rules={},
            coverage_options={
                "liability_coverage": {"min": 50000, "max": 250000, "default": 100000},
                "comprehensive": {"available": True, "deductible_options": [100, 250, 500]},
                "collision": {"available": True, "deductible_options": [100, 250, 500]},
                "rental_car": {"available": True, "daily_limit": 50}
            }
        )
        self.product_definitions["Monthly-Turbo"] = turbo_product
        
    def get_product_definition(self, product_code: str) -> Optional[ProductDefinition]:
        """
        Get the complete product definition for a given product code.
        
        Args:
            product_code: The product code (e.g., "Monthly-Comfort")
            
        Returns:
            ProductDefinition if found, None otherwise
        """
        return self.product_definitions.get(product_code)
        
    def get_risk_factor_definitions(self, product_code: str) -> List[Tuple[str, str]]:
        """
        Get risk factor definitions as <risk_subject, risk_factor_name> pairs.
        
        Args:
            product_code: The product code
            
        Returns:
            List of (risk_subject, risk_factor_name) tuples
        """
        product = self.get_product_definition(product_code)
        if not product:
            logger.warning(f"Product definition not found: {product_code}")
            return []
            
        return [(rf.risk_subject, rf.risk_factor_name) for rf in product.risk_factors]
        
    def get_assessment_rules(self, product_code: str, risk_factor_name: Optional[str] = None) -> Dict[str, Any]:
        """
        Get assessment rules for a product and optionally a specific risk factor.
        
        Args:
            product_code: The product code
            risk_factor_name: Optional specific risk factor name
            
        Returns:
            Dictionary of assessment rules
        """
        product = self.get_product_definition(product_code)
        if not product:
            logger.warning(f"Product definition not found: {product_code}")
            return {}
            
        if risk_factor_name:
            # Filter rules for specific risk factor
            risk_factor = next(
                (rf for rf in product.risk_factors if rf.risk_factor_name == risk_factor_name),
                None
            )
            if risk_factor:
                return {
                    rule_id: product.assessment_rules[rule_id]
                    for rule_id in risk_factor.evaluation_rules
                    if rule_id in product.assessment_rules
                }
            return {}
        
        return product.assessment_rules
        
    def get_coverage_options(self, product_code: str) -> Dict[str, Any]:
        """
        Get coverage options for a product.
        
        Args:
            product_code: The product code
            
        Returns:
            Dictionary of coverage options
        """
        product = self.get_product_definition(product_code)
        if not product:
            logger.warning(f"Product definition not found: {product_code}")
            return {}
            
        return product.coverage_options
        
    def list_available_products(self) -> List[str]:
        """
        Get list of available product codes.
        
        Returns:
            List of available product codes
        """
        return list(self.product_definitions.keys())
        
    def validate_product_configuration(self, product_code: str) -> Dict[str, Any]:
        """
        Validate that a product configuration is complete and valid.
        
        Args:
            product_code: The product code to validate
            
        Returns:
            Validation result with status and issues
        """
        validation_result = {
            "product_code": product_code,
            "valid": False,
            "issues": [],
            "warnings": []
        }
        
        product = self.get_product_definition(product_code)
        if not product:
            validation_result["issues"].append(f"Product definition not found: {product_code}")
            return validation_result
            
        # Check if product has risk factors
        if not product.risk_factors:
            validation_result["issues"].append("No risk factors defined for product")
            
        # Check if all required risk factors have evaluation rules
        for risk_factor in product.risk_factors:
            if risk_factor.required and not risk_factor.evaluation_rules:
                validation_result["issues"].append(
                    f"Required risk factor '{risk_factor.risk_factor_name}' has no evaluation rules"
                )
                
        # Check if assessment rules exist for referenced rule IDs
        for risk_factor in product.risk_factors:
            for rule_id in risk_factor.evaluation_rules:
                if rule_id not in product.assessment_rules:
                    validation_result["warnings"].append(
                        f"Rule '{rule_id}' referenced but not found in assessment rules"
                    )
                    
        validation_result["valid"] = len(validation_result["issues"]) == 0
        
        logger.info(f"Product validation for {product_code}: {'valid' if validation_result['valid'] else 'invalid'}")
        return validation_result
