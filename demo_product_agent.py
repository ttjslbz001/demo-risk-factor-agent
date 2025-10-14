"""
Demo Script for Memory-Based Product Definition Agent

This script demonstrates the memory-based product agent capabilities
without requiring the Streamlit UI. Use this for testing and demos.
"""

import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from src.agents.product_definition_agent import ProductDefinitionAgent
from datetime import datetime


def print_header(title):
    """Print a formatted header"""
    print(f"\n{'='*70}")
    print(f"  {title}")
    print(f"{'='*70}\n")


def demo_basic_operations():
    """Demonstrate basic product definition agent operations"""
    print_header("1. Basic Product Definition Operations")
    
    # Initialize agent without memory first
    print("Initializing agent WITHOUT memory...")
    agent_no_memory = ProductDefinitionAgent(use_memory=False)
    
    # List products
    products = agent_no_memory.list_available_products()
    print(f"✅ Available products: {', '.join(products)}")
    
    # Get product definition
    product = agent_no_memory.get_product_definition("Monthly-Comfort")
    if product:
        print(f"\n📦 Product: {product.product_name}")
        print(f"   Risk Factors: {len(product.risk_factors)}")
        for rf in product.risk_factors:
            print(f"   - {rf.risk_factor_name} (weight: {rf.weight})")
    
    # Get risk factor definitions
    factors = agent_no_memory.get_risk_factor_definitions("Monthly-Comfort")
    print(f"\n🎯 Risk Factor Definitions:")
    for subject, factor_name in factors:
        print(f"   ({subject}, {factor_name})")


def demo_memory_operations():
    """Demonstrate memory-based operations"""
    print_header("2. Memory-Based Operations")
    
    # Initialize agent WITH memory
    print("Initializing agent WITH memory...")
    agent = ProductDefinitionAgent(
        use_memory=True,
        agent_id="product_definition_agent",
        user_id="demo_user"
    )
    
    # Check memory stats
    stats = agent.get_memory_stats()
    print(f"\n📊 Memory Statistics:")
    if stats.get("enabled"):
        print(f"   ✅ Memory Enabled: Yes")
        print(f"   Total Memories: {stats.get('total_memories', 0)}")
        print(f"   Agent ID: {stats.get('agent_id')}")
        print(f"   User ID: {stats.get('user_id')}")
    else:
        print(f"   ⚠️  Memory Enabled: No")
        print(f"   Message: {stats.get('message', 'N/A')}")
        print(f"\n   💡 To enable memory:")
        print(f"      1. Load knowledge: ./load_risk_knowledge.sh")
        print(f"      2. Ensure MemoryLayer is properly configured")
        return
    
    # Query knowledge
    print("\n🔍 Querying Knowledge...")
    results = agent.query_knowledge("What are driver-related risk factors?", limit=3)
    
    if results:
        print(f"   Found {len(results)} results:")
        for idx, result in enumerate(results, 1):
            print(f"\n   Result {idx} (Score: {result['score']:.4f}):")
            text = result['text'][:150]
            print(f"   {text}...")
    else:
        print("   ⚠️  No results found. Knowledge may not be loaded yet.")
        print("   💡 Run: ./load_risk_knowledge.sh")


def demo_question_answering():
    """Demonstrate question answering"""
    print_header("3. Question Answering")
    
    agent = ProductDefinitionAgent(
        use_memory=True,
        agent_id="product_definition_agent",
        user_id="demo_user"
    )
    
    # Test questions
    questions = [
        "What is the Monthly-Comfort product?",
        "What are discount factors?",
        "How many coverage types are supported?",
    ]
    
    for idx, question in enumerate(questions, 1):
        print(f"\n❓ Question {idx}: {question}")
        print("─" * 70)
        
        answer = agent.answer_question(question)
        print(answer)
        print()


