# Quick Start: Memory-Based Product Definition Agent

## 🚀 Get Started in 3 Steps

This guide will help you set up and use the memory-based product definition agent in **less than 5 minutes**.

---

## Step 1: Load Knowledge (One-Time Setup)

Load risk factor knowledge into the agent's memory:

```bash
# Make scripts executable (if not already)
chmod +x load_risk_knowledge.sh run_product_agent.sh

# Load knowledge into memory
./load_risk_knowledge.sh
```

**What this does:**
- Loads 79 risk factor tables from markdown files
- Stores 70 risk factor names
- Adds product domain knowledge
- Creates semantic embeddings for search

**Time required:** ~30-60 seconds

**Output:**
```
📚 Loading Risk Factor Knowledge into Memory...
✅ Memory Layer initialized successfully
✅ Loaded overview knowledge
✅ Loaded 19 factors from Driver Factors
✅ Loaded 13 factors from Vehicle Factors
...
✨ Risk factor knowledge successfully loaded into memory!
```

---

## Step 2: Run the Streamlit App

Launch the interactive web interface:

```bash
./run_product_agent.sh
```

The app will open at `http://localhost:8502`

**What you'll see:**
- 4 tabs: Ask Questions, Search Knowledge, Product Definitions, Learning Dashboard
- Memory statistics in the sidebar
- Available products and quick actions

---

## Step 3: Try It Out!

### Example 1: Ask a Question

Navigate to the **"Ask Questions"** tab and try:

```
What are the driver-related risk factors?
```

**Response will include:**
- Knowledge from memory (semantic search results)
- Product definitions (if relevant)
- Context-aware information

### Example 2: Search Knowledge

Go to **"Search Knowledge"** tab and search:

```
discount factors
```

**You'll get:**
- Semantically relevant results
- Relevance scores
- Source metadata

### Example 3: View Product

In **"Product Definitions"** tab:
1. Select "Monthly-Comfort"
2. Click "Get Definition"
3. See risk factors, coverage options, and memory knowledge

---

## 📖 Sample Questions to Try

Copy and paste these into the app:

### About Risk Factors
```
What are the driver-related risk factors?
Tell me about discount factors
How many risk factors are there?
What factors affect vehicle premiums?
```

### About Products
```
What is the Monthly-Comfort product?
What coverage types are available?
Tell me about the Monthly-Economy product
What are the differences between products?
```

### About Coverage
```
What coverage types are supported?
Explain BI and PD coverage
What is comprehensive coverage?
Tell me about deductible options
```

### Specific Risk Factors
```
Explain the three-year claim-free discount
What is the Driver Age Risk Factor?
How does garaging location affect premium?
Tell me about the youthful driver discount
```

---

## 🧪 Test Without UI (Optional)

Run the demo script to test functionality:

```bash
python demo_product_agent.py
```

This will demonstrate:
1. Basic operations (without memory)
2. Memory operations
3. Question answering
4. Risk factor search
5. Learning capabilities
6. Product knowledge retrieval

---

## 🎯 Key Features to Explore

### 1. Memory-Based Intelligence
The agent remembers across sessions and learns from interactions.

**Try this:**
1. Ask: "What are driver factors?"
2. Close the app
3. Reopen and ask the same question
4. The agent remembers the context!

### 2. Semantic Search
Search by meaning, not keywords.

**Example:**
- Search: "factors related to how old the driver is"
- Finds: "Driver_Age_Risk_Factor" even without exact words

### 3. Learning
Every interaction is recorded.

**What gets learned:**
- Questions you ask
- Products you view
- Search patterns
- Validation results

### 4. Context-Aware Responses
Responses combine multiple sources:
- Memory knowledge (learned)
- Product definitions (configured)
- Usage patterns (observed)

---

## 📊 Understanding the Interface

### Sidebar
- **Memory Statistics**: Shows total memories and agent info
- **Available Products**: Quick list of products
- **Quick Actions**: Reload and view samples

### Tab 1: Ask Questions
- Natural language Q&A
- Sample questions available
- Shows timestamp for answers

### Tab 2: Search Knowledge
- Semantic search across memory
- Adjustable result limit
- Shows relevance scores and metadata

### Tab 3: Product Definitions
- Detailed product configurations
- Risk factors with weights
- Coverage options
- Additional memory knowledge

### Tab 4: Learning Dashboard
- Learning metrics
- Risk factor search
- Explanation of learning types
- Usage tips

---

## 🔧 Troubleshooting

