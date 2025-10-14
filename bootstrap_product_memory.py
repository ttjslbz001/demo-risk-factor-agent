#!/usr/bin/env python3
"""
Bootstrap Product Memory Script

This script helps initialize the ProductDefinitionAgent's memory with product definitions.
It can load product data from various sources and store them in the memory system.

Usage:
    python bootstrap_product_memory.py --products Monthly-Comfort,Monthly-Economy
    python bootstrap_product_memory.py --from-rules docs/insurance_risk_factor_agent/3_year_claim_free_discount
    python bootstrap_product_memory.py --sample-data
"""

import argparse
import json
import logging
from typing import Dict, Any, List
from datetime import datetime

from src.agents.product_definition_agent import ProductDefinitionAgent, ProductDefinition, RiskFactorDefinition

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def create_sample_products() -> List[ProductDefinition]:
    """Create sample product definitions for demonstration."""
    
    products = []
    
    # Monthly-Comfort Product
    comfort_product = ProductDefinition(
        product_code="Monthly-Comfort",
        product_name="Monthly Comfort Package",
        risk_factors=[
            RiskFactorDefinition(
                risk_subject="driver",
                risk_factor_name="three_year_claim_free_discount",
                description="Three-year claim-free driving discount assessment",
                evaluation_rules=["P36_Three_Year_Safe_Driving_Discount"],
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
        assessment_rules={
            "P36_Three_Year_Safe_Driving_Discount": {
                "id": "P36_Three_Year_Safe_Driving_Discount",
                "name": "Three Year Safe Driving Discount",
                "description": "Discount for drivers with 3+ years claim-free record"
            },
            "D04_Driving_Record_Classification": {
                "id": "D04_Driving_Record_Classification",
                "name": "Driving Record Classification",
                "description": "Classification based on driving violations and claims"
            },
            "D03_Driver_Classification": {
                "id": "D03_Driver_Classification",
                "name": "Driver Classification",
                "description": "Basic classification by age and experience"
            }
        },
        coverage_options={
            "liability_coverage": {"min": 25000, "max": 100000, "default": 50000},
            "comprehensive": {"available": True, "deductible_options": [250, 500, 1000]},
            "collision": {"available": True, "deductible_options": [250, 500, 1000]}
        }
    )
    products.append(comfort_product)
    
    # Monthly-Economy Product
    economy_product = ProductDefinition(
        product_code="Monthly-Economy",
        product_name="Monthly Economy Package",
        risk_factors=[
            RiskFactorDefinition(
                risk_subject="driver",
                risk_factor_name="basic_driver_assessment",
                description="Basic driver assessment for economy package",
                evaluation_rules=["D03_Driver_Classification"],
                required=True,
                weight=1.0
            )
        ],
        assessment_rules={
            "D03_Driver_Classification": {
                "id": "D03_Driver_Classification",
                "name": "Driver Classification",
                "description": "Basic classification by age and experience"
            }
        },
        coverage_options={
            "liability_coverage": {"min": 15000, "max": 50000, "default": 25000}
        }
    )
    products.append(economy_product)
    
    # Monthly-Turbo Product
    turbo_product = ProductDefinition(
        product_code="Monthly-Turbo",
        product_name="Monthly Turbo Package",
        risk_factors=[
            RiskFactorDefinition(
                risk_subject="driver",
                risk_factor_name="comprehensive_risk_assessment",
                description="Comprehensive risk assessment for turbo package",
                evaluation_rules=["D03_Driver_Classification", "D04_Driving_Record_Classification", "P36_Three_Year_Safe_Driving_Discount"],
                required=True,
                weight=1.5
            ),
            RiskFactorDefinition(
                risk_subject="vehicle",
                risk_factor_name="vehicle_safety_rating",
                description="Vehicle safety features and ratings assessment",
                evaluation_rules=["V01_Vehicle_Safety_Assessment"],
                required=True,
                weight=1.2
            )
        ],
        assessment_rules={
            "D03_Driver_Classification": {
                "id": "D03_Driver_Classification",
                "name": "Driver Classification",
                "description": "Basic classification by age and experience"
            },
            "D04_Driving_Record_Classification": {
                "id": "D04_Driving_Record_Classification",
                "name": "Driving Record Classification",
                "description": "Classification based on driving violations and claims"
            },
            "P36_Three_Year_Safe_Driving_Discount": {
                "id": "P36_Three_Year_Safe_Driving_Discount",
                "name": "Three Year Safe Driving Discount",
                "description": "Discount for drivers with 3+ years claim-free record"
            },
            "V01_Vehicle_Safety_Assessment": {
                "id": "V01_Vehicle_Safety_Assessment",
                "name": "Vehicle Safety Assessment",
                "description": "Assessment of vehicle safety features and ratings"
            }
        },
        coverage_options={
            "liability_coverage": {"min": 50000, "max": 250000, "default": 100000},
            "comprehensive": {"available": True, "deductible_options": [100, 250, 500]},
            "collision": {"available": True, "deductible_options": [100, 250, 500]},
            "rental_car": {"available": True, "daily_limit": 50},
            "roadside_assistance": {"available": True}
        }
    )
    products.append(turbo_product)
    
    return products


def bootstrap_memory(agent: ProductDefinitionAgent, products: List[ProductDefinition]) -> None:
    """Store products in agent's memory."""
    logger.info(f"Bootstrapping memory with {len(products)} products...")
    
    success_count = 0
    for product in products:
        logger.info(f"Storing product: {product.product_code}")
        if agent.store_product_to_memory(product):
            success_count += 1
            logger.info(f"  ✓ Successfully stored {product.product_code}")
        else:
            logger.error(f"  ✗ Failed to store {product.product_code}")
    
    logger.info(f"\nBootstrap complete: {success_count}/{len(products)} products stored successfully")


def main():
    parser = argparse.ArgumentParser(description="Bootstrap Product Definition Agent Memory")
    parser.add_argument(
        "--sample-data",
        action="store_true",
        help="Load sample product data (Monthly-Comfort, Monthly-Economy, Monthly-Turbo)"
    )
    parser.add_argument(
        "--products",
        type=str,
        help="Comma-separated list of product codes to create"
    )
    parser.add_argument(
        "--from-rules",
        type=str,
        help="Load products from rules directory"
    )
    parser.add_argument(
        "--user-id",
        type=str,
        default="system",
        help="User ID for memory isolation (default: system)"
    )
    parser.add_argument(
        "--agent-id",
        type=str,
        default="product_definition_agent",
        help="Agent ID for memory isolation (default: product_definition_agent)"
    )
    parser.add_argument(
        "--clear-existing",
        action="store_true",
        help="Clear existing product definitions before bootstrapping"
    )
    
    args = parser.parse_args()
    
    # Initialize agent
    logger.info("Initializing ProductDefinitionAgent...")
    agent = ProductDefinitionAgent(
        use_memory=True,
        agent_id=args.agent_id,
        user_id=args.user_id
    )
    
    if not agent.use_memory or not agent.memory:
        logger.error("Memory system is not available. Cannot bootstrap.")
        return 1
    
    # Get products to store
    products_to_store = []
    
    if args.sample_data:
        logger.info("Loading sample product data...")
        products_to_store = create_sample_products()
    
    elif args.from_rules:
        logger.info(f"Loading products from rules directory: {args.from_rules}")
        # Load from rules directory
        # This would need to be implemented based on your rule file structure
        logger.warning("Loading from rules directory is not yet fully implemented")
        return 1
    
    elif args.products:
        logger.error("Custom product creation not yet implemented. Use --sample-data instead.")
        return 1
    
    else:
        logger.error("No data source specified. Use --sample-data, --from-rules, or --products")
        parser.print_help()
        return 1
    
    # Bootstrap the memory
    if products_to_store:
        bootstrap_memory(agent, products_to_store)
        
        # Verify by querying
        logger.info("\nVerifying stored products...")
        loaded_products = agent.list_available_products()
        logger.info(f"Available products in memory: {loaded_products}")
        
        # Show memory stats
        stats = agent.get_memory_stats()
        logger.info(f"\nMemory statistics: {stats}")
        
        logger.info("\n✓ Bootstrap completed successfully!")
        logger.info("\nYou can now use the ProductDefinitionAgent with memory-based product definitions.")
        return 0
    else:
        logger.error("No products to store")
        return 1


if __name__ == "__main__":
    exit(main())

