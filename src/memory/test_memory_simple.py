"""
Simple test to verify mem0 is extracting and storing memories correctly
"""

from test_memory import MemoryLayer

# Initialize
print("Initializing Memory Layer...")
memory = MemoryLayer()

# Test 1: Add memories with rich, meaningful content
print("\n=== Test 1: Adding memories with rich content ===")
user_id = "user_123"

messages = [
    {
        "role": "user",
        "content": "Hi, I'm John. I'm a 35-year-old software engineer living in San Francisco."
    },
    {
        "role": "assistant", 
        "content": "Hello John! Nice to meet you. How can I help you today?"
    },
    {
        "role": "user",
        "content": "I love playing guitar and hiking on weekends. I also enjoy reading science fiction novels."
    }
]

print(f"Adding conversation for user: {user_id}")
result = memory.memory.add(messages, user_id=user_id)
print(f"Add result: {result}")

# Test 2: Get all memories
print(f"\n=== Test 2: Retrieving memories for {user_id} ===")
memories = memory.memory.get_all(user_id=user_id)
print(f"Number of memories: {len(memories) if isinstance(memories, list) else 0}")
print(f"Memories: {memories}")

# Test 3: Search memories
print(f"\n=== Test 3: Searching memories ===")
search_results = memory.memory.search("What are John's hobbies?", user_id=user_id)
print(f"Search results: {search_results}")

print("\n=== Test Complete ===")

