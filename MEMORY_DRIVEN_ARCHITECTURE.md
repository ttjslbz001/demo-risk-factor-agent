# Memory-Driven Architecture - Product Definition Agent

## 🔥 Overview

The `ProductDefinitionAgent` has been **completely refactored** to be a **fully memory-driven, stateless agent** that loads all knowledge from **mem0** (memory system).

### Key Changes

**Before (Hardcoded):**
- ❌ Product definitions hardcoded in `_load_product_definitions()`
- ❌ Local state management with `self.product_definitions` dictionary
- ❌ Static, unchangeable product catalog
- ❌ Not scalable - each instance has its own copy

**After (Memory-Driven):**
- ✅ All product definitions stored in mem0 vector database
- ✅ NO local state - queries mem0 dynamically for every request
- ✅ Dynamic, growable knowledge base
- ✅ Horizontally scalable stateless design
- ✅ Shared knowledge across all agent instances

---

## 🏗️ Architecture

### Stateless Design

```python
class ProductDefinitionAgent:
    """
    Fully memory-driven agent - NO local state management
    """
    
    def __init__(self, use_memory=True, agent_id="product_definition_agent", user_id="system"):
        # Only initialize memory connection
        self.memory = MemoryLayer(...)
        # NO self.product_definitions dictionary!
        
    def get_product_definition(self, product_code: str):
        # Always queries mem0 - never uses local cache
        results = self.memory.search_memories(query=f"product definition for {product_code}", ...)
        return self._parse_product_from_memory(results)
```

### Data Flow

```
User Request
    ↓
ProductDefinitionAgent
    ↓
mem0 Vector Database (semantic search)
    ↓
Parse & Return Results
    ↓
User Response
```

---

## 📦 Setting Up Memory

### 1. Bootstrap with Sample Data

The quickest way to get started:

```bash
python bootstrap_product_memory.py --sample-data
```

This will load 3 sample products into mem0:
- **Monthly-Comfort**: Mid-tier product with 3 risk factors
- **Monthly-Economy**: Basic product with minimal coverage
- **Monthly-Turbo**: Premium product with comprehensive coverage

### 2. Store Custom Products

```python
from src.agents.product_definition_agent import ProductDefinitionAgent, ProductDefinition, RiskFactorDefinition

# Initialize agent
agent = ProductDefinitionAgent(use_memory=True)

# Create product definition
product = ProductDefinition(
    product_code="Custom-Product",
    product_name="Custom Insurance Package",
    risk_factors=[
        RiskFactorDefinition(
            risk_subject="driver",
            risk_factor_name="age_factor",
            description="Driver age assessment",
            evaluation_rules=["R01_Age_Rule"],
            required=True,
            weight=1.0
        )
    ],
    assessment_rules={
        "R01_Age_Rule": {
            "id": "R01_Age_Rule",
            "name": "Age Rule",
            "description": "Assess driver by age"
        }
    },
    coverage_options={
        "liability": {"min": 25000, "max": 100000}
    }
)

# Store to mem0
agent.store_product_to_memory(product)
```

### 3. Load from Rules Directory

```python
# Load product from existing rule files
agent.load_product_from_rules_dir(
    product_code="Monthly-Comfort",
    rules_dir="docs/insurance_risk_factor_agent/3_year_claim_free_discount"
)
```

---

## 🔍 Using the Agent

### Query Products

All queries go through mem0 - no local state:

```python
agent = ProductDefinitionAgent(use_memory=True)

# List all available products (queries mem0)
products = agent.list_available_products()
print(f"Available: {products}")  # ['Monthly-Comfort', 'Monthly-Economy', 'Monthly-Turbo']

# Get specific product (queries mem0)
product = agent.get_product_definition("Monthly-Comfort")
print(f"Risk Factors: {len(product.risk_factors)}")

# Get risk factor definitions (queries mem0)
factors = agent.get_risk_factor_definitions("Monthly-Comfort")
print(f"Factors: {factors}")

# Get assessment rules (queries mem0)
rules = agent.get_assessment_rules("Monthly-Comfort")
print(f"Rules: {len(rules)}")
```

### Ask Questions

Natural language queries using semantic search:

```python
# Ask questions - agent searches mem0
answer = agent.answer_question("What products are available?")
print(answer)

answer = agent.answer_question("Tell me about Monthly-Comfort product")
print(answer)

answer = agent.answer_question("What risk factors does Monthly-Turbo have?")
print(answer)
```

