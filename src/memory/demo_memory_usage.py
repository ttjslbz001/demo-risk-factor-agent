"""
Demo script showing how to use the MemoryLayer programmatically
This demonstrates various memory operations without the Streamlit UI
"""

from test_memory import MemoryLayer
from datetime import datetime
import time

def print_section(title):
    """Print a formatted section header"""
    print(f"\n{'='*60}")
    print(f"  {title}")
    print('='*60)

def main():
    print("🧠 Agent Memory System Demo")
    print("Demonstrating programmatic memory management")
    
    # Initialize Memory Layer
    print_section("1. Initializing Memory Layer")
    memory_layer = MemoryLayer(
        llm_provider="openai",
        temperature=0.7,
        max_tokens=2000
    )
    print("✅ Memory Layer initialized successfully")
    
    # Demo identifiers
    user_id = "demo_user_001"
    agent_id = "risk_assessment_agent"
    run_id = f"run_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    print(f"👤 User ID: {user_id}")
    print(f"🤖 Agent ID: {agent_id}")
    print(f"▶️  Run ID: {run_id}")
    
    # Add memories
    print_section("2. Adding Memories")
    
    memories_to_add = [
        {
            "text": "User has been a safe driver for 10 years with no accidents or violations",
            "metadata": {
                "category": "driving_history",
                "priority": "high",
                "source": "user_application",
                "timestamp": datetime.now().isoformat()
            }
        },
        {
            "text": "User prefers comprehensive coverage with low deductibles",
            "metadata": {
                "category": "preferences",
                "priority": "medium",
                "source": "user_input",
                "timestamp": datetime.now().isoformat()
            }
        },
        {
            "text": "Vehicle is a 2020 Honda Accord, valued at $25,000",
            "metadata": {
                "category": "vehicle_info",
                "priority": "high",
                "source": "vehicle_database",
                "timestamp": datetime.now().isoformat()
            }
        },
        {
            "text": "User lives in a low-risk zip code with minimal theft and accident rates",
            "metadata": {
                "category": "location_info",
                "priority": "medium",
                "source": "risk_assessment",
                "timestamp": datetime.now().isoformat()
            }
        }
    ]
    
    added_memory_ids = []
    for idx, memory_data in enumerate(memories_to_add, 1):
        print(f"\nAdding memory {idx}...")
        result = memory_layer.add_memory(
            text=memory_data["text"],
            user_id=user_id,
            agent_id=agent_id,
            run_id=run_id,
            metadata=memory_data["metadata"]
        )
        
        # Extract memory ID from result (handle different response formats)
        memory_id = 'unknown'
        if isinstance(result, dict):
            if 'results' in result:
                results = result.get('results', [])
                if results and len(results) > 0:
                    memory_id = results[0].get('id', 'unknown') if isinstance(results[0], dict) else 'unknown'
            elif 'id' in result:
                memory_id = result.get('id', 'unknown')
        
        added_memory_ids.append(memory_id)
        print(f"✅ Added: {memory_data['text'][:50]}...")
        print(f"   ID: {memory_id}")
        time.sleep(0.5)  # Brief pause to avoid rate limiting
    
    # Search memories
    print_section("3. Searching Memories")
    
    search_queries = [
        "What is the user's driving history?",
        "Tell me about the user's vehicle",
        "What are the user's insurance preferences?"
    ]
    
    for query in search_queries:
        print(f"\n🔍 Query: '{query}'")
        results = memory_layer.search_memories(
            query=query,
            user_id=user_id,
            agent_id=agent_id,
            limit=2
        )
        
        if results:
            for idx, result in enumerate(results, 1):
                # Handle both dict and string responses
                if isinstance(result, dict):
                    score = result.get('score', 'N/A')
                    if isinstance(score, (int, float)):
                        print(f"   Result {idx} (Score: {score:.4f}):")
                    else:
                        print(f"   Result {idx} (Score: {score}):")
                    memory_text = result.get('memory', result.get('text', str(result)))
                    print(f"   {str(memory_text)[:80]}...")
                else:
                    # If result is a string or other type
                    print(f"   Result {idx}:")
                    print(f"   {str(result)[:80]}...")
        else:
            print("   No results found")
        time.sleep(0.5)
    
    # Get all memories
    print_section("4. Retrieving All Memories")
    
    all_memories = memory_layer.get_memories(
        user_id=user_id,
        agent_id=agent_id,
        run_id=run_id
    )
    
    print(f"Found {len(all_memories)} memories for this session:")
    for idx, memory in enumerate(all_memories, 1):
        # Handle both dict and string responses
        if isinstance(memory, dict):
            memory_text = memory.get('memory', memory.get('text', str(memory)))
            print(f"\n{idx}. {str(memory_text)[:60]}...")
            if 'metadata' in memory and isinstance(memory['metadata'], dict):
                category = memory['metadata'].get('category', 'N/A')
                priority = memory['metadata'].get('priority', 'N/A')
                print(f"   Category: {category} | Priority: {priority}")
        else:
            print(f"\n{idx}. {str(memory)[:60]}...")
    
    # Update a memory
    print_section("5. Updating a Memory")
    
    if added_memory_ids:
        memory_to_update = added_memory_ids[0]
        print(f"Updating memory ID: {memory_to_update}")
        
        update_result = memory_layer.update_memory(
            memory_id=memory_to_update,
            text="User has been a safe driver for 10 years with no accidents, violations, or insurance claims. Perfect driving record.",
            user_id=user_id,
            agent_id=agent_id,
            run_id=run_id,
            metadata={
                "category": "driving_history",
                "priority": "high",
                "source": "user_application",
                "timestamp": datetime.now().isoformat(),
                "updated": True
            }
        )
        print("✅ Memory updated successfully")
        print(f"   Result: {update_result}")
    
    # Get memory history
    print_section("6. Memory History")
    
    if added_memory_ids:
        memory_for_history = added_memory_ids[0]
        print(f"Getting history for memory ID: {memory_for_history}")
        
        try:
            history = memory_layer.get_memory_history(
                memory_id=memory_for_history,
                user_id=user_id,
                agent_id=agent_id,
                run_id=run_id
            )
            
            if history:
                print(f"Found {len(history)} history entries")
                for idx, entry in enumerate(history, 1):
                    print(f"\n   Version {idx}:")
                    print(f"   {entry}")
            else:
                print("No history available for this memory")
        except Exception as e:
            print(f"Note: History feature might not be available: {str(e)}")
    
    # Demonstrate context-aware search
    print_section("7. Context-Aware Search")
    
    print("\n🤖 Agent performing risk assessment using memory...")
    
    # Search for relevant information
    risk_factors = memory_layer.search_memories(
        query="What factors affect this user's insurance risk profile?",
        user_id=user_id,
        agent_id=agent_id,
        limit=5
    )
    
    print("\nRelevant risk factors found:")
    for idx, factor in enumerate(risk_factors, 1):
        # Handle both dict and string responses
        if isinstance(factor, dict):
            memory_text = factor.get('memory', factor.get('text', str(factor)))
            score = factor.get('score', 0)
            print(f"\n{idx}. {memory_text}")
            if isinstance(score, (int, float)):
                print(f"   Relevance Score: {score:.4f}")
            else:
                print(f"   Relevance Score: {score}")
        else:
            print(f"\n{idx}. {str(factor)}")
            print(f"   Relevance Score: N/A")
    
    # Cleanup option
    print_section("8. Cleanup (Optional)")
    
    cleanup = input("\n⚠️  Would you like to delete all demo memories? (yes/no): ")
    if cleanup.lower() in ['yes', 'y']:
        print(f"\nDeleting all memories for run: {run_id}")
        delete_result = memory_layer.delete_all_memories(
            user_id=user_id,
            agent_id=agent_id,
            run_id=run_id
        )
        print("✅ Demo memories deleted")
        print(f"   Result: {delete_result}")
    else:
        print("Keeping demo memories. You can view them in the Streamlit app.")
        print(f"Use these identifiers:")
        print(f"   User ID: {user_id}")
        print(f"   Agent ID: {agent_id}")
        print(f"   Run ID: {run_id}")
    
    print_section("Demo Complete")
    print("✨ Memory Layer demo finished successfully!")
    print("\n💡 Next steps:")
    print("   1. Run the Streamlit app: streamlit run memory_manager_app.py")
    print("   2. Use the identifiers above to view these memories in the UI")
    print("   3. Explore the different memory management features")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Demo interrupted by user")
    except Exception as e:
        print(f"\n\n❌ Error during demo: {str(e)}")
        import traceback
        traceback.print_exc()

