# Agent Memory Manager - Streamlit App

A comprehensive Streamlit application for managing AI agent memories using mem0ai with semantic search capabilities.

## Features

### 🎯 Core Functionality

1. **Add Memory**
   - Store new memories with text content
   - Associate memories with User ID, Agent ID, or Run ID
   - Add custom metadata (category, priority, source, tags)
   - Automatic timestamping

2. **Search Memories**
   - Semantic search using natural language queries
   - Filter by User ID, Agent ID, or Run ID
   - Configurable result limits
   - Relevance scoring

3. **View All Memories**
   - Browse all stored memories
   - Apply identity filters
   - Quick edit/delete actions
   - Expandable metadata views

4. **Update/Delete Operations**
   - Update existing memory content
   - Delete individual memories
   - Bulk delete with filters
   - Safety confirmations for destructive operations

5. **Memory History**
   - View change history for specific memories
   - Track memory evolution over time

## Installation

1. Make sure you have the required dependencies:
```bash
pip install streamlit mem0ai
```

2. Ensure the `test_memory.py` module is in the same directory

3. Set up your OpenAI API configuration (already configured in `test_memory.py`)

## Usage

### Running the App

From the `src/memory` directory:

```bash
streamlit run memory_manager_app.py
```

Or from the project root:

```bash
streamlit run src/memory/memory_manager_app.py
```

The app will open in your default browser at `http://localhost:8501`

### Using Identity Filters

In the sidebar, you can set:
- **User ID**: Filter memories for a specific user
- **Agent ID**: Filter memories for a specific agent
- **Run ID**: Filter memories for a specific session/run

These filters apply globally across all operations.

## Interface Guide

### Tab 1: Add Memory
1. Enter memory content in the text area
2. Optionally specify User ID, Agent ID, Run ID
3. Add metadata:
   - Category (e.g., "preferences", "facts")
   - Priority (low, medium, high)
   - Source (e.g., "user_input", "api")
   - Tags (comma-separated)
4. Click "Add Memory"

### Tab 2: Search Memories
1. Enter a natural language search query
2. Set maximum number of results
3. Click "Search"
4. View results with relevance scores

### Tab 3: View All Memories
1. Set any filters in the sidebar
2. Set result limit
3. Click "Load Memories"
4. Use quick actions:
   - 📝 Edit: Loads memory into Update tab
   - 🗑️ Delete: Immediately deletes the memory

### Tab 4: Update/Delete
**Update Memory:**
1. Enter Memory ID (or use Edit button from View tab)
2. Enter new content
3. Specify identifiers
4. Click "Update Memory"

**Delete Single Memory:**
1. Enter Memory ID
2. Specify identifiers
3. Click "Delete Memory"

**Delete All Memories:**
1. Specify at least one filter (User/Agent/Run ID)
2. Check the confirmation box
3. Click "Delete All Memories"

### Tab 5: Memory History
1. Enter Memory ID
2. Specify identifiers
3. Click "Get History"
4. View all versions and changes

## Configuration

The app uses the configuration from `MemoryLayer` class:
- **LLM Provider**: OpenAI (via Telenav API)
- **Model**: gpt-4o
- **Embedder**: ailab-embedding
- **Vector Store**: Milvus (local database)
- **Temperature**: 0.7
- **Max Tokens**: 2000

## Tips & Best Practices

1. **Use Meaningful IDs**: Assign clear User/Agent/Run IDs for easier filtering
2. **Add Metadata**: Rich metadata makes memories more discoverable
3. **Regular Cleanup**: Periodically delete obsolete memories
4. **Semantic Search**: Use natural language questions for better search results
5. **Test Filters**: Use the Statistics section to verify filter results

## Troubleshooting

### App Won't Start
- Ensure `test_memory.py` is in the same directory
- Check that all dependencies are installed
- Verify OpenAI API configuration

### Search Not Working
- Ensure memories have been added
- Try broader search queries
- Check identity filters aren't too restrictive

### Memory Not Found
- Verify Memory ID is correct
- Check that User/Agent/Run IDs match
- Use "View All Memories" to browse available memories

## Architecture

```
memory_manager_app.py
├── Initialization
│   └── MemoryLayer (from test_memory.py)
├── Sidebar
│   ├── Identity Filters
│   └── Statistics
└── Main Tabs
    ├── Add Memory
    ├── Search Memories
    ├── View All Memories
    ├── Update/Delete
    └── Memory History
```

## Example Workflow

1. **Add a memory** about user preferences:
   ```
   Content: "User prefers Python for backend and React for frontend"
   User ID: user_123
   Category: preferences
   Tags: programming, stack
   ```

2. **Search for it**:
   ```
   Query: "What does the user prefer for development?"
   ```

3. **Update it** with more details:
   ```
   New Content: "User prefers Python with FastAPI for backend and React with TypeScript for frontend"
   ```

4. **View history** to see the changes

## Future Enhancements

- Export memories to JSON/CSV
- Import memories from files
- Advanced filtering options
- Memory analytics and insights
- Batch operations
- Memory similarity analysis

## Support

For issues or questions, refer to:
- mem0ai documentation: https://docs.mem0.ai/
- Streamlit documentation: https://docs.streamlit.io/

---

**Version**: 1.0.0  
**Last Updated**: October 13, 2025