### Search Knowledge

```python
# Search for risk factors
results = agent.search_risk_factors("driver age", category="driver")
print(f"Found {len(results)} results")

# Query general knowledge
results = agent.query_knowledge("discount factors", limit=5)
for r in results:
    print(f"Score: {r['score']:.3f} - {r['text'][:100]}")
```

---

## 🔄 Memory Management

### Learning from Interactions

The agent automatically learns from usage:

```python
# Automatically logs to mem0 when you use the agent
agent.answer_question("...")  # Logs query + response
agent.get_product_definition("...")  # Logs product access
agent.validate_product_configuration("...")  # Logs validation
```

### Manual Learning

```python
# Store custom learning insights
agent.learn_from_interaction(
    interaction_type="usage_pattern",
    data={"pattern": "Users frequently ask about discounts", "frequency": 50}
)
```

### Memory Statistics

```python
stats = agent.get_memory_stats()
print(f"Total memories: {stats['total_memories']}")
print(f"Agent ID: {stats['agent_id']}")
print(f"User ID: {stats['user_id']}")
```

---

## 🎯 Benefits of Memory-Driven Architecture

### 1. **Scalability**
- Stateless design allows horizontal scaling
- Multiple agent instances share the same mem0 database
- No memory overhead from duplicated product definitions

### 2. **Flexibility**
- Add/update products without code changes
- Dynamic knowledge base grows over time
- Easy A/B testing with different product configurations

### 3. **Persistence**
- Product definitions survive application restarts
- Learning insights accumulate over time
- Shared knowledge across deployments

### 4. **Context-Aware**
- Semantic search finds relevant information
- Natural language queries work out of the box
- Related knowledge automatically surfaces

### 5. **Maintainability**
- No hardcoded product data in source code
- Separation of code and data
- Easy to version control product definitions

---

## 🔧 Advanced Usage

### Multi-User Isolation

```python
# Different users get isolated memory spaces
agent_user1 = ProductDefinitionAgent(user_id="user_001", agent_id="product_agent")
agent_user2 = ProductDefinitionAgent(user_id="user_002", agent_id="product_agent")

# Each user has separate product definitions in mem0
agent_user1.store_product_to_memory(product_for_user1)
agent_user2.store_product_to_memory(product_for_user2)
```

### Product Versioning

```python
# Store different versions with metadata
product_v1 = ProductDefinition(
    product_code="Monthly-Comfort-v1",
    product_name="Monthly Comfort Package v1.0",
    # ... rest of definition
)

product_v2 = ProductDefinition(
    product_code="Monthly-Comfort-v2",
    product_name="Monthly Comfort Package v2.0",
    # ... updated definition
)

agent.store_product_to_memory(product_v1)
agent.store_product_to_memory(product_v2)
```

### Bulk Operations

```python
# Load multiple products at once
products = [product1, product2, product3]
for product in products:
    success = agent.store_product_to_memory(product)
    print(f"Stored {product.product_code}: {success}")
```

---

## 📊 Performance Considerations

### Query Optimization

```python
# Efficient: Specific queries
product = agent.get_product_definition("Monthly-Comfort")

# Less efficient: Broad queries that need parsing
all_products = agent.list_available_products()  # Queries mem0 with broad search
```

### Caching Strategy

While the agent itself is stateless, you can implement caching at the application level:

```python
from functools import lru_cache

class CachedProductAgent:
    def __init__(self):
        self.agent = ProductDefinitionAgent(use_memory=True)
    
    @lru_cache(maxsize=100)
    def get_product(self, product_code: str):
        # Cache product definitions in application memory
        return self.agent.get_product_definition(product_code)
```

---

## 🐛 Troubleshooting

### No Products Found

```python
products = agent.list_available_products()
if not products:
    print("⚠️ No products in memory. Run bootstrap script:")
    print("python bootstrap_product_memory.py --sample-data")
```

### Memory Not Enabled

```python
agent = ProductDefinitionAgent(use_memory=True)
if not agent.use_memory:
    print("⚠️ Memory layer failed to initialize")
    print("Check your OpenAI API key and Milvus connection")
```

### Product Not Parsing

