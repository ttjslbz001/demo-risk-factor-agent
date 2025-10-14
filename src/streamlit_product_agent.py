"""
Streamlit App for Memory-Based Product Definition Agent

This app demonstrates a memory-enhanced agent that can:
- Answer questions about risk factors and products
- Learn from interactions
- Search knowledge using semantic search
- Provide context-aware responses
"""

import streamlit as st
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.agents.product_definition_agent import ProductDefinitionAgent
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="Product Definition Agent - Memory-Based",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }
    .memory-stat {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    .knowledge-card {
        background-color: #e8f4f8;
        padding: 1rem;
        border-left: 4px solid #1f77b4;
        margin: 1rem 0;
        border-radius: 0.25rem;
    }
    .answer-box {
        background-color: #f9f9f9;
        padding: 1.5rem;
        border-radius: 0.5rem;
        border: 1px solid #ddd;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)


@st.cache_resource
def init_agent():
    """Initialize the product definition agent (cached)"""
    return ProductDefinitionAgent(
        use_memory=True,
        agent_id="product_definition_agent",
        user_id="system"
    )


def main():
    # Header
    st.markdown('<div class="main-header">🧠 Memory-Based Product Definition Agent</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Ask questions about risk factors, products, and insurance knowledge</div>', unsafe_allow_html=True)
    
    # Initialize agent
    try:
        agent = init_agent()
    except Exception as e:
        st.error(f"❌ Failed to initialize agent: {str(e)}")
        st.stop()
    
    # Sidebar
    with st.sidebar:
        st.header("🎛️ Agent Controls")
        
        # Memory stats
        st.subheader("📊 Memory Statistics")
        memory_stats = agent.get_memory_stats()
        
        if memory_stats.get("enabled", False):
            st.success("✅ Memory Enabled")
            if "total_memories" in memory_stats:
                st.metric("Total Memories", memory_stats["total_memories"])
            st.info(f"Agent ID: {memory_stats.get('agent_id', 'N/A')}")
        else:
            st.warning("⚠️ Memory Not Enabled")
            st.info(memory_stats.get("message", "Memory disabled"))
        
        st.divider()
        
        # Agent info
        st.subheader("ℹ️ Agent Info")
        st.write(f"**Agent Type:** Product Definition")
        st.write(f"**Memory-Based:** Yes")
        st.write(f"**Learning:** Enabled")
        
        st.divider()
        
        # Available products
        st.subheader("📦 Available Products")
        products = agent.list_available_products()
        for prod in products:
            st.write(f"• {prod}")
        
        st.divider()
        
        # Quick actions
        st.subheader("⚡ Quick Actions")
        if st.button("🔄 Reload Knowledge", use_container_width=True):
            st.rerun()
        
        if st.button("📚 View Sample Questions", use_container_width=True):
            st.session_state['show_samples'] = True
    
    # Main content area
    tab1, tab2, tab3, tab4 = st.tabs([
        "💬 Ask Questions", 
        "🔍 Search Knowledge", 
        "📋 Product Definitions",
        "📊 Learning Dashboard"
    ])
    
    # Tab 1: Ask Questions
    with tab1:
        st.header("Ask the Agent")
        st.write("The agent uses both hardcoded definitions and learned knowledge from memory to answer your questions.")
        
        # Sample questions
        if st.session_state.get('show_samples', False):
            st.info("""
            **Sample Questions:**
            - What are the driver-related risk factors?
            - Tell me about the Monthly-Comfort product
            - What discount factors are available?
            - How many risk factors are there?
            - What coverage types are supported?
            - Explain the three-year claim-free discount
            """)
            if st.button("Hide Samples"):
                st.session_state['show_samples'] = False
        
        # Question input
        question = st.text_area(
            "Your Question:",
            placeholder="e.g., What are the driver-related risk factors?",
            height=100,
            key="question_input"
        )
        
        col1, col2 = st.columns([1, 5])
        with col1:
            ask_button = st.button("🚀 Ask", type="primary", use_container_width=True)
        with col2:
            if st.button("🗑️ Clear", use_container_width=True):
                st.session_state['question_input'] = ""
                st.rerun()
        
        if ask_button and question:
            with st.spinner("🤔 Thinking..."):
                try:
                    answer = agent.answer_question(question)
                    
                    st.markdown("### 💡 Answer")
                    # Render the answer as markdown for better formatting
                    st.markdown(answer)
                    
                    # Show timestamp
                    st.caption(f"Answered at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                    
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")
        elif ask_button:
            st.warning("⚠️ Please enter a question")
    
    # Tab 2: Search Knowledge
    with tab2:
        st.header("Search Knowledge Base")
        st.write("Perform semantic search across the agent's memory to find relevant knowledge.")
        
        search_query = st.text_input(
            "Search Query:",
            placeholder="e.g., driver age factors",
            key="search_query"
        )
        
        col1, col2, col3 = st.columns([1, 1, 4])
        with col1:
            search_limit = st.number_input("Max Results", min_value=1, max_value=20, value=5)
        with col2:
            search_button = st.button("🔍 Search", type="primary", use_container_width=True)
        
        if search_button and search_query:
            with st.spinner("🔍 Searching..."):
                try:
                    results = agent.query_knowledge(search_query, limit=search_limit)
                    
                    if results:
                        st.success(f"✅ Found {len(results)} results")
                        
                        for idx, result in enumerate(results, 1):
                            with st.expander(f"Result {idx} - Score: {result.get('score', 0):.4f}"):
                                st.markdown(result['text'])
                                
                                # Show metadata if available
                                metadata = result.get('metadata', {})
                                if metadata:
                                    st.caption("**Metadata:**")
                                    for key, value in metadata.items():
                                        st.caption(f"  • {key}: {value}")
                    else:
                        st.info("No results found. Try a different query.")
                        
                except Exception as e:
                    st.error(f"❌ Search error: {str(e)}")
        elif search_button:
            st.warning("⚠️ Please enter a search query")
    
    # Tab 3: Product Definitions
    with tab3:
        st.header("Product Definitions")
        st.write("View detailed product definitions and risk factors.")
        
        # Product selector
        products = agent.list_available_products()
        selected_product = st.selectbox("Select Product:", products)
        
        if st.button("📋 Get Definition", type="primary"):
            with st.spinner("Loading..."):
                try:
                    product_knowledge = agent.get_product_knowledge(selected_product)
                    product_def = product_knowledge.get('definition')
                    
                    if product_def:
                        # Product overview
                        st.subheader(f"📦 {product_def.product_name}")
                        st.write(f"**Product Code:** {product_def.product_code}")
                        
                        # Risk factors
                        st.markdown("### 🎯 Risk Factors")
                        for rf in product_def.risk_factors:
                            with st.expander(f"{rf.risk_factor_name} (Weight: {rf.weight})"):
                                st.write(f"**Subject:** {rf.risk_subject}")
                                st.write(f"**Description:** {rf.description}")
                                st.write(f"**Required:** {'Yes' if rf.required else 'No'}")
                                st.write(f"**Evaluation Rules:** {', '.join(rf.evaluation_rules)}")
                        
                        # Coverage options
                        st.markdown("### 🛡️ Coverage Options")
                        coverage = product_def.coverage_options
                        for cov_type, cov_details in coverage.items():
                            st.write(f"**{cov_type}:** {cov_details}")
                        
                        # Memory knowledge
                        if product_knowledge.get('memory_knowledge'):
                            st.markdown("### 🧠 Additional Knowledge from Memory")
                            for idx, know in enumerate(product_knowledge['memory_knowledge'], 1):
                                st.markdown(f'<div class="knowledge-card">{know["text"]}</div>', 
                                          unsafe_allow_html=True)
                    else:
                        st.warning(f"No definition found for {selected_product}")
                        
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")
    
    # Tab 4: Learning Dashboard
    with tab4:
        st.header("Learning Dashboard")
        st.write("Monitor how the agent learns from interactions.")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📈 Learning Metrics")
            memory_stats = agent.get_memory_stats()
            
            if memory_stats.get("enabled"):
                st.metric("Total Memories", memory_stats.get("total_memories", 0))
                st.metric("Agent ID", memory_stats.get("agent_id", "N/A"))
            else:
                st.info("Memory not enabled")
        
        with col2:
            st.subheader("🔍 Search Risk Factors")
            
            risk_factor_query = st.text_input(
                "Search for risk factors:",
                placeholder="e.g., discount factors"
            )
            
            if st.button("🔎 Search Risk Factors"):
                if risk_factor_query:
                    with st.spinner("Searching..."):
                        try:
                            results = agent.search_risk_factors(risk_factor_query)
                            
                            if results:
                                st.success(f"Found {len(results)} risk factors")
                                for idx, result in enumerate(results, 1):
                                    st.write(f"{idx}. {result['text'][:150]}...")
                            else:
                                st.info("No risk factors found")
                        except Exception as e:
                            st.error(f"Error: {str(e)}")
                else:
                    st.warning("Please enter a search query")
        
        st.divider()
        
        # Learning examples
        st.subheader("📚 How Learning Works")
        st.markdown("""
        The agent learns in several ways:
        
        1. **Query Learning**: Records what questions users ask and how they're answered
        2. **Definition Requests**: Tracks which products and risk factors are frequently accessed
        3. **Usage Patterns**: Identifies common workflows and preferences
        4. **Validation Learning**: Remembers validation results and issues
        
        This enables the agent to:
        - Provide better, more contextual answers over time
        - Anticipate user needs based on patterns
        - Continuously expand its knowledge base
        - Maintain conversation history and context
        """)
        
        st.info("💡 **Tip:** The more you interact with the agent, the smarter it becomes!")
    
    # Footer
    st.divider()
    st.caption("🧠 Memory-Based Product Definition Agent | Built with Streamlit + mem0 pattern")


if __name__ == "__main__":
    main()

