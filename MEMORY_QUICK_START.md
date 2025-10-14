# 🚀 Memory System - Quick Start Guide

## ✅ System Status: WORKING!

All issues have been resolved. The memory system is fully operational.

---

## 🎯 Quick Test (30 seconds)

```bash
# Run diagnostic test
./test_memory_fix.sh

# Start Streamlit app  
streamlit run src/memory/memory_manager_app.py
```

---

## 💡 Key Insight: Content Matters!

**Mem0 uses AI to extract facts from your text.**

### ✅ Works Great:
```
"I am John Smith, a 45-year-old engineer with 20 years of safe driving."
```
**Extracts:** 3 memories (name, age/occupation, driving history)

### ❌ Won't Work:
```
"Test memory"
```
**Extracts:** 0 memories (no meaningful facts)

---

## 📝 Add Memory (Streamlit)

1. Enter **`user_123`** in sidebar
2. Click **"Add Memory"** tab
3. Enter meaningful text:
   ```
   Customer has comprehensive insurance preference with $500 deductible.
   Drives a 2022 Honda Accord. Lives in San Francisco, California.
   ```
4. Click **"Add Memory"**
5. See extracted memories in the response!

---

## 🔍 View Memories

1. Enter **`user_123`** in sidebar
2. Click **"View All Memories"** tab  
3. Click **"Load Memories"**
4. See all stored memories!

---

## 🔎 Search Memories

1. Enter **`user_123`** in sidebar
2. Click **"Search Memories"** tab
3. Enter natural language query:
   ```
   What vehicle does the customer drive?
   ```
4. See relevant results with scores!

---

## 🐛 Troubleshooting

### No memories found?
- ✅ **Use meaningful content** (see examples above)
- ✅ **Check user_id matches** what you used when adding

### Database errors?
```bash
# Reset database
rm milvus.db
# Restart app
```

### Library errors?
```bash
# Reinstall with pinned versions
pip install -r requirements.txt --force-reinstall
```

---

## 📚 Good Content Examples

### Insurance Context:
- "Customer prefers comprehensive coverage with low deductible"
- "Has 15 years claim-free driving history"
- "Owns a 2023 Tesla Model 3 valued at $45,000"
- "Lives in low-risk ZIP code 94102"

### Personal Information:
- "Name is Sarah Johnson, age 42, works as a dentist"
- "Has two teenage drivers in the household"
- "Commutes 30 miles daily to work"

### Preferences:
- "Prefers digital communication over phone calls"
- "Interested in bundling home and auto insurance"
- "Wants paperless billing"

---

## 🎓 Programmatic Usage

```python
from src.memory.test_memory import MemoryLayer

# Initialize
memory = MemoryLayer()

# Add
result = memory.add_memory(
    text="Customer drives a 2022 Honda Accord",
    user_id="user_123"
)

# Retrieve
memories = memory.get_memories(user_id="user_123")

# Search
results = memory.search_memories(
    query="What car does the customer drive?",
    user_id="user_123"
)
```

---

## ✅ Verification Checklist

- [ ] Run `./test_memory_fix.sh` - all tests pass
- [ ] Streamlit app starts without errors
- [ ] Can add memory with meaningful content
- [ ] Can view all memories for user_123
- [ ] Can search and find relevant memories
- [ ] No database corruption errors

---

## 🎉 Ready to Use!

The system is working perfectly. Start adding memories to your agents!

**For full details, see:** `MEMORY_SYSTEM_FIXED.md`

