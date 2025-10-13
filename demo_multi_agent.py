#!/usr/bin/env python3
"""
Demo script for the Multi-Agent Insurance Rating Engine

This script demonstrates how to use the multi-agent graph system
to process insurance applications and calculate premiums.

Usage:
    python demo_multi_agent.py
"""

import json
import logging
from typing import Dict, Any
from datetime import datetime

from src.agents.multi_agent_graph import create_rating_engine, InsuranceRatingEngine

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)


def create_sample_application() -> Dict[str, Any]:
    """Create a sample insurance application for demonstration."""
    return {
        "household": {
            "address": "123 Main Street, Anytown, CA 90210",
            "zip_code": "90210",
            "home_ownership": "own",
            "residents_count": 2
        },
        "drivers": [
            {
                "name": "John Smith",
                "age": 35,
                "gender": "M",
                "marital_status": "married",
                "license_years": 18,
                "education": "college",
                "occupation": "engineer",
                "violations": [],
                "claims": [],
                "credit_score": 750
            },
            {
                "name": "Jane Smith",
                "age": 32,
                "gender": "F",
                "marital_status": "married",
                "license_years": 14,
                "education": "college",
                "occupation": "teacher",
                "violations": [
                    {
                        "type": "speeding",
                        "date": "2022-03-15",
                        "points": 2
                    }
                ],
                "claims": [],
                "credit_score": 780
            }
        ],
        "vehicles": [
            {
                "make": "Toyota",
                "model": "Camry",
                "year": 2021,
                "vin": "1234567890ABCDEFG",
                "usage": "commuting",
                "annual_mileage": 12000,
                "safety_features": ["abs", "airbags", "backup_camera"],
                "anti_theft": True,
                "garage_kept": True
            },
            {
                "make": "Honda",
                "model": "CR-V",
                "year": 2019,
                "vin": "ABCDEFG1234567890",
                "usage": "leisure",
                "annual_mileage": 8000,
                "safety_features": ["abs", "airbags", "lane_assist"],
                "anti_theft": False,
                "garage_kept": False
            }
        ],
        "coverage_preferences": {
            "liability_limit": 100000,
            "comprehensive_deductible": 500,
            "collision_deductible": 500,
            "rental_car_coverage": True,
            "roadside_assistance": True
        }
    }


def demonstrate_single_product(product_code: str) -> None:
    """Demonstrate the multi-agent system with a single product."""
    print(f"\n{'='*60}")
    print(f"DEMONSTRATING: {product_code}")
    print(f"{'='*60}")
    
    # Create rating engine for the product
    engine = create_rating_engine(product_code)
    
    # Show graph status
    status = engine.get_graph_status()
    print(f"\nGraph Status:")
    print(f"  - Strands Available: {status['strands_available']}")
    print(f"  - Graph Built: {status['graph_built']}")
    print(f"  - Agents Initialized: {status['agents_initialized']}")
    print(f"  - Product Code: {status['product_code']}")
    
    # Create sample application
    application = create_sample_application()
    application_json = json.dumps(application, indent=2)
    
    print(f"\nSample Application:")
    print(f"  - Household: {application['household']['address']}")
    print(f"  - Drivers: {len(application['drivers'])} drivers")
    print(f"  - Vehicles: {len(application['vehicles'])} vehicles")
    
    # Process the application
    print(f"\nProcessing application with multi-agent graph...")
    start_time = datetime.now()
    
    try:
        result = engine.process_application_with_graph(application_json, product_code)
        
        end_time = datetime.now()
        processing_time = (end_time - start_time).total_seconds()
        
        # Display results
        print(f"\nProcessing Results:")
        print(f"  - Status: {result.status}")
        print(f"  - Session ID: {result.session_id}")
        print(f"  - Processing Time: {processing_time:.2f}s ({result.execution_time_ms}ms)")
        print(f"  - Execution Order: {' -> '.join(result.execution_order)}")
        
        if result.errors:
            print(f"  - Errors: {len(result.errors)}")
            for error in result.errors:
                print(f"    * {error}")
                
        if result.warnings:
            print(f"  - Warnings: {len(result.warnings)}")
            for warning in result.warnings:
                print(f"    * {warning}")
        
        # Show risk assessment results
        if result.risk_assessment:
            print(f"\nRisk Assessment:")
            risk_data = result.risk_assessment
            if "overall_risk_tier" in risk_data:
                print(f"  - Overall Risk Tier: {risk_data['overall_risk_tier']}")
            if "confidence" in risk_data:
                print(f"  - Confidence: {risk_data['confidence']:.1%}")
            if "key_factors" in risk_data:
                print(f"  - Key Factors: {', '.join(risk_data['key_factors'])}")
        
        # Show premium calculation results
        if result.premium_calculation:
            print(f"\nPremium Calculation:")
            premium_data = result.premium_calculation
            if "base_premium" in premium_data:
                print(f"  - Base Premium: ${premium_data['base_premium']:.2f}")
            if "total_premium" in premium_data:
                print(f"  - Total Premium: ${premium_data['total_premium']:.2f}")
            if "calculation_valid" in premium_data:
                print(f"  - Calculation Valid: {premium_data['calculation_valid']}")
        
    except Exception as e:
        print(f"Error processing application: {e}")
        logger.exception("Application processing failed")


