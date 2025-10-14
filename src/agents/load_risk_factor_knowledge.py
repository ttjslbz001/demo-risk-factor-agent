"""
Load Risk Factor Knowledge into Memory
This script loads risk factor knowledge from markdown files into the memory system
Following the mem0 pattern for persistent, evolving knowledge
"""

import sys
import os
from pathlib import Path
from datetime import datetime
import time

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.memory.test_memory import MemoryLayer


def print_section(title):
    """Print a formatted section header"""
    print(f"\n{'='*70}")
    print(f"  {title}")
    print('='*70)


def load_risk_factor_knowledge():
    """Load risk factor knowledge from markdown files into memory"""
    
    print("🧠 Risk Factor Knowledge Loader")
    print("Loading risk factor knowledge into memory system...")
    
    # Initialize Memory Layer
    print_section("1. Initializing Memory Layer")
    memory_layer = MemoryLayer(
        llm_provider="openai",
        temperature=0.3,  # Lower temperature for factual knowledge
        max_tokens=4000
    )
    print("✅ Memory Layer initialized successfully")
    
    # Agent identity
    agent_id = "product_definition_agent"
    user_id = "system"  # System-level knowledge
    run_id = f"knowledge_load_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    print(f"🤖 Agent ID: {agent_id}")
    print(f"📚 Loading knowledge as system-level memory")
    print(f"▶️  Run ID: {run_id}")
    
    # Load risk factor point tables
    print_section("2. Loading Risk Factor Point Tables Knowledge")
    
    point_tables_file = Path("docs/audit_file_demo/risk_factor_point_tables.md")
    if point_tables_file.exists():
        with open(point_tables_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Parse and load the table data as structured memories
        lines = content.split('\n')
        
        # Load the overview as a memory
        overview = """
        Risk Factors Reference Table contains 79 risk factor/point tables extracted from 92+ factor tables.
        Organized into categories: Driver Factors (19), Vehicle Factors (13), Household/Policy Factors (5),
        Discount Factors (11), Tier & Rate Factors (5), Coverage & Limit Factors (12),
        Operational Expense Factors (9), UBI/Telematics Factors (2).
        Coverage codes include: BI, PD, COMP, COLL, LOAN, MED, UM, UIM, RENT, ACPE, ACQ-EXP, OPS-EXP, TOW.
        Source: AZ_2025-07-15_v250.xlsm
        """
        
        result = memory_layer.add_memory(
            text=overview,
            user_id=user_id,
            agent_id=agent_id,
            run_id=run_id,
            metadata={
                "category": "risk_factor_overview",
                "priority": "high",
                "source": "risk_factor_point_tables.md",
                "type": "knowledge",
                "timestamp": datetime.now().isoformat()
            }
        )
        print(f"✅ Loaded overview knowledge")
        time.sleep(0.5)
        
        # Parse individual risk factors from the table
        risk_factors = []
        current_category = None
        
        for line in lines:
            if "**DRIVER FACTORS**" in line:
                current_category = "Driver Factors"
            elif "**VEHICLE FACTORS**" in line:
                current_category = "Vehicle Factors"
            elif "**HOUSEHOLD/POLICY FACTORS**" in line:
                current_category = "Household/Policy Factors"
            elif "**DISCOUNT FACTORS**" in line:
                current_category = "Discount Factors"
            elif "**TIER & RATE FACTORS**" in line:
                current_category = "Tier & Rate Factors"
            elif "**COVERAGE & LIMIT FACTORS**" in line:
                current_category = "Coverage & Limit Factors"
            elif "**OPERATIONAL EXPENSE FACTORS**" in line:
                current_category = "Operational Expense Factors"
            elif "**UBI/TELEMATICS FACTORS**" in line:
                current_category = "UBI/Telematics Factors"
            elif line.startswith('|| ') and line.count('|') >= 4 and current_category:
                parts = [p.strip() for p in line.split('|') if p.strip()]
                if len(parts) >= 4 and parts[0].isdigit():
                    risk_factors.append({
                        "number": parts[0],
                        "name": parts[1],
                        "risk_category": parts[2],
                        "coverages": parts[3],
                        "category": current_category
                    })
        
        print(f"Parsed {len(risk_factors)} risk factors from table")
        
        # Load each risk factor as a memory (batch by category)
        categories = {}
        for rf in risk_factors:
            cat = rf['category']
            if cat not in categories:
                categories[cat] = []
            categories[cat].append(rf)
        
        for category, factors in categories.items():
            # Create consolidated memory for each category
            factor_texts = []
            for rf in factors:
                factor_texts.append(
                    f"{rf['name']}: {rf['risk_category']} | Applies to coverages: {rf['coverages']}"
                )
            
            consolidated_text = f"Category: {category}\n" + "\n".join(factor_texts)
            
            result = memory_layer.add_memory(
                text=consolidated_text,
                user_id=user_id,
                agent_id=agent_id,
                run_id=run_id,
                metadata={
                    "category": f"risk_factors_{category.lower().replace(' ', '_').replace('/', '_')}",
                    "priority": "high",
                    "source": "risk_factor_point_tables.md",
                    "type": "knowledge",
                    "factor_count": len(factors),
                    "timestamp": datetime.now().isoformat()
                }
            )
            print(f"✅ Loaded {len(factors)} factors from {category}")
            time.sleep(0.5)
    
    else:
        print(f"⚠️  File not found: {point_tables_file}")
    
    # Load risk factor list knowledge
    print_section("3. Loading Risk Factor List Knowledge")
    
    list_file = Path("docs/audit_file_demo/risk_factor_list_knowlege.md")
    if list_file.exists():
        with open(list_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Parse the list
        factor_names = [line.strip() for line in content.split('\n') if line.strip()]
        
        print(f"Found {len(factor_names)} risk factor names")
        
        # Create batches of 10 for efficient memory storage
        batch_size = 10
        for i in range(0, len(factor_names), batch_size):
            batch = factor_names[i:i+batch_size]
            batch_text = f"Risk Factor Names (Batch {i//batch_size + 1}):\n" + "\n".join(
                f"- {name}" for name in batch
            )
            
            result = memory_layer.add_memory(
                text=batch_text,
                user_id=user_id,
                agent_id=agent_id,
                run_id=run_id,
                metadata={
                    "category": "risk_factor_names",
                    "priority": "medium",
                    "source": "risk_factor_list_knowlege.md",
                    "type": "knowledge",
                    "batch_number": i//batch_size + 1,
                    "timestamp": datetime.now().isoformat()
                }
            )
            print(f"✅ Loaded batch {i//batch_size + 1} ({len(batch)} factors)")
            time.sleep(0.5)
    
    else:
        print(f"⚠️  File not found: {list_file}")
    
    # Add domain knowledge about product definitions
    print_section("4. Loading Product Domain Knowledge")
    
    domain_knowledge = [
        {
            "text": """
            Product Definition Agent manages insurance product configurations including:
            - Risk factor definitions (risk_subject, risk_factor_name pairs)
            - Assessment rules for each risk factor
            - Coverage options and limits
            - Product-specific rule configurations
            Main products: Monthly-Comfort, Monthly-Economy, Monthly-Turbo
            """,
            "category": "product_domain",
            "priority": "high"
        },
        {
            "text": """
            Risk Subject Types in insurance products:
            - driver: Risk factors related to the driver (age, experience, driving record)
            - vehicle: Risk factors related to the vehicle (age, type, value, location)
            - policy: Risk factors related to the policy (coverage, limits, household)
            """,
            "category": "risk_subject_types",
            "priority": "high"
        },
        {
            "text": """
            Monthly-Comfort Product includes three main risk factors:
            1. three_year_claim_free_discount (driver, weight 1.0)
            2. driving_record_classification (driver, weight 1.2)
            3. driver_classification (driver, weight 0.8)
            Coverage options: liability (25k-100k), comprehensive, collision with various deductibles
            """,
            "category": "product_monthly_comfort",
            "priority": "high"
        },
        {
            "text": """
            Risk Factor Evaluation Process:
            1. Product Definition Agent defines required risk factors
            2. Risk Factor Agent assesses each factor based on rules
            3. Premium Calculation Agent uses assessments to calculate premium
            4. Data Lookup Agent provides data needed for assessment
            """,
            "category": "evaluation_process",
            "priority": "medium"
        }
    ]
    
    for knowledge in domain_knowledge:
        result = memory_layer.add_memory(
            text=knowledge["text"],
            user_id=user_id,
            agent_id=agent_id,
            run_id=run_id,
            metadata={
                "category": knowledge["category"],
                "priority": knowledge["priority"],
                "source": "domain_knowledge",
                "type": "knowledge",
                "timestamp": datetime.now().isoformat()
            }
        )
        print(f"✅ Loaded: {knowledge['category']}")
        time.sleep(0.5)
    
    # Verify loaded knowledge
    print_section("5. Verifying Loaded Knowledge")
    
    test_queries = [
        "What are the driver-related risk factors?",
        "What coverage types are supported?",
        "What is the Monthly-Comfort product?",
        "How many risk factors are there?"
    ]
    
    for query in test_queries:
        print(f"\n🔍 Test Query: '{query}'")
        results = memory_layer.search_memories(
            query=query,
            user_id=user_id,
            agent_id=agent_id,
            limit=2
        )
        
        if results:
            for idx, result in enumerate(results, 1):
                if isinstance(result, dict):
                    score = result.get('score', 'N/A')
                    memory_text = result.get('memory', result.get('text', str(result)))
                    if isinstance(score, (int, float)):
                        print(f"   ✓ Result {idx} (Score: {score:.4f})")
                    else:
                        print(f"   ✓ Result {idx} (Score: {score})")
                    print(f"     {str(memory_text)[:100]}...")
                else:
                    print(f"   ✓ Result {idx}: {str(result)[:100]}...")
        else:
            print("   ⚠️  No results found")
        time.sleep(0.3)
    
    print_section("Knowledge Loading Complete")
    print("✨ Risk factor knowledge successfully loaded into memory!")
    print(f"\n📊 Summary:")
    print(f"   Agent ID: {agent_id}")
    print(f"   User ID: {user_id}")
    print(f"   Run ID: {run_id}")
    print(f"\n💡 The Product Definition Agent can now use this knowledge to answer questions!")
    print(f"   Run: python src/agents/product_definition_agent.py")
    print(f"   Or use the Streamlit app: streamlit run src/streamlit_product_agent.py")
    
    return {
        "agent_id": agent_id,
        "user_id": user_id,
        "run_id": run_id,
        "status": "success"
    }


if __name__ == "__main__":
    try:
        result = load_risk_factor_knowledge()
        print(f"\n✅ Knowledge loading completed: {result['status']}")
    except KeyboardInterrupt:
        print("\n\n⚠️  Knowledge loading interrupted by user")
    except Exception as e:
        print(f"\n\n❌ Error during knowledge loading: {str(e)}")
        import traceback
        traceback.print_exc()

