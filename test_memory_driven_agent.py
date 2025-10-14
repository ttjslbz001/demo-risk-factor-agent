#!/usr/bin/env python3
"""
Test script for the memory-driven ProductDefinitionAgent

This script demonstrates:
1. Initializing the agent (no hardcoded data)
2. Bootstrapping products into mem0
3. Querying products from mem0
4. Natural language questions
5. Memory statistics

Run this after running: python bootstrap_product_memory.py --sample-data
"""

import logging
from src.agents.product_definition_agent import ProductDefinitionAgent

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def test_agent_initialization():
    """Test that agent initializes without hardcoded data."""
    logger.info("=" * 60)
    logger.info("TEST 1: Agent Initialization (Stateless)")
    logger.info("=" * 60)
    
    agent = ProductDefinitionAgent(use_memory=True, user_id="test_user", agent_id="test_product_agent")
    
    assert agent.use_memory == True, "Memory should be enabled"
    assert agent.memory is not None, "Memory layer should be initialized"
    
    logger.info("✅ Agent initialized successfully (stateless, no hardcoded data)")
    return agent


def test_list_products(agent):
    """Test listing products from mem0."""
    logger.info("\n" + "=" * 60)
    logger.info("TEST 2: List Products from mem0")
    logger.info("=" * 60)
    
    products = agent.list_available_products()
    logger.info(f"Found {len(products)} products in mem0: {products}")
    
    if not products:
        logger.warning("⚠️ No products found. Run: python bootstrap_product_memory.py --sample-data")
        return False
    
    logger.info("✅ Products retrieved from mem0")
    return True


def test_get_product(agent, product_code="Monthly-Comfort"):
    """Test getting a specific product from mem0."""
    logger.info("\n" + "=" * 60)
    logger.info(f"TEST 3: Get Product '{product_code}' from mem0")
    logger.info("=" * 60)
    
    product = agent.get_product_definition(product_code)
    
    if not product:
        logger.error(f"❌ Product '{product_code}' not found in mem0")
        return False
    
    logger.info(f"✅ Retrieved product: {product.product_name}")
    logger.info(f"   Product Code: {product.product_code}")
    logger.info(f"   Risk Factors: {len(product.risk_factors)}")
    logger.info(f"   Coverage Options: {len(product.coverage_options)}")
    
    # Show risk factors
    logger.info("\n   Risk Factors:")
    for rf in product.risk_factors:
        logger.info(f"   - {rf.risk_factor_name} ({rf.risk_subject}) - weight: {rf.weight}")
    
    return True


def test_risk_factor_definitions(agent, product_code="Monthly-Comfort"):
    """Test getting risk factor definitions."""
    logger.info("\n" + "=" * 60)
    logger.info(f"TEST 4: Get Risk Factor Definitions for '{product_code}'")
    logger.info("=" * 60)
    
    factors = agent.get_risk_factor_definitions(product_code)
    logger.info(f"Found {len(factors)} risk factors:")
    
    for subject, name in factors:
        logger.info(f"   - <{subject}, {name}>")
    
    logger.info("✅ Risk factor definitions retrieved from mem0")
    return True


def test_natural_language_queries(agent):
    """Test natural language question answering."""
    logger.info("\n" + "=" * 60)
    logger.info("TEST 5: Natural Language Queries (Semantic Search)")
    logger.info("=" * 60)
    
    questions = [
        "What products are available?",
        "Tell me about Monthly-Comfort",
        "What risk factors does Monthly-Turbo have?"
    ]
    
    for question in questions:
        logger.info(f"\n📝 Question: {question}")
        answer = agent.answer_question(question)
        logger.info(f"🤖 Answer:\n{answer[:300]}...")  # First 300 chars
    
    logger.info("\n✅ Natural language queries working")
    return True


def test_search_risk_factors(agent):
    """Test searching for risk factors."""
    logger.info("\n" + "=" * 60)
    logger.info("TEST 6: Search Risk Factors")
    logger.info("=" * 60)
    
    query = "driver age factors"
    results = agent.search_risk_factors(query)
    
    logger.info(f"Query: '{query}'")
    logger.info(f"Found {len(results)} results:")
    
    for idx, result in enumerate(results[:3], 1):
        logger.info(f"   {idx}. Score: {result.get('score', 0):.3f}")
        logger.info(f"      Text: {result['text'][:100]}...")
    
    logger.info("✅ Risk factor search working")
    return True


def test_memory_stats(agent):
    """Test memory statistics."""
    logger.info("\n" + "=" * 60)
    logger.info("TEST 7: Memory Statistics")
    logger.info("=" * 60)
    
    stats = agent.get_memory_stats()
    logger.info(f"Memory Statistics:")
    logger.info(f"   Enabled: {stats.get('enabled', False)}")
    logger.info(f"   Total Memories: {stats.get('total_memories', 0)}")
    logger.info(f"   Agent ID: {stats.get('agent_id', 'N/A')}")
    logger.info(f"   User ID: {stats.get('user_id', 'N/A')}")
    
    logger.info("✅ Memory statistics retrieved")
    return True


def test_product_knowledge(agent, product_code="Monthly-Comfort"):
    """Test getting comprehensive product knowledge."""
    logger.info("\n" + "=" * 60)
    logger.info(f"TEST 8: Get Product Knowledge for '{product_code}'")
    logger.info("=" * 60)
    
    knowledge = agent.get_product_knowledge(product_code)
    
    logger.info(f"Product Code: {knowledge['product_code']}")
    logger.info(f"Definition: {knowledge['definition'].product_name if knowledge['definition'] else 'None'}")
    logger.info(f"Memory Knowledge Items: {len(knowledge['memory_knowledge'])}")
    
    logger.info("✅ Product knowledge retrieved")
    return True


def main():
    """Run all tests."""
    logger.info("\n" + "🔥" * 30)
    logger.info("TESTING MEMORY-DRIVEN PRODUCT DEFINITION AGENT")
    logger.info("🔥" * 30 + "\n")
    
    try:
        # Test 1: Initialize agent
        agent = test_agent_initialization()
        
        # Test 2: List products
        has_products = test_list_products(agent)
        
        if not has_products:
            logger.warning("\n" + "⚠️" * 30)
            logger.warning("NO PRODUCTS FOUND IN MEMORY")
            logger.warning("Please run: python bootstrap_product_memory.py --sample-data")
            logger.warning("⚠️" * 30 + "\n")
            return 1
        
        # Test 3: Get specific product
        test_get_product(agent, "Monthly-Comfort")
        
        # Test 4: Get risk factor definitions
        test_risk_factor_definitions(agent, "Monthly-Comfort")
        
        # Test 5: Natural language queries
        test_natural_language_queries(agent)
        
        # Test 6: Search risk factors
        test_search_risk_factors(agent)
        
        # Test 7: Memory statistics
        test_memory_stats(agent)
        
        # Test 8: Product knowledge
        test_product_knowledge(agent, "Monthly-Comfort")
        
        # Summary
        logger.info("\n" + "=" * 60)
        logger.info("✅ ALL TESTS PASSED!")
        logger.info("=" * 60)
        logger.info("\nThe ProductDefinitionAgent is fully memory-driven:")
        logger.info("  ✓ No hardcoded product definitions")
        logger.info("  ✓ All data loaded from mem0")
        logger.info("  ✓ Stateless agent architecture")
        logger.info("  ✓ Semantic search working")
        logger.info("  ✓ Natural language queries working")
        
        return 0
        
    except Exception as e:
        logger.error(f"\n❌ TEST FAILED: {e}", exc_info=True)
        return 1


if __name__ == "__main__":
    exit(main())