def demonstrate_all_products() -> None:
    """Demonstrate the multi-agent system with all available products."""
    products = ["Monthly-Economy", "Monthly-Comfort", "Monthly-Turbo"]
    
    print("MULTI-AGENT INSURANCE RATING ENGINE DEMONSTRATION")
    print("=" * 60)
    print("This demo shows how the multi-agent graph system processes")
    print("insurance applications using the Strands Agents framework.")
    print("\nArchitecture:")
    print("  1. Orchestrator Agent - Validates and coordinates workflow")
    print("  2. Product Definition Agent - Defines risk factors and rules")  
    print("  3. Risk Factor Reasoning Agent - Assesses risk tiers")
    print("  4. Data Lookup Agent - Provides mapping values")
    print("  5. Premium Calculation Agent - Calculates final premium")
    
    for product_code in products:
        try:
            demonstrate_single_product(product_code)
        except Exception as e:
            print(f"\nError demonstrating {product_code}: {e}")
            logger.exception(f"Demo failed for {product_code}")
    
    print(f"\n{'='*60}")
    print("DEMONSTRATION COMPLETE")
    print(f"{'='*60}")


def demonstrate_individual_agents() -> None:
    """Demonstrate individual agent capabilities."""
    print(f"\n{'='*60}")
    print("INDIVIDUAL AGENT CAPABILITIES")
    print(f"{'='*60}")
    
    # Create engine to access agents
    engine = create_rating_engine("Monthly-Comfort")
    
    # Product Definition Agent
    print(f"\n1. Product Definition Agent:")
    products = engine.product_agent.list_available_products()
    print(f"   Available Products: {', '.join(products)}")
    
    for product in products:
        risk_factors = engine.product_agent.get_risk_factor_definitions(product)
        print(f"   {product} Risk Factors: {len(risk_factors)}")
        
    # Data Lookup Agent  
    print(f"\n2. Data Lookup Agent:")
    validation = engine.lookup_agent.validate_lookup_tables()
    print(f"   Lookup Tables: {validation['table_count']} tables, {validation['total_entries']} entries")
    print(f"   Validation: {'Valid' if validation['valid'] else 'Invalid'}")
    
    # Sample lookups
    print(f"   Sample Lookups:")
    print(f"     - Risk Tier LOW: {engine.lookup_agent.lookup_risk_tier_multiplier('LOW')}")
    print(f"     - 3 Years Claim-Free: {engine.lookup_agent.lookup_claim_free_discount(3)}")
    print(f"     - Base Premium Comfort: ${engine.lookup_agent.lookup_base_premium('Monthly-Comfort')}")
    
    # Premium Calculation Agent
    print(f"\n3. Premium Calculation Agent:")
    sample_risk_factors = {
        "three_year_claim_free_discount": {"tier": "LOW", "discount": 0.15},
        "driving_record_classification": {"multiplier": 0.9, "tier": "LOW"}
    }
    sample_coverage = {"liability": {"base": 50000, "premium_factor": 1.0}}
    
    calc_result = engine.premium_agent.calculate_premium(
        base_premium=180.0,
        risk_factors=sample_risk_factors,
        coverage_values=sample_coverage,
        product_code="Monthly-Comfort"
    )
    
    print(f"   Sample Calculation:")
    print(f"     - Base Premium: ${calc_result.base_premium}")
    print(f"     - Total Premium: ${calc_result.total_premium}")
    print(f"     - Risk Multiplier: {calc_result.risk_multiplier}")
    print(f"     - Components: {len(calc_result.components)}")
    print(f"     - Discounts: {len(calc_result.discounts)}")


if __name__ == "__main__":
    try:
        # Run the complete demonstration
        demonstrate_all_products()
        
        # Show individual agent capabilities
        demonstrate_individual_agents()
        
    except KeyboardInterrupt:
        print("\nDemo interrupted by user")
    except Exception as e:
        print(f"\nDemo failed with error: {e}")
        logger.exception("Demo script failed")
    finally:
        print("\nDemo script finished.")
