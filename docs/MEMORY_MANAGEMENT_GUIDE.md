# Agent Memory Management System

Complete guide for the Agent Memory Management implementation using mem0ai and Streamlit.

## 📋 Overview

This memory management system provides both a **Streamlit web interface** and **programmatic API** for managing AI agent memories with semantic search capabilities. Built on top of mem0ai, it enables persistent storage and retrieval of contextual information across user sessions, agent interactions, and processing runs.

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Memory Management Layer                   │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌─────────────────┐              ┌────────────────────┐    │
│  │   Streamlit UI  │              │  Programmatic API  │    │
│  │  (Web Interface)│              │  (Python Module)   │    │
│  └────────┬────────┘              └─────────┬──────────┘    │
│           │                                  │               │
│           └──────────────┬───────────────────┘               │
│                          │                                   │
│                  ┌───────▼────────┐                          │
│                  │  MemoryLayer   │                          │
│                  │  (test_memory) │                          │
│                  └───────┬────────┘                          │
│                          │                                   │
│                  ┌───────▼────────┐                          │
│                  │    mem0ai      │                          │
│                  └───────┬────────┘                          │
│                          │                                   │
│        ┌─────────────────┼─────────────────┐                │
│        │                 │                 │                │
│  ┌─────▼─────┐   ┌──────▼──────┐   ┌──────▼──────┐         │
│  │  OpenAI   │   │  Embeddings │   │   Milvus    │         │
│  │ (GPT-4o)  │   │   (ailab)   │   │ Vector DB   │         │
│  └───────────┘   └─────────────┘   └─────────────┘         │
│                                                               │
└─────────────────────────────────────────────────────────────┘
```

## 📁 File Structure

```
demo-risk-factor-agent/
├── src/
│   └── memory/
│       ├── test_memory.py              # Core memory layer implementation
│       ├── memory_manager_app.py       # Streamlit web application
│       ├── demo_memory_usage.py        # Programmatic usage examples
│       └── README_MEMORY_APP.md        # App-specific documentation
├── run_memory_app.sh                   # Quick launcher script
├── docs/
│   └── MEMORY_MANAGEMENT_GUIDE.md      # This file
└── milvus.db                           # Local vector database
```

## 🚀 Quick Start

### Option 1: Run the Streamlit App

From the project root:

```bash
# Make the launcher executable (first time only)
chmod +x run_memory_app.sh

# Launch the app
./run_memory_app.sh
```

Or manually:

```bash
cd src/memory
streamlit run memory_manager_app.py
```

The app will open at `http://localhost:8501`

### Option 2: Use Programmatically

Run the demo script:

```bash
cd src/memory
python demo_memory_usage.py
```

Or use in your own code:

```python
from src.memory.test_memory import MemoryLayer

# Initialize
memory = MemoryLayer()

# Add a memory
result = memory.add_memory(
    text="User prefers low-risk insurance options",
    user_id="user_123",
    metadata={"category": "preferences"}
)

# Search memories
results = memory.search_memories(
    query="What are the user's insurance preferences?",
    user_id="user_123"
)
```

## 🎯 Key Features

### 1. Memory Operations

#### Add Memory
Store new contextual information with:
- Text content (required)
- User/Agent/Run identifiers
- Custom metadata
- Automatic timestamping

#### Search Memory
Semantic search using natural language:
- Context-aware retrieval
- Relevance scoring
- Filtered by identifiers
- Configurable result limits

#### Update Memory
Modify existing memories:
- Change content
- Update metadata
- Maintain history (if supported)

#### Delete Memory
Remove memories:
- Single memory deletion
- Bulk deletion with filters
- Safety confirmations

### 2. Identity Management

Three levels of identity tracking:

1. **User ID**: Identifies the end user
   - Example: `user_123`, `john_doe`
   - Use case: User-specific preferences and history

2. **Agent ID**: Identifies the AI agent
   - Example: `risk_assessment_agent`, `claims_processor`
   - Use case: Agent-specific learned information

3. **Run ID**: Identifies a processing session
   - Example: `run_20251013_143022`, `session_abc123`
   - Use case: Session-specific context

### 3. Metadata Support

Attach structured metadata to memories:

```python
metadata = {
    "category": "driving_history",
    "priority": "high",
    "source": "user_application",
    "tags": ["safe_driver", "long_term"],
    "confidence": 0.95,
    "timestamp": "2025-10-13T14:30:22"
}
```

## 💡 Use Cases

### Use Case 1: Insurance Risk Assessment