### Problem: "Memory Not Enabled"

**Solution:**
```bash
# Check if memory layer is available
python -c "from src.memory.test_memory import MemoryLayer; print('OK')"

# If error, check OpenAI API key
echo $OPENAI_API_KEY

# Reload knowledge
./load_risk_knowledge.sh
```

### Problem: "No Results Found"

**Solution:**
```bash
# Reload knowledge
./load_risk_knowledge.sh

# Verify in app: Check Memory Statistics in sidebar
# Should show "Total Memories" > 0
```

### Problem: App Won't Start

**Solution:**
```bash
# Check dependencies
pip install streamlit openai mem0

# Try different port
streamlit run src/streamlit_product_agent.py --server.port 8503
```

---

## 📚 What's Happening Behind the Scenes?

### Knowledge Loading
```python
# 1. Load markdown files
with open('risk_factor_point_tables.md') as f:
    content = f.read()

# 2. Parse and structure
factors = parse_risk_factors(content)

# 3. Store in memory with embeddings
memory_layer.add_memory(
    text=factor_description,
    metadata={"category": "risk_factors", ...}
)

# 4. Create vector embeddings (automatic)
# Uses OpenAI to create semantic embeddings
```

### Question Answering
```python
# 1. User asks question
question = "What are driver factors?"

# 2. Semantic search in memory
results = memory.search_memories(query=question)

# 3. Combine with definitions
product_info = get_product_definition(...)

# 4. Generate context-aware answer
answer = combine_sources(results, product_info)

# 5. Learn from interaction
memory.add_memory(f"User asked: {question}")
```

---

## 🎓 Learning More

### Documentation
- Full README: `MEMORY_BASED_PRODUCT_AGENT_README.md`
- Architecture: See "Architecture" section in README
- API Reference: See "API Reference" section in README

### Code Examples
```python
# Initialize agent
from src.agents.product_definition_agent import ProductDefinitionAgent

agent = ProductDefinitionAgent(use_memory=True)

# Query knowledge
results = agent.query_knowledge("driver factors", limit=5)

# Answer questions
answer = agent.answer_question("What is Monthly-Comfort?")

# Search risk factors
factors = agent.search_risk_factors("discount")

# Learn from interactions
agent.learn_from_interaction("query", {
    "query": "...",
    "response": "..."
})
```

### References
- [mem0 Pattern](https://mem0.ai/blog/memory-in-agents-what-why-and-how)
- [Strands Agents Memory](https://strandsagents.com/latest/documentation/docs/examples/python/memory_agent/)

---

## 🚀 Next Steps

### 1. Experiment
- Try different questions
- Search for various terms
- View all products
- Monitor learning metrics

### 2. Extend
- Add new products (edit `product_definition_agent.py`)
- Load additional knowledge (create new loader script)
- Customize learning (modify `learn_from_interaction`)

### 3. Integrate
- Use in other agents (import `ProductDefinitionAgent`)
- Connect to existing systems
- Build on top of memory layer

---

## 💡 Pro Tips

### Tip 1: Better Questions
❌ "driver"  
✅ "What are the driver-related risk factors?"

More context = better answers!

### Tip 2: Use Semantic Search
Instead of exact keywords, describe what you're looking for:
- "factors about how old someone is" → finds "Driver_Age_Risk_Factor"
- "ways to save money on insurance" → finds discount factors

### Tip 3: Monitor Learning
Check the Learning Dashboard regularly to see:
- How many memories have been created
- What patterns are emerging
- Which topics are queried most

### Tip 4: Reload Knowledge
If you update the markdown files:
```bash
./load_risk_knowledge.sh  # Reload
./run_product_agent.sh    # Restart app
```

---

## ✅ Success Checklist

- [ ] Knowledge loaded successfully
- [ ] Streamlit app running
- [ ] Memory enabled (check sidebar)
- [ ] Can ask questions and get answers
- [ ] Can search knowledge
- [ ] Can view product definitions
- [ ] Learning dashboard shows statistics

---

## 🎉 You're Ready!

You now have a **memory-based agent** that:
- ✅ Stores knowledge persistently
- ✅ Learns from interactions
- ✅ Provides context-aware answers
- ✅ Searches semantically
- ✅ Grows over time

**Happy exploring!** 🚀

---

**Questions or Issues?**
- Check the full README: `MEMORY_BASED_PRODUCT_AGENT_README.md`
- Review troubleshooting section above
- Run demo: `python demo_product_agent.py`

