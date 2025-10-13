# 🚀 Quick Start Guide - Agent Memory Manager

Get started with the Agent Memory Manager in 3 simple steps!

## Step 1: Launch the App

```bash
# From project root
./run_memory_app.sh
```

Or:

```bash
cd src/memory
streamlit run memory_manager_app.py
```

The app will open at **http://localhost:8501** 🎉

## Step 2: Try the Demo

Experience all features programmatically:

```bash
cd src/memory
python demo_memory_usage.py
```

This will demonstrate:
- Adding memories with metadata
- Semantic search
- Retrieving all memories
- Updating content
- Viewing history
- Context-aware search
- Cleanup operations

## Step 3: Integrate into Your Code

```python
from src.memory.test_memory import MemoryLayer

# Initialize
memory = MemoryLayer()

# Add a memory
memory.add_memory(
    text="User prefers low-risk insurance options",
    user_id="user_123",
    metadata={"category": "preferences", "priority": "high"}
)

# Search with natural language
results = memory.search_memories(
    query="What are the user's insurance preferences?",
    user_id="user_123",
    limit=5
)

# Use the results
for result in results:
    print(f"Memory: {result['memory']}")
    print(f"Score: {result['score']}")
```

## Common Use Cases

### Use Case 1: Store User Preferences
```python
memory.add_memory(
    text="User prefers comprehensive coverage with $500 deductible",
    user_id="user_456",
    metadata={"category": "preferences"}
)
```

### Use Case 2: Track Agent Decisions
```python
memory.add_memory(
    text="Approved premium of $1,200 based on low risk profile",
    user_id="user_456",
    agent_id="pricing_agent",
    metadata={"category": "decision", "confidence": 0.95}
)
```

### Use Case 3: Session Context
```python
run_id = f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

memory.add_memory(
    text="User started quote process for 2020 Honda Accord",
    user_id="user_456",
    run_id=run_id,
    metadata={"category": "session_event"}
)
```

## Streamlit App Features

### 1. Add Memory Tab
- Enter memory content
- Assign User/Agent/Run IDs
- Add metadata (category, priority, tags)
- Automatic timestamping

### 2. Search Tab
- Natural language queries
- Semantic search with relevance scores
- Filter by identifiers
- View detailed results

### 3. View All Tab
- Browse all memories
- Apply filters
- Quick edit/delete
- Metadata viewer

### 4. Update/Delete Tab
- Edit memory content
- Delete individual memories
- Bulk delete with confirmation

### 5. History Tab
- View change history
- Track additions and updates
- Temporal navigation

## Tips for Success

### ✅ Do This:
- Use descriptive User/Agent/Run IDs
- Add rich metadata to memories
- Use natural language for searches
- Clean up obsolete memories regularly

### ❌ Avoid This:
- Don't use keyword searches
- Don't store sensitive data without encryption
- Don't skip metadata for important memories
- Don't keep unlimited memories

## Example Workflow

```python
# 1. Initialize
memory = MemoryLayer()

# 2. Store application data
memory.add_memory(
    text="Applicant: 15 years safe driving, no claims",
    user_id="applicant_789",
    agent_id="risk_agent",
    metadata={"category": "driving_history", "risk": "low"}
)

# 3. Later, retrieve context for decision
context = memory.search_memories(
    query="What is the driving history?",
    user_id="applicant_789",
    agent_id="risk_agent"
)

# 4. Use context in your agent
for item in context:
    print(f"Found: {item['memory']} (Score: {item['score']:.2f})")

# 5. Clean up when done
memory.delete_all_memories(run_id="current_session")
```

## Architecture

```
Your Application
     │
     ├─→ Streamlit UI (memory_manager_app.py)
     │   └─→ Interactive web interface
     │
     └─→ Python API (test_memory.py)
         └─→ MemoryLayer
             ├─→ mem0ai
             │   ├─→ OpenAI GPT-4o (reasoning)
             │   ├─→ ailab-embedding (vectors)
             │   └─→ Milvus (storage)
             │
             └─→ Your Agent Code
```

## Configuration

Default settings (in `test_memory.py`):
- **LLM**: GPT-4o via Telenav API
- **Embeddings**: ailab-embedding
- **Vector DB**: Milvus (local: `./milvus.db`)
- **Temperature**: 0.7
- **Max Tokens**: 2000

## Troubleshooting

**App won't start?**
```bash
pip install streamlit mem0ai
```

**Import errors?**
```bash
# Make sure you're in the correct directory
cd src/memory
```

**No search results?**
- Use natural language questions
- Check your filters aren't too restrictive
- Verify memories were added successfully

## Documentation

- **This Guide**: `src/memory/QUICKSTART.md`
- **Full Guide**: `docs/MEMORY_MANAGEMENT_GUIDE.md`
- **App Docs**: `src/memory/README_MEMORY_APP.md`
- **Summary**: `MEMORY_APP_SUMMARY.md`
- **Technical Fixes**: `src/memory/FIXES_APPLIED.md`

## Support

Having issues? Check:
1. All dependencies installed
2. Correct directory (`src/memory`)
3. API keys configured
4. Milvus database accessible

## Next Steps

1. ✅ Launch the Streamlit app
2. ✅ Run the demo script
3. ✅ Try adding your own memories
4. ✅ Integrate into your agents
5. ✅ Customize for your use case

---

**Ready to start?** Run: `./run_memory_app.sh` 🚀

**Questions?** Check the docs or run `python demo_memory_usage.py` to see examples.

**Status**: Fully tested and working ✅