def demo_risk_factor_search():
    """Demonstrate risk factor search"""
    print_header("4. Risk Factor Search")
    
    agent = ProductDefinitionAgent(
        use_memory=True,
        agent_id="product_definition_agent",
        user_id="demo_user"
    )
    
    stats = agent.get_memory_stats()
    if not stats.get("enabled") or stats.get("total_memories", 0) == 0:
        print("⚠️  Memory not enabled or no knowledge loaded")
        print("💡 Run ./load_risk_knowledge.sh first")
        return
    
    # Search for specific risk factors
    searches = [
        "driver age",
        "discount",
        "vehicle"
    ]
    
    for search_term in searches:
        print(f"\n🔎 Searching for: '{search_term}'")
        results = agent.search_risk_factors(search_term)
        
        if results:
            print(f"   Found {len(results)} risk factors:")
            for idx, result in enumerate(results[:3], 1):
                text = result['text'][:100]
                print(f"   {idx}. {text}...")
        else:
            print("   No results found")


def demo_learning():
    """Demonstrate learning capabilities"""
    print_header("5. Learning from Interactions")
    
    agent = ProductDefinitionAgent(
        use_memory=True,
        agent_id="product_definition_agent",
        user_id="demo_user"
    )
    
    stats = agent.get_memory_stats()
    if not stats.get("enabled"):
        print("⚠️  Memory not enabled, cannot demonstrate learning")
        return
    
    print("Recording interactions...")
    
    # Simulate various interactions
    interactions = [
        ("query", {"query": "What are driver factors?", "response": "Driver factors include..."}),
        ("definition_request", {"product_code": "Monthly-Comfort", "factors": 3}),
        ("usage_pattern", {"pattern": "frequent_discount_queries", "frequency": 5}),
    ]
    
    for interaction_type, data in interactions:
        success = agent.learn_from_interaction(interaction_type, data)
        if success:
            print(f"   ✅ Learned from {interaction_type}")
        else:
            print(f"   ❌ Failed to learn from {interaction_type}")
    
    # Check updated memory stats
    new_stats = agent.get_memory_stats()
    if new_stats.get("enabled"):
        print(f"\n📊 Updated Memory Statistics:")
        print(f"   Total Memories: {new_stats.get('total_memories', 0)}")


def demo_product_knowledge():
    """Demonstrate comprehensive product knowledge retrieval"""
    print_header("6. Product Knowledge Retrieval")
    
    agent = ProductDefinitionAgent(
        use_memory=True,
        agent_id="product_definition_agent",
        user_id="demo_user"
    )
    
    # Get comprehensive knowledge about a product
    print("Getting comprehensive knowledge for Monthly-Comfort...")
    knowledge = agent.get_product_knowledge("Monthly-Comfort")
    
    print(f"\n📦 Product Code: {knowledge['product_code']}")
    
    product = knowledge['definition']
    if product:
        print(f"   Name: {product.product_name}")
        print(f"   Risk Factors: {len(product.risk_factors)}")
        print(f"   Coverage Options: {len(product.coverage_options)}")
    
    # Memory knowledge
    memory_knowledge = knowledge.get('memory_knowledge', [])
    if memory_knowledge:
        print(f"\n🧠 Additional knowledge from memory ({len(memory_knowledge)} items):")
        for idx, know in enumerate(memory_knowledge[:2], 1):
            text = know['text'][:100]
            print(f"   {idx}. {text}...")
    else:
        print(f"\n⚠️  No additional memory knowledge (knowledge may not be loaded)")


def main():
    """Run all demos"""
    print("\n" + "="*70)
    print("  🧠 Memory-Based Product Definition Agent Demo")
    print("="*70)
    print("\nThis demo showcases the memory-enhanced product definition agent")
    print("Following the mem0 pattern for intelligent, learning agents\n")
    
    try:
        # Run demos
        demo_basic_operations()
        demo_memory_operations()
        demo_question_answering()
        demo_risk_factor_search()
        demo_learning()
        demo_product_knowledge()
        
        # Summary
        print_header("Demo Complete")
        print("✨ All demos completed successfully!\n")
        print("Next Steps:")
        print("  1. Load knowledge: ./load_risk_knowledge.sh")
        print("  2. Run Streamlit app: ./run_product_agent.sh")
        print("  3. Explore the interactive UI\n")
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Demo interrupted by user")
    except Exception as e:
        print(f"\n\n❌ Error during demo: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()