```python
# Products must be stored as JSON in mem0
# Check the format:
results = agent.memory.search_memories(query="product definition", limit=1)
print(results[0]['text'])  # Should contain JSON structure
```

---

## 🚀 Migration Guide

### From Hardcoded to Memory-Driven

**Step 1:** Bootstrap existing products into mem0

```bash
python bootstrap_product_memory.py --sample-data
```

**Step 2:** Update your code

```python
# OLD: Agent had products loaded at startup
agent = ProductDefinitionAgent()
product = agent.product_definitions["Monthly-Comfort"]  # Direct access

# NEW: Agent queries mem0 dynamically
agent = ProductDefinitionAgent(use_memory=True)
product = agent.get_product_definition("Monthly-Comfort")  # Queries mem0
```

**Step 3:** Remove hardcoded product definitions

The `_load_product_definitions()` method no longer exists - all data comes from mem0!

---

## 📚 API Reference

### Core Methods

| Method | Description | Queries mem0? |
|--------|-------------|---------------|
| `get_product_definition(code)` | Get product by code | ✅ Yes |
| `list_available_products()` | List all products | ✅ Yes |
| `get_risk_factor_definitions(code)` | Get risk factors | ✅ Yes |
| `get_assessment_rules(code)` | Get rules | ✅ Yes |
| `store_product_to_memory(product)` | Store product | ✅ Yes |
| `answer_question(question)` | Natural language query | ✅ Yes |
| `query_knowledge(query)` | Semantic search | ✅ Yes |
| `search_risk_factors(query)` | Search factors | ✅ Yes |

### Memory Methods

| Method | Description |
|--------|-------------|
| `learn_from_interaction(type, data)` | Store learning insight |
| `get_memory_stats()` | Get memory statistics |
| `load_product_from_rules_dir(code, dir)` | Bootstrap from files |

---

## 🎓 Best Practices

### 1. Initialize Products Early

```python
# At application startup
if not agent.list_available_products():
    print("Bootstrapping products...")
    os.system("python bootstrap_product_memory.py --sample-data")
```

### 2. Use Descriptive Product Codes

```python
# Good
product_code = "Monthly-Comfort-Auto-2024"

# Less good
product_code = "P001"
```

### 3. Include Rich Metadata

```python
# Add detailed descriptions for better semantic search
RiskFactorDefinition(
    risk_subject="driver",
    risk_factor_name="three_year_claim_free_discount",
    description="Comprehensive three-year claim-free driving discount assessment for safe drivers with no at-fault accidents",  # Detailed
    # not: "Discount"  # Too vague
)
```

### 4. Monitor Memory Growth

```python
# Periodically check memory stats
stats = agent.get_memory_stats()
if stats['total_memories'] > 10000:
    print("⚠️ Consider archiving old memories")
```

---

## 🔐 Security Considerations

### User Isolation

Always use proper `user_id` for multi-tenant applications:

```python
# Isolated per user
agent = ProductDefinitionAgent(
    user_id=current_user.id,  # Important!
    agent_id="product_agent"
)
```

### Data Validation

Validate products before storing:

```python
def validate_and_store(agent, product):
    # Validate structure
    if not product.product_code or not product.product_name:
        raise ValueError("Invalid product")
    
    # Validate business rules
    if len(product.risk_factors) == 0:
        raise ValueError("Product must have risk factors")
    
    # Store
    return agent.store_product_to_memory(product)
```

---

## 📈 Monitoring & Observability

### Logging

The agent logs all mem0 interactions:

```python
import logging
logging.basicConfig(level=logging.INFO)

# Logs include:
# - "Retrieved product from mem0: Monthly-Comfort"
# - "Stored product definition to mem0: Monthly-Economy"
# - "Found 3 products in mem0"
```

### Metrics to Track

- Query latency (mem0 search time)
- Cache hit rate (if implementing application-level caching)
- Product access patterns
- Failed queries
- Memory growth rate

---

## 🎉 Summary

The `ProductDefinitionAgent` is now a **fully memory-driven, stateless agent** that:

✅ Loads all data from mem0 dynamically  
✅ Has no local state management  
✅ Scales horizontally  
✅ Learns from interactions  
✅ Supports natural language queries  
✅ Persists knowledge across restarts  

**Get started:**
```bash
python bootstrap_product_memory.py --sample-data
```

**Questions?** See the examples above or check the source code docstrings.