```python
# Store applicant information
memory.add_memory(
    text="Applicant has 15 years of safe driving with no claims",
    user_id="applicant_456",
    agent_id="risk_assessment_agent",
    metadata={"category": "driving_history", "risk_score": "low"}
)

# Later, retrieve relevant information
results = memory.search_memories(
    query="What is the driving history of this applicant?",
    user_id="applicant_456",
    agent_id="risk_assessment_agent"
)
```

### Use Case 2: Conversational Context

```python
# Store conversation context
memory.add_memory(
    text="User asked about comprehensive coverage for a 2020 Honda Accord",
    user_id="user_789",
    run_id="conversation_001",
    metadata={"intent": "coverage_inquiry", "vehicle": "Honda Accord"}
)

# Retrieve context in next interaction
context = memory.search_memories(
    query="What was the user asking about?",
    user_id="user_789",
    run_id="conversation_001"
)
```

### Use Case 3: Agent Learning

```python
# Agent stores learned patterns
memory.add_memory(
    text="Users in zip code 94085 typically prefer comprehensive coverage",
    agent_id="recommendation_agent",
    metadata={"pattern_type": "regional_preference", "confidence": 0.87}
)

# Agent retrieves patterns for recommendations
patterns = memory.search_memories(
    query="What are the coverage preferences in this area?",
    agent_id="recommendation_agent"
)
```

## 🔧 Configuration

### Memory Layer Configuration

Located in `test_memory.py`:

```python
config = {
    "llm": {
        "provider": "openai",
        "config": {
            "model": "gpt-4o",
            "temperature": 0.7,
            "max_tokens": 2000,
            "openai_base_url": "https://us-ailab-api.telenav.com/v1",
            "api_key": "sk-nIDrG5iv1XNwFzRcaAzDgg"
        }
    },
    "embedder": {
        "provider": "openai",
        "config": {
            "model": "ailab-embedding",
            "openai_base_url": "https://us-ailab-api.telenav.com/v1"
        }
    },
    "vector_store": {
        "provider": "milvus",
        "config": {
            "collection_name": "quickstart_mem0_with_milvus",
            "embedding_model_dims": "1536",
            "url": "./milvus.db"
        }
    }
}
```

### Customization Options

You can customize:
- **LLM Provider**: OpenAI, Groq, Ollama, etc.
- **Model**: Any supported model
- **Temperature**: Control randomness (0.0-1.0)
- **Max Tokens**: Response length limit
- **Vector Store**: Milvus, Pinecone, Qdrant, etc.
- **Embedding Model**: Different embedding models

## 📊 Streamlit App Features

### Dashboard Layout

```
┌─────────────────────────────────────────────────────────┐
│  🧠 Agent Memory Manager                                │
├───────────────┬─────────────────────────────────────────┤
│   Sidebar     │  Main Content Area                      │
│               │                                          │
│ Configuration │  ┌───────────────────────────────────┐  │
│ - User ID     │  │  Tabs:                            │  │
│ - Agent ID    │  │  • Add Memory                     │  │
│ - Run ID      │  │  • Search Memories                │  │
│               │  │  • View All Memories              │  │
│ Statistics    │  │  • Update/Delete                  │  │
│ - Total Count │  │  • Memory History                 │  │
│ - Refresh     │  └───────────────────────────────────┘  │
└───────────────┴─────────────────────────────────────────┘
```

### Tab Functions

1. **Add Memory Tab**
   - Rich text input
   - Identity assignment
   - Metadata editor
   - Success/error feedback

2. **Search Tab**
   - Natural language queries
   - Result limiting
   - Relevance scores
   - Expandable details

3. **View All Tab**
   - Filtered listings
   - Quick actions
   - Metadata display
   - Pagination support

4. **Update/Delete Tab**
   - Single memory updates
   - Single memory deletion
   - Bulk deletion (with confirmation)
   - Memory ID lookup

5. **History Tab**
   - Version tracking
   - Change history
   - Temporal navigation

## 🔍 Advanced Features

### Semantic Search

The system uses semantic search, not keyword matching:

```python
# Instead of keyword search
query = "safe driver no accidents"  # ❌ Less effective

# Use natural language
query = "What is the user's driving safety record?"  # ✅ Better
```

### Context Retrieval

Retrieve relevant context for agent reasoning:

```python
# Get context for decision making
context = memory.search_memories(
    query="What information do we have about this user's risk profile?",
    user_id="user_123",
    agent_id="risk_assessment_agent",
    limit=5
)

# Use context in agent prompt
prompt = f"""
Based on the following context:
{context}

Assess the insurance risk for this applicant.
"""
```

### Memory Deduplication

mem0ai automatically handles similar memories:
- Detects duplicate information
- Merges related memories
- Maintains consistency

## 🛡️ Best Practices

### 1. Identity Management
- ✅ Use consistent ID formats
- ✅ Document your ID schema
- ✅ Include timestamps in Run IDs
- ❌ Don't use personally identifiable information in IDs

