"""
Query Risk Factors - Detailed Results
Show full details of risk factor search results
"""

import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from src.agents.product_definition_agent import ProductDefinitionAgent
import json


def print_separator(char="=", length=80):
    print(char * length)


def print_result_details(results, query):
    """Print detailed search results"""
    print_separator("=")
    print(f"QUERY: {query}")
    print_separator("=")
    print(f"\nFound {len(results)} result(s)\n")
    
    for idx, result in enumerate(results, 1):
        print_separator("-")
        print(f"RESULT #{idx}")
        print_separator("-")
        
        # Extract result data
        text = result.get('text', '')
        score = result.get('score', 0)
        metadata = result.get('metadata', {})
        
        # Print score
        if isinstance(score, (int, float)):
            print(f"\n📊 Relevance Score: {score:.4f}")
        else:
            print(f"\n📊 Relevance Score: {score}")
        
        # Print text content
        print(f"\n📝 Content:")
        print("-" * 80)
        print(text)
        print("-" * 80)
        
        # Print metadata if available
        if metadata:
            print(f"\n📋 Metadata:")
            for key, value in metadata.items():
                print(f"   • {key}: {value}")
        
        print()  # Extra line between results


def main():
    print("\n🔍 Risk Factor Search - Detailed Results\n")
    
    # Initialize agent
    print("Initializing agent...")
    agent = ProductDefinitionAgent(use_memory=True)
    
    # Check memory stats
    stats = agent.get_memory_stats()
    print(f"Memory enabled: {stats.get('enabled', False)}")
    print(f"Total memories: {stats.get('total_memories', 0)}\n")
    
    # Query
    query = "which risk factors used for insurance quote premium calculation and rule assessment"
    
    print(f"Searching for: '{query}'")
    print("Please wait...\n")
    
    # Search with different methods
    
    # Method 1: General knowledge query
    print_separator("=")
    print("METHOD 1: General Knowledge Query")
    print_separator("=")
    results = agent.query_knowledge(query, limit=5)
    print_result_details(results, query)
    
    # Method 2: Risk factor specific search
    print_separator("=")
    print("METHOD 2: Risk Factor Specific Search")
    print_separator("=")
    risk_results = agent.search_risk_factors(query)
    print_result_details(risk_results, query)
    
    # Method 3: Natural language answer
    print_separator("=")
    print("METHOD 3: Natural Language Answer")
    print_separator("=")
    print(f"\nQUERY: {query}\n")
    answer = agent.answer_question(query)
    print("ANSWER:")
    print("-" * 80)
    print(answer)
    print("-" * 80)
    print()
    
    # Additional queries for context
    print_separator("=")
    print("ADDITIONAL CONTEXT SEARCHES")
    print_separator("=")
    
    additional_queries = [
        "risk factors for premium calculation",
        "driver risk factors",
        "vehicle risk factors",
        "discount risk factors"
    ]
    
    for add_query in additional_queries:
        print(f"\n🔍 Searching: '{add_query}'")
        add_results = agent.query_knowledge(add_query, limit=3)
        
        if add_results:
            print(f"   Found {len(add_results)} results:")
            for idx, result in enumerate(add_results[:2], 1):  # Show top 2
                text_preview = result['text'][:150].replace('\n', ' ')
                score = result.get('score', 0)
                print(f"   {idx}. [{score:.4f}] {text_preview}...")
        else:
            print("   No results found")
    
    print("\n" + "=" * 80)
    print("Search Complete!")
    print("=" * 80 + "\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Search interrupted by user")
    except Exception as e:
        print(f"\n\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()


