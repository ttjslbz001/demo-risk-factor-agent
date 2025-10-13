"""
Premium Calculation Agent - Multi-Agent System

This agent is responsible for:
1. Applying premium calculation formulas
2. Processing risk factors and coverage values
3. Calculating final premium amount
4. Validating calculation results
"""

import logging
from typing import Any, Dict, List, Optional
from dataclasses import dataclass
from decimal import Decimal, ROUND_HALF_UP

from src.gateway.agent_factory import init_agent

logger = logging.getLogger(__name__)


@dataclass
class PremiumComponent:
    """Represents a component of the premium calculation."""
    name: str
    base_amount: float
    multiplier: float
    final_amount: float
    description: str


@dataclass
class PremiumCalculationResult:
    """Result of premium calculation with breakdown."""
    base_premium: float
    total_premium: float
    components: List[PremiumComponent]
    discounts: List[PremiumComponent]
    risk_multiplier: float
    calculation_details: Dict[str, Any]
    validation_status: str


class PremiumCalculationAgent:
    """
    Agent responsible for calculating insurance premiums based on
    risk factors, coverage values, and product configurations.
    """
    
    def __init__(self):
        """Initialize the premium calculation agent."""
        self.agent = init_agent()
        self.calculation_history: List[PremiumCalculationResult] = []
        
    def calculate_premium(
        self,
        base_premium: float,
        risk_factors: Dict[str, Any],
        coverage_values: Dict[str, Any],
        product_code: str
    ) -> PremiumCalculationResult:
        """
        Calculate the final premium based on risk factors and coverage values.
        
        Args:
            base_premium: Base premium amount for the product
            risk_factors: Dictionary of risk factor values and tiers
            coverage_values: Dictionary of coverage values and factors
            product_code: Product code for calculation context
            
        Returns:
            PremiumCalculationResult with detailed breakdown
        """
        try:
            logger.info(f"Starting premium calculation for {product_code}")
            
            # Initialize calculation components
            components = []
            discounts = []
            total_multiplier = 1.0
            
            # Process base premium
            components.append(PremiumComponent(
                name="Base Premium",
                base_amount=base_premium,
                multiplier=1.0,
                final_amount=base_premium,
                description=f"Base premium for {product_code}"
            ))
            
            # Process risk factors
            risk_multiplier = self._calculate_risk_multiplier(risk_factors)
            total_multiplier *= risk_multiplier
            
            # Process coverage adjustments
            coverage_multiplier = self._calculate_coverage_multiplier(coverage_values)
            total_multiplier *= coverage_multiplier
            
            # Apply discounts
            discount_amount = self._calculate_discounts(base_premium, risk_factors, discounts)
            
            # Calculate final premium
            adjusted_premium = base_premium * total_multiplier
            final_premium = max(adjusted_premium - discount_amount, base_premium * 0.5)  # Minimum 50% of base
            
            # Round to 2 decimal places
            final_premium = float(Decimal(str(final_premium)).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP))
            
            # Create detailed calculation result
            calculation_details = {
                "base_premium": base_premium,
                "risk_multiplier": risk_multiplier,
                "coverage_multiplier": coverage_multiplier,
                "total_multiplier": total_multiplier,
                "discount_amount": discount_amount,
                "adjusted_premium": adjusted_premium,
                "minimum_premium": base_premium * 0.5
            }
            
            result = PremiumCalculationResult(
                base_premium=base_premium,
                total_premium=final_premium,
                components=components,
                discounts=discounts,
                risk_multiplier=risk_multiplier,
                calculation_details=calculation_details,
                validation_status="valid"
            )
            
            # Validate the calculation
            validation_result = self._validate_calculation(result)
            result.validation_status = validation_result["status"]
            
            # Store in history
            self.calculation_history.append(result)
            
            logger.info(f"Premium calculation completed: {final_premium}")
            return result
            
        except Exception as e:
            logger.error(f"Premium calculation failed: {e}")
            raise RuntimeError(f"PremiumCalculationError: {e}") from e
            
    def _calculate_risk_multiplier(self, risk_factors: Dict[str, Any]) -> float:
        """
        Calculate the overall risk multiplier from individual risk factors.
        
        Args:
            risk_factors: Dictionary of risk factor values
            
        Returns:
            Combined risk multiplier
        """
        risk_multiplier = 1.0
        
        # Process three-year claim-free discount
        if "three_year_claim_free_discount" in risk_factors:
            factor_data = risk_factors["three_year_claim_free_discount"]
            if isinstance(factor_data, dict) and "tier" in factor_data:
                tier = factor_data["tier"]
                tier_multipliers = {
                    "LOW": 0.85,
                    "MEDIUM": 1.0,
                    "HIGH": 1.25,
                    "VERY_HIGH": 1.5
                }
                risk_multiplier *= tier_multipliers.get(tier, 1.0)
                logger.debug(f"Applied claim-free multiplier for tier {tier}: {tier_multipliers.get(tier, 1.0)}")
                
        # Process driving record classification
        if "driving_record_classification" in risk_factors:
            factor_data = risk_factors["driving_record_classification"]
            if isinstance(factor_data, dict) and "multiplier" in factor_data:
                multiplier = factor_data["multiplier"]
                risk_multiplier *= multiplier
                logger.debug(f"Applied driving record multiplier: {multiplier}")
                
        # Process driver classification
        if "driver_classification" in risk_factors:
            factor_data = risk_factors["driver_classification"]
            if isinstance(factor_data, dict) and "base_rate" in factor_data:
                base_rate = factor_data["base_rate"]
                risk_multiplier *= base_rate
                logger.debug(f"Applied driver classification rate: {base_rate}")
                
        # Apply age multiplier if available
        if "age_multiplier" in risk_factors:
            age_mult = risk_factors["age_multiplier"]
            if isinstance(age_mult, (int, float)):
                risk_multiplier *= age_mult
                logger.debug(f"Applied age multiplier: {age_mult}")
                
        # Apply vehicle multiplier if available
        if "vehicle_multiplier" in risk_factors:
            vehicle_mult = risk_factors["vehicle_multiplier"]
            if isinstance(vehicle_mult, (int, float)):
                risk_multiplier *= vehicle_mult
                logger.debug(f"Applied vehicle multiplier: {vehicle_mult}")
                
        logger.info(f"Total risk multiplier: {risk_multiplier}")
        return risk_multiplier
        
    def _calculate_coverage_multiplier(self, coverage_values: Dict[str, Any]) -> float:
        """
        Calculate coverage-based multiplier.
        
        Args:
            coverage_values: Dictionary of coverage values
            
        Returns:
            Coverage multiplier
        """
        coverage_multiplier = 1.0
        
        # Apply coverage-specific multipliers
        for coverage_type, coverage_data in coverage_values.items():
            if isinstance(coverage_data, dict) and "premium_factor" in coverage_data:
                factor = coverage_data["premium_factor"]
                coverage_multiplier += (factor - 1.0) * 0.1  # Weighted impact
                logger.debug(f"Applied {coverage_type} coverage factor: {factor}")
                
        logger.info(f"Coverage multiplier: {coverage_multiplier}")
        return coverage_multiplier
        
    def _calculate_discounts(
        self,
        base_premium: float,
        risk_factors: Dict[str, Any],
        discounts: List[PremiumComponent]
    ) -> float:
        """
        Calculate applicable discounts.
        
        Args:
            base_premium: Base premium amount
            risk_factors: Risk factor data
            discounts: List to populate with discount components
            
        Returns:
            Total discount amount
        """
        total_discount = 0.0
        
        # Claim-free discount
        if "three_year_claim_free_discount" in risk_factors:
            factor_data = risk_factors["three_year_claim_free_discount"]
            if isinstance(factor_data, dict) and "discount" in factor_data:
                discount_rate = factor_data["discount"]
                discount_amount = base_premium * discount_rate
                total_discount += discount_amount
                
                discounts.append(PremiumComponent(
                    name="Claim-Free Discount",
                    base_amount=base_premium,
                    multiplier=discount_rate,
                    final_amount=discount_amount,
                    description=f"Discount for claim-free driving ({discount_rate:.1%})"
                ))
                logger.debug(f"Applied claim-free discount: {discount_amount}")
                
        # Multi-policy discount (placeholder)
        if risk_factors.get("multi_policy", False):
            multi_discount = base_premium * 0.05  # 5% multi-policy discount
            total_discount += multi_discount
            
            discounts.append(PremiumComponent(
                name="Multi-Policy Discount",
                base_amount=base_premium,
                multiplier=0.05,
                final_amount=multi_discount,
                description="Discount for multiple policies (5%)"
            ))
            logger.debug(f"Applied multi-policy discount: {multi_discount}")
            
        logger.info(f"Total discounts: {total_discount}")
        return total_discount
        
    def _validate_calculation(self, result: PremiumCalculationResult) -> Dict[str, Any]:
        """
        Validate the premium calculation result.
        
        Args:
            result: Premium calculation result
            
        Returns:
            Validation result
        """
        validation = {
            "status": "valid",
            "issues": [],
            "warnings": []
        }
        
        # Check if premium is reasonable
        if result.total_premium <= 0:
            validation["issues"].append("Premium cannot be zero or negative")
            
        if result.total_premium < result.base_premium * 0.3:
            validation["warnings"].append("Premium is unusually low compared to base premium")
            
        if result.total_premium > result.base_premium * 3.0:
            validation["warnings"].append("Premium is unusually high compared to base premium")
            
        # Check risk multiplier reasonableness
        if result.risk_multiplier < 0.5 or result.risk_multiplier > 3.0:
            validation["warnings"].append(f"Risk multiplier ({result.risk_multiplier}) is outside normal range")
            
        # Validate components
        if not result.components:
            validation["issues"].append("No premium components found")
            
        validation["status"] = "valid" if not validation["issues"] else "invalid"
        
        logger.debug(f"Calculation validation: {validation['status']}")
        return validation
        
    def get_calculation_breakdown(self, result: PremiumCalculationResult) -> Dict[str, Any]:
        """
        Get a detailed breakdown of the premium calculation.
        
        Args:
            result: Premium calculation result
            
        Returns:
            Detailed breakdown dictionary
        """
        breakdown = {
            "summary": {
                "base_premium": result.base_premium,
                "total_premium": result.total_premium,
                "savings": sum(discount.final_amount for discount in result.discounts),
                "risk_adjustment": (result.risk_multiplier - 1.0) * result.base_premium
            },
            "components": [
                {
                    "name": comp.name,
                    "amount": comp.final_amount,
                    "description": comp.description
                }
                for comp in result.components
            ],
            "discounts": [
                {
                    "name": discount.name,
                    "amount": discount.final_amount,
                    "rate": discount.multiplier,
                    "description": discount.description
                }
                for discount in result.discounts
            ],
            "calculation_details": result.calculation_details,
            "validation": result.validation_status
        }
        
        return breakdown
        
    def get_calculation_history(self, limit: Optional[int] = None) -> List[PremiumCalculationResult]:
        """
        Get the history of premium calculations.
        
        Args:
            limit: Optional limit on number of results
            
        Returns:
            List of calculation results
        """
        if limit:
            return self.calculation_history[-limit:]
        return self.calculation_history.copy()
        
    def clear_calculation_history(self) -> None:
        """Clear the calculation history."""
        self.calculation_history.clear()
        logger.info("Calculation history cleared")