### 2. Memory Content
- ✅ Store factual, specific information
- ✅ Use complete sentences
- ✅ Include relevant context
- ❌ Don't store sensitive personal data without proper handling

### 3. Metadata Usage
- ✅ Add rich, structured metadata
- ✅ Use consistent category names
- ✅ Include timestamps
- ❌ Don't overload with unnecessary fields

### 4. Search Queries
- ✅ Use natural language questions
- ✅ Be specific about what you need
- ✅ Include context in queries
- ❌ Don't use keyword-style searches

### 5. Cleanup
- ✅ Regularly delete obsolete memories
- ✅ Use Run IDs for session-based cleanup
- ✅ Archive important historical data
- ❌ Don't keep unlimited memories indefinitely

## 🔒 Security Considerations

### API Keys
- Store API keys in environment variables
- Don't commit keys to version control
- Rotate keys regularly

### Data Privacy
- Anonymize personal information
- Implement access controls
- Follow data retention policies
- Comply with GDPR/CCPA requirements

### Vector Database
- Secure Milvus instance
- Use authentication
- Encrypt sensitive data
- Regular backups

## 🧪 Testing

### Unit Tests

```python
import pytest
from src.memory.test_memory import MemoryLayer

def test_add_memory():
    memory = MemoryLayer()
    result = memory.add_memory(
        text="Test memory",
        user_id="test_user"
    )
    assert result is not None
    
def test_search_memory():
    memory = MemoryLayer()
    results = memory.search_memories(
        query="test",
        user_id="test_user"
    )
    assert isinstance(results, list)
```

### Integration Tests

Run the demo script:
```bash
python src/memory/demo_memory_usage.py
```

## 📈 Performance Optimization

### Tips for Faster Operations

1. **Use Appropriate Limits**
   ```python
   # Don't retrieve everything
   memory.get_memories(user_id="user_123")  # ❌ Slow
   
   # Limit results
   memory.get_memories(user_id="user_123", limit=20)  # ✅ Fast
   ```

2. **Batch Operations**
   ```python
   # Add multiple memories in a loop with delays
   for text in memory_texts:
       memory.add_memory(text, user_id="user_123")
       time.sleep(0.5)  # Avoid rate limits
   ```

3. **Effective Filtering**
   ```python
   # Use specific filters
   memory.search_memories(
       query="risk assessment",
       user_id="user_123",
       agent_id="risk_agent",
       run_id="current_run"
   )
   ```

## 🐛 Troubleshooting

### Common Issues

**Issue**: Memory not found after adding
- **Solution**: Check identifier spelling and consistency

**Issue**: Search returns no results
- **Solution**: Use natural language, broaden query, check filters

**Issue**: Slow performance
- **Solution**: Use limits, optimize filters, check network

**Issue**: Initialization fails
- **Solution**: Verify API keys, check Milvus setup, review config

**Issue**: Duplicate memories
- **Solution**: mem0ai handles this automatically, check dedup settings

## 📚 API Reference

### MemoryLayer Class

#### `__init__(llm_provider, temperature, max_tokens, **kwargs)`
Initialize the memory layer.

#### `add_memory(text, user_id, agent_id, run_id, metadata)`
Add a new memory to the system.

#### `get_memories(user_id, agent_id, run_id, limit)`
Retrieve all memories matching the filters.

#### `search_memories(query, user_id, agent_id, run_id, limit)`
Search memories using semantic search.

#### `update_memory(memory_id, text, user_id, agent_id, run_id, metadata)`
Update an existing memory.

#### `delete_memory(memory_id, user_id, agent_id, run_id)`
Delete a specific memory.

#### `delete_all_memories(user_id, agent_id, run_id)`
Delete all memories matching the filters.

#### `get_memory_history(memory_id, user_id, agent_id, run_id)`
Get the change history for a memory.

## 🔗 Resources

- **mem0ai Documentation**: https://docs.mem0.ai/
- **Streamlit Documentation**: https://docs.streamlit.io/
- **Milvus Documentation**: https://milvus.io/docs
- **OpenAI API Reference**: https://platform.openai.com/docs/api-reference

## 🎓 Learning Path

1. **Beginner**: Run the Streamlit app, explore the UI
2. **Intermediate**: Run `demo_memory_usage.py`, modify examples
3. **Advanced**: Integrate into your agents, customize configuration
4. **Expert**: Extend functionality, optimize performance, scale deployment

## 📝 License

This implementation is part of the demo-risk-factor-agent project.

---

**Version**: 1.0.0  
**Last Updated**: October 13, 2025  
**Maintainer**: Demo Risk Factor Agent Team

