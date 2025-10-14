# Memory-Based Product Definition Agent

## Overview

This is a **memory-enhanced AI agent** that manages insurance product definitions, risk factors, and assessment rules. Unlike traditional stateless agents, this agent **learns and grows** with every interaction, following the [mem0 pattern](https://mem0.ai/blog/memory-in-agents-what-why-and-how) for building intelligent, persistent agents.

## 🌟 Key Features

### Memory-Based Intelligence
- **Persistent Knowledge**: Stores risk factor knowledge across sessions
- **Semantic Search**: Finds relevant information using meaning, not keywords
- **Learning Capability**: Records interactions and usage patterns
- **Context-Aware Responses**: Provides answers based on accumulated knowledge
- **Growing Knowledge Base**: Continuously expands understanding over time

### Core Capabilities
1. **Product Definition Management**
   - Manages multiple insurance products (Monthly-Comfort, Monthly-Economy, Monthly-Turbo)
   - Defines risk factors for each product
   - Maintains assessment rules and coverage options

2. **Risk Factor Knowledge**
   - 79+ risk factor tables organized by category
   - Driver, Vehicle, Household/Policy, Discount, and other factors
   - Detailed coverage mappings (BI, PD, COMP, COLL, etc.)

3. **Interactive Question Answering**
   - Natural language queries about risk factors and products
   - Context-aware responses using both definitions and memory
   - Learning from every interaction

## 🏗️ Architecture

### Components

```
┌─────────────────────────────────────────────────────────────┐
│                   Streamlit UI Layer                        │
│            (streamlit_product_agent.py)                     │
└────────────────────┬────────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────────┐
│          ProductDefinitionAgent (Memory-Based)              │
│         • Query Knowledge    • Learn from Interactions      │
│         • Search Risk Factors • Answer Questions            │
└────────────────────┬────────────────────────────────────────┘
                     │
         ┌───────────┴───────────┐
         │                       │
┌────────▼─────────┐   ┌────────▼──────────┐
│  MemoryLayer     │   │ Product Definitions│
│  (Persistent)    │   │   (Hardcoded)      │
│  • Semantic      │   │  • Risk Factors    │
│    Search        │   │  • Rules           │
│  • Storage       │   │  • Coverage        │
└──────────────────┘   └───────────────────┘
```

### Memory Types

Following the mem0 architecture, the agent uses multiple memory types:

| Memory Type | Purpose | Example |
|-------------|---------|---------|
| **Factual Memory** | Stores risk factor definitions and product knowledge | "Driver_Age_Risk_Factor applies to BI, PD coverages" |
| **Episodic Memory** | Records specific interactions | "User queried about discount factors on 2025-10-14" |
| **Semantic Memory** | Stores generalized knowledge | "Most queries are about driver-related risk factors" |

## 🚀 Getting Started

### Prerequisites

```bash
# Python 3.10+
# Virtual environment activated
source venv/bin/activate

# Required packages
pip install streamlit openai mem0
```

### Step 1: Load Knowledge into Memory

First, load the risk factor knowledge from markdown files into the memory system:

```bash
# Run the knowledge loader
./load_risk_knowledge.sh

# Or manually:
python src/agents/load_risk_factor_knowledge.py
```

This will load:
- **79 risk factor tables** from `risk_factor_point_tables.md`
- **70 risk factor names** from `risk_factor_list_knowlege.md`
- **Product domain knowledge** (products, coverage types, evaluation process)

### Step 2: Run the Streamlit App

```bash
# Run using the shell script
./run_product_agent.sh

# Or manually:
streamlit run src/streamlit_product_agent.py --server.port 8502
```

The app will be available at `http://localhost:8502`

## 📱 Using the App

### Tab 1: Ask Questions

Ask natural language questions about risk factors and products:

**Example Questions:**
- "What are the driver-related risk factors?"
- "Tell me about the Monthly-Comfort product"
- "What discount factors are available?"
- "How many risk factors are there?"
- "What coverage types are supported?"
- "Explain the three-year claim-free discount"

The agent uses both:
1. **Memory-based knowledge** (learned from loaded knowledge)
2. **Hardcoded definitions** (product configurations)

### Tab 2: Search Knowledge

Perform semantic search across the agent's memory:

```
Search: "driver age factors"
→ Returns relevant risk factors related to driver age
  with relevance scores
```

### Tab 3: Product Definitions

View detailed product configurations:
- Risk factors with weights
- Coverage options and limits
- Assessment rules
- Additional knowledge from memory

### Tab 4: Learning Dashboard

Monitor the agent's learning:
- Total memories stored
- Learning metrics
- Usage patterns
- Risk factor search

## 🧠 How Memory Works

### 1. Knowledge Storage

When you load knowledge, it's broken down and stored as semantic memories:

```python
# Example: Loading driver factors
memory_layer.add_memory(
    text="Category: Driver Factors\n"
         "Driver_Age_Risk_Factor_BI_PD: Driver Age, BI/PD Points | "
         "Applies to coverages: BI, PD",
    metadata={
        "category": "risk_factors_driver",
        "priority": "high",
        "source": "risk_factor_point_tables.md"
    }
)
```

### 2. Semantic Search

When you ask a question, the agent searches memory using semantic similarity:

```python
# Query: "What are driver age factors?"
results = agent.query_knowledge("What are driver age factors?", limit=5)
# Returns relevant memories ranked by similarity
```

### 3. Learning from Interactions

Every interaction is recorded for future learning:

```python
# After answering a question
agent.learn_from_interaction("query", {
    "query": "What are discount factors?",
    "response": "Based on my knowledge: ..."
})
```

### 4. Context-Aware Responses

The agent combines multiple sources:
1. Memory search results (semantic knowledge)
2. Hardcoded definitions (product configurations)
3. Usage patterns (frequently accessed information)

## 📊 Knowledge Base

### Risk Factor Categories

| Category | Count | Examples |
|----------|-------|----------|
| **Driver Factors** | 19 | Driver Age, Driver Class, Years Licensed, Driving Record Points |
| **Vehicle Factors** | 13 | Vehicle Age, Garaging Location, Annual Miles, Vehicle Attributes |
| **Household/Policy** | 5 | HH Structure, Full Coverage, Late Renewal, Advance Quote |
| **Discount Factors** | 11 | Continuous Insurance, Three Year Safe Driver, Home/MH/MC |
| **Tier & Rate** | 5 | UW Tier, FR Tier, Base Rates, Monthly Rate, Policy Term |
| **Coverage & Limit** | 12 | COLL/COMP Selection, Limit and Deductible factors |
| **Operational Expense** | 9 | OpEx1-8, Acquisition Expense factors |
| **UBI/Telematics** | 2 | NSP Default Safety Score factors |

**Total:** 79 risk factors

### Coverage Types

- **BI** (Bodily Injury)
- **PD** (Property Damage)
- **COMP** (Comprehensive)
- **COLL** (Collision)
- **LOAN** (Loan/Lease)
- **MED** (Medical Payments)
- **UM** (Uninsured Motorist)
- **UIM** (Underinsured Motorist)
- **RENT** (Rental)
- **ACPE** (Additional Custom Personal Equipment)
- **ACQ-EXP** (Acquisition Expense)
- **OPS-EXP** (Operations Expense)
- **TOW** (Towing)

## 🔧 API Reference

### ProductDefinitionAgent

#### Memory-Based Methods

```python
# Initialize agent
agent = ProductDefinitionAgent(
    use_memory=True,
    agent_id="product_definition_agent",
    user_id="system"
)

# Query knowledge
results = agent.query_knowledge(
    query="What are driver factors?",
    limit=5
)

# Search risk factors
factors = agent.search_risk_factors(
    query="discount",
    category="Driver Factors"
)

# Answer questions
answer = agent.answer_question(
    "Tell me about the Monthly-Comfort product"
)

# Learn from interaction
agent.learn_from_interaction("query", {
    "query": "...",
    "response": "..."
})

# Get product knowledge
knowledge = agent.get_product_knowledge("Monthly-Comfort")

# Get memory statistics
stats = agent.get_memory_stats()
```

#### Traditional Methods

```python
# Get product definition
product = agent.get_product_definition("Monthly-Comfort")

# Get risk factor definitions
factors = agent.get_risk_factor_definitions("Monthly-Comfort")
# Returns: [(risk_subject, risk_factor_name), ...]

# Get assessment rules
rules = agent.get_assessment_rules("Monthly-Comfort")

# List products
products = agent.list_available_products()

# Validate product
validation = agent.validate_product_configuration("Monthly-Comfort")
```

## 🎓 Learning Capabilities

The agent learns in several ways:

### 1. Query Learning
Records what questions users ask and how they're answered
```python
# Stored as: "User queried: X. Response provided: Y"
```

### 2. Definition Request Tracking
Tracks which products/factors are frequently accessed
```python
# Stored as: "Product definition requested: Monthly-Comfort. Factors: 3"
```

### 3. Usage Pattern Detection
Identifies common workflows and preferences
```python
# Stored as: "Usage pattern detected: frequent_discount_queries. Frequency: 15"
```

### 4. Validation Learning
Remembers validation results and issues
```python
# Stored as: "Validation performed for: Monthly-Economy. Status: valid"
```

## 🔬 Technical Details

### Memory Storage

- **Provider**: Mem0 / OpenAI embeddings
- **Search**: Semantic similarity using vector embeddings
- **Persistence**: Milvus (or configured backend)
- **Temperature**: 0.3 (lower for factual knowledge)

### Performance

- **Knowledge Loading**: ~30-60 seconds for full knowledge base
- **Query Response**: ~1-3 seconds (includes memory search)
- **Memory Growth**: Linear with interactions
- **Search Accuracy**: High (semantic embeddings)

## 📚 Knowledge Sources

All knowledge is loaded from:

1. **risk_factor_point_tables.md**
   - 79 risk factor/point tables
   - Detailed coverage mappings
   - Source: AZ_2025-07-15_v250.xlsm

2. **risk_factor_list_knowlege.md**
   - 70 risk factor names
   - Quick reference list

3. **Product Domain Knowledge**
   - Hardcoded in agent initialization
   - Monthly-Comfort, Monthly-Economy, Monthly-Turbo definitions

## 🔄 Comparison: Traditional vs Memory-Based

| Feature | Traditional Agent | Memory-Based Agent |
|---------|-------------------|-------------------|
| **State** | Stateless | Stateful |
| **Learning** | None | Continuous |
| **Context** | Per-session only | Across sessions |
| **Knowledge** | Fixed/Hardcoded | Growing |
| **Responses** | Template-based | Context-aware |
| **Personalization** | None | User-specific |
| **Improvement** | Manual updates | Automatic learning |

## 🎯 Use Cases

### 1. Product Information System
Answer questions about products and risk factors for:
- Sales teams
- Underwriters
- Product managers
- Compliance teams

### 2. Knowledge Base
Centralized, searchable repository of:
- Risk factor definitions
- Product configurations
- Assessment rules
- Coverage options

### 3. Training Tool
Help new employees learn about:
- Insurance products
- Risk assessment process
- Factor relationships
- Coverage types

### 4. Development Assistant
Support developers working on:
- Premium calculation
- Risk assessment
- Product configuration
- Rule implementation

## 🛠️ Extending the System

### Add New Products

Edit `product_definition_agent.py`:

```python
def _add_new_product(self) -> None:
    """Add new product definition"""
    new_product = ProductDefinition(
        product_code="Monthly-Premium",
        product_name="Monthly Premium Package",
        risk_factors=[...],
        assessment_rules={...},
        coverage_options={...}
    )
    self.product_definitions["Monthly-Premium"] = new_product
```

### Add New Knowledge

Create script to load additional knowledge:

```python
# Load new markdown file
with open('new_knowledge.md', 'r') as f:
    content = f.read()

# Store in memory
memory_layer.add_memory(
    text=content,
    user_id="system",
    agent_id="product_definition_agent",
    metadata={"category": "new_knowledge", "priority": "high"}
)
```

### Customize Learning

Modify `learn_from_interaction` to track specific patterns:

```python
def learn_from_interaction(self, interaction_type: str, data: Dict):
    # Add custom learning logic
    if interaction_type == "custom_pattern":
        # Custom learning implementation
        pass
```

## 🐛 Troubleshooting

### Memory Not Loading

```bash
# Check if MemoryLayer is available
python -c "from src.memory.test_memory import MemoryLayer; print('OK')"

# Verify OpenAI API key
echo $OPENAI_API_KEY
```

### Knowledge Not Found

```bash
# Reload knowledge
./load_risk_knowledge.sh

# Check memory stats in the app (Sidebar)
```

### App Not Starting

```bash
# Check dependencies
pip install -r requirements.txt

# Check port availability
lsof -i :8502
```

## 📖 References

- [mem0.ai - Memory in Agents: What, Why and How](https://mem0.ai/blog/memory-in-agents-what-why-and-how)
- [Strands Agents - Memory Agent Example](https://strandsagents.com/latest/documentation/docs/examples/python/memory_agent/)
- Project documentation in `docs/`

## 🤝 Contributing

To contribute or extend this system:

1. Follow the mem0 pattern for memory-based features
2. Use semantic memory for knowledge storage
3. Implement learning for new interaction types
4. Update knowledge loading scripts for new sources
5. Document learning capabilities

## 📄 License

See project LICENSE file.

---

**Built with:** Python 3.10+ | Streamlit | mem0 | OpenAI | Milvus

**Status:** Production Ready ✅

**Last Updated:** October 14, 2025

