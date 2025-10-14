"""
Quick diagnostic script to test memory operations
Run this to verify that memories are being stored and retrieved correctly
"""

import sys
from test_memory import MemoryLayer
from datetime import datetime

def main():
    print("=" * 60)
    print("MEMORY LAYER DIAGNOSTIC TEST")
    print("=" * 60)
    
    # Initialize
    print("\n1️⃣  Initializing Memory Layer...")
    try:
        memory_layer = MemoryLayer(
            llm_provider="openai",
            temperature=0.7,
            max_tokens=2000
        )
        print("✅ Memory Layer initialized successfully")
        print(f"   Config: {memory_layer.config['vector_store']}")
    except Exception as e:
        print(f"❌ Failed to initialize: {e}")
        import traceback
        traceback.print_exc()
        return
    
    # Test user
    test_user = "user_123"
    
    # Add a test memory
    print(f"\n2️⃣  Adding test memory for user: {test_user}")
    test_text = f"I am John Smith, a 45-year-old engineer. I have 20 years of safe driving experience with no accidents. I drive a 2022 Honda Accord and live in California."
    print(f"   Text: {test_text}")
    
    try:
        result = memory_layer.add_memory(
            text=test_text,
            user_id=test_user,
            metadata={
                "category": "test",
                "timestamp": datetime.now().isoformat()
            }
        )
        print(f"✅ Add operation completed")
        print(f"   Result type: {type(result)}")
        print(f"   Result: {result}")
        
        # Try to extract memory ID
        memory_id = None
        if isinstance(result, dict):
            if 'results' in result:
                results_list = result.get('results', [])
                if results_list:
                    memory_id = results_list[0].get('id') if isinstance(results_list[0], dict) else None
                    print(f"   Memory ID: {memory_id}")
                else:
                    print("   ⚠️  Results list is empty")
            elif 'id' in result:
                memory_id = result.get('id')
                print(f"   Memory ID: {memory_id}")
            else:
                print(f"   ⚠️  No 'results' or 'id' key in response")
                print(f"   Available keys: {list(result.keys())}")
        
    except Exception as e:
        print(f"❌ Failed to add memory: {e}")
        import traceback
        traceback.print_exc()
        return
    
    # Get all memories for user
    print(f"\n3️⃣  Retrieving all memories for user: {test_user}")
    try:
        memories = memory_layer.get_memories(user_id=test_user)
        print(f"✅ Get operation completed")
        print(f"   Result type: {type(memories)}")
        print(f"   Number of memories: {len(memories) if isinstance(memories, list) else 'N/A'}")
        
        if isinstance(memories, list):
            if memories:
                print(f"\n   Found {len(memories)} memories:")
                for idx, mem in enumerate(memories, 1):
                    if isinstance(mem, dict):
                        mem_text = mem.get('memory', mem.get('text', str(mem)))
                        mem_id = mem.get('id', 'N/A')
                        print(f"   {idx}. ID: {mem_id}")
                        print(f"      Text: {mem_text[:80]}...")
                    else:
                        print(f"   {idx}. {mem}")
            else:
                print("   ⚠️  Memory list is empty")
        else:
            print(f"   ⚠️  Unexpected response type: {memories}")
            
    except Exception as e:
        print(f"❌ Failed to get memories: {e}")
        import traceback
        traceback.print_exc()
        return
    
    # Search memories
    print(f"\n4️⃣  Searching memories for user: {test_user}")
    try:
        results = memory_layer.search_memories(
            query="test memory",
            user_id=test_user,
            limit=5
        )
        print(f"✅ Search operation completed")
        print(f"   Result type: {type(results)}")
        print(f"   Number of results: {len(results) if isinstance(results, list) else 'N/A'}")
        
        if isinstance(results, list) and results:
            print(f"\n   Found {len(results)} results:")
            for idx, res in enumerate(results, 1):
                if isinstance(res, dict):
                    res_text = res.get('memory', res.get('text', str(res)))
                    score = res.get('score', 'N/A')
                    print(f"   {idx}. Score: {score}")
                    print(f"      Text: {res_text[:80]}...")
                else:
                    print(f"   {idx}. {res}")
        elif isinstance(results, list):
            print("   ⚠️  Search results list is empty")
        else:
            print(f"   ⚠️  Unexpected response type: {results}")
            
    except Exception as e:
        print(f"❌ Failed to search memories: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n" + "=" * 60)
    print("DIAGNOSTIC TEST COMPLETED")
    print("=" * 60)
    
    # Prompt for cleanup
    cleanup = input("\nDelete test memory? (y/n): ")
    if cleanup.lower() in ['y', 'yes']:
        try:
            result = memory_layer.delete_all_memories(user_id=test_user)
            print(f"✅ Cleanup completed: {result}")
        except Exception as e:
            print(f"❌ Cleanup failed: {e}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Test interrupted by user")
    except Exception as e:
        print(f"\n\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()

