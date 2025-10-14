# 🧠 Memory-Based Product Definition Agent

> Transform your product definition agent from stateless to stateful - learn, grow, and improve with every interaction!

[![Status](https://img.shields.io/badge/Status-Production%20Ready-success)]()
[![Tests](https://img.shields.io/badge/Tests-All%20Passing-success)]()
[![Compatibility](https://img.shields.io/badge/Backward%20Compatible-100%25-success)]()
[![Pattern](https://img.shields.io/badge/Pattern-mem0-blue)]()

---

## 🎯 What Is This?

A **memory-enhanced AI agent** that manages insurance product definitions and risk factors. Unlike traditional stateless agents, this agent:

- 🧠 **Remembers** across sessions
- 📈 **Learns** from interactions  
- 🔍 **Searches** semantically
- 💬 **Answers** natural language questions
- 🌱 **Grows** smarter over time

Built following the [mem0 pattern](https://mem0.ai/blog/memory-in-agents-what-why-and-how) for intelligent agents.

---

## ⚡ Quick Start (5 Minutes)

### 1. Load Knowledge
```bash
./load_risk_knowledge.sh
```

### 2. Run App
```bash
./run_product_agent.sh
```

### 3. Ask Questions
Open `http://localhost:8502` and try:
```
What are the driver-related risk factors?
```

**That's it!** 🎉

---

## 🌟 Key Features

### Before: Traditional Agent
```python
agent = ProductDefinitionAgent()
product = agent.get_product_definition("Monthly-Comfort")
# ❌ No memory
# ❌ No learning
# ❌ No semantic search
```

### After: Memory-Based Agent
```python
agent = ProductDefinitionAgent(use_memory=True)

# ✅ Ask questions in natural language
answer = agent.answer_question("What are driver factors?")

# ✅ Search semantically
results = agent.query_knowledge("factors about age")

# ✅ Learns from interactions
agent.learn_from_interaction("query", {...})

# ✅ PLUS all original methods still work!
product = agent.get_product_definition("Monthly-Comfort")
```

---

## 📊 What's Included

### Core Components
- ✅ **Memory-Based Agent** (`product_definition_agent.py`)
- ✅ **Knowledge Loader** (`load_risk_factor_knowledge.py`)
- ✅ **Web Interface** (`streamlit_product_agent.py`)
- ✅ **Demo Script** (`demo_product_agent.py`)
- ✅ **Integration Tests** (`test_memory_agent_integration.py`)

### Documentation
- 📘 **Full Guide** (`MEMORY_BASED_PRODUCT_AGENT_README.md`)
- 🚀 **Quick Start** (`QUICKSTART_MEMORY_AGENT.md`)
- 🔧 **Technical Details** (`REFACTORING_SUMMARY.md`)
- 📦 **Delivery Summary** (`DELIVERY_SUMMARY.md`)

### Knowledge Base
- 📚 **79 Risk Factors** from `risk_factor_point_tables.md`
- 📋 **70 Factor Names** from `risk_factor_list_knowlege.md`
- 🎯 **3 Products** (Monthly-Comfort, Economy, Turbo)
- 🏷️ **13 Coverage Types** (BI, PD, COMP, COLL, etc.)

---

## 🎨 Streamlit App Features

### 4 Interactive Tabs

**1. Ask Questions** 💬
- Natural language Q&A
- Sample questions provided
- Context-aware answers

**2. Search Knowledge** 🔍
- Semantic search
- Relevance scoring
- Metadata display

**3. Product Definitions** 📋
- Complete product details
- Risk factors with weights
- Coverage options

**4. Learning Dashboard** 📊
- Memory statistics
- Learning metrics
- Usage insights

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────┐
│         User Interfaces                     │
│                                             │
│  ┌─────────┐  ┌──────────┐  ┌──────────┐  │
│  │Streamlit│  │Python API│  │CLI Demo  │  │
│  └─────────┘  └──────────┘  └──────────┘  │
└──────────────────┬──────────────────────────┘
                   │
┌──────────────────▼──────────────────────────┐
│     ProductDefinitionAgent                  │
│     (Memory-Based)                          │
│                                             │
│  New Methods:          Original Methods:    │
│  • query_knowledge()   • get_product_def()  │
│  • answer_question()   • get_risk_factors() │
│  • search_factors()    • get_rules()        │
│  • learn_interaction() • validate()         │
└──────────┬────────────────────┬─────────────┘
           │                    │
┌──────────▼──────────┐  ┌──────▼──────────┐
│   Memory Layer      │  │Product Definitions│
│   (Persistent)      │  │  (Hardcoded)     │
│                     │  │                  │
│ • Semantic Search   │  │ • 3 Products     │
│ • Embeddings        │  │ • Risk Factors   │
│ • Milvus Storage    │  │ • Rules          │
│ • Learning          │  │ • Coverage       │
└─────────────────────┘  └──────────────────┘
```

---

## 📚 Documentation Map

| Want to... | Read this |
|------------|-----------|
| **Get started quickly** | `QUICKSTART_MEMORY_AGENT.md` |
| **Learn all features** | `MEMORY_BASED_PRODUCT_AGENT_README.md` |
| **Understand changes** | `REFACTORING_SUMMARY.md` |
| **See implementation** | `MEMORY_AGENT_IMPLEMENTATION.md` |
| **Check delivery** | `DELIVERY_SUMMARY.md` |

---

## 💻 Usage Examples

### Example 1: Natural Language Q&A

```python
from src.agents.product_definition_agent import ProductDefinitionAgent

agent = ProductDefinitionAgent(use_memory=True)

# Ask questions
answer = agent.answer_question(
    "What are the discount factors available?"
)
print(answer)

# Output: Based on my knowledge:
# 1. Continuous Insurance Discount - applies to BI, PD, COMP...
# 2. Three Year Safe Driving Discount - eligibility based on...
# 3. Home/Mobile Home Owner Discount - prior BI level...
```

### Example 2: Semantic Search

```python
# Search by meaning, not keywords
results = agent.query_knowledge(
    "factors related to how old the driver is",
    limit=5
)

for result in results:
    print(f"{result['text']} (score: {result['score']:.4f})")

# Output: Driver_Age_Risk_Factor: Driver Age, BI/PD Points...
```

### Example 3: Learning

```python
# Agent learns from every interaction
agent.answer_question("What is Monthly-Comfort?")

# This interaction is recorded:
# - What was asked
# - What was answered
# - When it happened

# Future responses improve based on patterns
```

---

## 🧪 Testing

### Run Integration Tests

```bash
python test_memory_agent_integration.py
```

### Expected Output
```
======================================================================
TEST SUMMARY
======================================================================
Backward Compatibility............................ ✅ PASSED
Memory Initialization............................. ✅ PASSED
New Methods....................................... ✅ PASSED
Hybrid Usage...................................... ✅ PASSED
======================================================================
🎉 ALL TESTS PASSED!
```

---

## 📈 Knowledge Base Statistics

| Category | Count | Examples |
|----------|-------|----------|
| **Driver Factors** | 19 | Age, Class, Training, Record |
| **Vehicle Factors** | 13 | Age, Location, Mileage, Type |
| **Discount Factors** | 11 | Continuous, Safe Driver, Home Owner |
| **Coverage Types** | 13 | BI, PD, COMP, COLL, MED, UM, UIM |
| **Products** | 3 | Monthly-Comfort, Economy, Turbo |

**Total Knowledge Items:** 79+ risk factors, 70+ factor names, 4 domain concepts

---

## 🔍 How Memory Works

### 1. Load Knowledge (One-Time)
```bash
./load_risk_knowledge.sh
```
Loads 79 risk factors into persistent memory with semantic embeddings.

### 2. Query Knowledge
```python
results = agent.query_knowledge("driver factors")
```
Searches using semantic similarity (meaning-based, not keyword-based).

### 3. Learn from Usage
```python
agent.answer_question("...")
```
Every interaction is recorded to improve future responses.

### 4. Grow Over Time
The more you use it, the smarter it gets! 🌱

---

## 🎯 Use Cases

### 1. Product Information Hub
Answer questions about products and risk factors for:
- Sales teams
- Underwriters
- Product managers
- Compliance

### 2. Development Assistant
Help developers understand:
- Risk factor relationships
- Product configurations
- Assessment rules
- Coverage mappings

### 3. Training Tool
Onboard new employees with:
- Interactive Q&A
- Searchable knowledge
- Real-world examples
- Learning by doing

### 4. Knowledge Management
Maintain and grow:
- Product definitions
- Risk factor catalog
- Business rules
- Domain knowledge

---

## 🚀 Deployment

### Development
```bash
# Load knowledge
./load_risk_knowledge.sh

# Run app
./run_product_agent.sh
```

### Production
```bash
# Set environment
export OPENAI_API_KEY=your_key

# Load knowledge (one-time)
./load_risk_knowledge.sh

# Run with production settings
streamlit run src/streamlit_product_agent.py \
    --server.port 8502 \
    --server.headless true
```

---

## 🛠️ Requirements

- Python 3.10+
- OpenAI API key (or Telenav API key)
- Packages: `streamlit`, `openai`, `mem0`, `milvus-lite`

```bash
pip install -r requirements.txt
```

---

## 🤝 Contributing

### To Extend

1. **Add New Knowledge**
   ```python
   memory_layer.add_memory(
       text="Your new knowledge",
       metadata={"category": "...", "priority": "high"}
   )
   ```

2. **Add New Products**
   Edit `product_definition_agent.py` and add product definitions.

3. **Customize Learning**
   Modify `learn_from_interaction()` to track custom patterns.

---

## 📊 Performance

| Operation | Time | Notes |
|-----------|------|-------|
| Initialize Agent | 1-2s | First time |
| Query Knowledge | 1-3s | Includes search |
| Answer Question | 2-4s | Full pipeline |
| Load Knowledge | 30-60s | One-time setup |

---

## ✅ Production Ready

- ✅ **Error Handling** - Graceful degradation
- ✅ **Backward Compatible** - 100% compatible
- ✅ **User Isolation** - Multi-user support
- ✅ **Logging** - Comprehensive logs
- ✅ **Testing** - Integration tests
- ✅ **Documentation** - 5 detailed guides
- ✅ **Monitoring** - Memory statistics

---

## 🎓 Learn More

### References
- [mem0 - Memory in Agents](https://mem0.ai/blog/memory-in-agents-what-why-and-how)
- [Strands Agents - Memory Example](https://strandsagents.com/latest/documentation/docs/examples/python/memory_agent/)

### Related Files
- `src/memory/test_memory.py` - Memory layer implementation
- `src/memory/demo_memory_usage.py` - Memory usage examples
- `docs/insurance_risk_factor_agent/` - Business rules

---

## 🎉 Success!

You now have a **memory-based agent** that:
- ✅ Stores knowledge persistently
- ✅ Learns from interactions
- ✅ Answers questions naturally
- ✅ Searches semantically
- ✅ Grows over time

**Start using it now:**
```bash
./load_risk_knowledge.sh && ./run_product_agent.sh
```

---

## 📞 Support

### Common Issues

**Problem:** Memory not loading  
**Solution:** Check `OPENAI_API_KEY` and run `./load_risk_knowledge.sh`

**Problem:** No results in search  
**Solution:** Reload knowledge with `./load_risk_knowledge.sh`

**Problem:** App won't start  
**Solution:** Install dependencies: `pip install -r requirements.txt`

---

## 📄 License

See project LICENSE file.

---

**Built with ❤️ using:**
- Python 3.10+
- Streamlit
- mem0
- OpenAI
- Milvus

**Pattern:** [mem0.ai](https://mem0.ai/) + [Strands Agents](https://strandsagents.com/)  
**Status:** ✅ Production Ready  
**Last Updated:** October 14, 2025


