"""
Streamlit App for Agent Memory Management
This app provides a user interface for managing AI agent memories using mem0ai.
"""

import streamlit as st
from datetime import datetime
from memory_layer import MemoryLayer

# Page configuration
st.set_page_config(
    page_title="Agent Memory Manager",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        margin-bottom: 1rem;
    }
    .section-header {
        font-size: 1.5rem;
        font-weight: bold;
        color: #2c3e50;
        margin-top: 1.5rem;
        margin-bottom: 1rem;
        border-bottom: 2px solid #1f77b4;
        padding-bottom: 0.5rem;
    }
    .memory-card {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
        margin-bottom: 1rem;
    }
    .success-message {
        background-color: #d4edda;
        color: #155724;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #28a745;
    }
    .error-message {
        background-color: #f8d7da;
        color: #721c24;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #dc3545;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'memory_layer' not in st.session_state:
    try:
        st.session_state.memory_layer = MemoryLayer(
            llm_provider="openai",
            temperature=0.7,
            max_tokens=2000
        )
        st.session_state.initialized = True
    except Exception as e:
        st.session_state.initialized = False
        st.session_state.init_error = str(e)

# Main header
st.markdown('<div class="main-header">🧠 Agent Memory Manager</div>', unsafe_allow_html=True)
st.markdown("Manage AI agent memories with semantic search and contextual storage")

# Check initialization
if not st.session_state.initialized:
    st.error(f"Failed to initialize Memory Layer: {st.session_state.get('init_error', 'Unknown error')}")
    st.stop()

# Sidebar for configuration and filters
with st.sidebar:
    st.header("⚙️ Configuration")
    
    # Identity filters
    st.subheader("Identity Filters")
    user_id = st.text_input("User ID", value="", placeholder="e.g., user_123")
    agent_id = st.text_input("Agent ID", value="", placeholder="e.g., agent_456")
    run_id = st.text_input("Run ID", value="", placeholder="e.g., run_789")
    
    st.divider()
    
    # Statistics
    st.subheader("📊 Statistics")
    if st.button("Refresh Stats"):
        try:
            all_memories = st.session_state.memory_layer.get_memories(
                user_id=user_id if user_id else None,
                agent_id=agent_id if agent_id else None,
                run_id=run_id if run_id else None
            )
            st.metric("Total Memories", len(all_memories))
        except Exception as e:
            st.error(f"Error fetching stats: {str(e)}")

# Main tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "➕ Add Memory",
    "🔍 Search Memories", 
    "📋 View All Memories",
    "✏️ Update/Delete",
    "📜 Memory History"
])

# Tab 1: Add Memory
with tab1:
    st.markdown('<div class="section-header">Add New Memory</div>', unsafe_allow_html=True)
    
    st.info("💡 **Tip:** Mem0 uses AI to extract meaningful facts from your text. Write natural sentences with facts, preferences, or information about the user/agent.")
    
    with st.expander("✨ Example Content That Works Well"):
        st.markdown("""
        **Good examples:**
        - "I am John Smith, 35 years old, and I work as a software engineer."
        - "The user prefers comprehensive insurance with low deductibles."
        - "Customer has 10 years of safe driving with no accidents or violations."
        - "Vehicle is a 2022 Honda Accord valued at $30,000."
        
        **Less effective:**
        - "Test memory" ← Too generic
        - "Hello" ← No extractable facts
        - "Memory123" ← No meaningful content
        """)
    
    with st.form("add_memory_form"):
        col1, col2 = st.columns([2, 1])
        
        with col1:
            memory_text = st.text_area(
                "Memory Content",
                height=150,
                placeholder="Example: I am John, a 45-year-old engineer with 20 years of driving experience...",
                help="Write natural sentences with facts - Mem0 will extract meaningful memories from your text"
            )
        
        with col2:
            add_user_id = st.text_input("User ID", value=user_id, key="add_user")
            add_agent_id = st.text_input("Agent ID", value=agent_id, key="add_agent")
            add_run_id = st.text_input("Run ID", value=run_id, key="add_run")
        
        st.subheader("Metadata (Optional)")
        metadata_col1, metadata_col2 = st.columns(2)
        with metadata_col1:
            meta_category = st.text_input("Category", placeholder="e.g., preferences")
            meta_priority = st.selectbox("Priority", ["low", "medium", "high"], index=1)
        with metadata_col2:
            meta_source = st.text_input("Source", placeholder="e.g., user_input")
            meta_tags = st.text_input("Tags", placeholder="tag1, tag2, tag3")
        
        submit_button = st.form_submit_button("💾 Add Memory", use_container_width=True)
        
        if submit_button:
            if not memory_text:
                st.error("⚠️ Please enter memory content")
            else:
                try:
                    # Build metadata
                    metadata = {
                        "timestamp": datetime.now().isoformat(),
                        "priority": meta_priority
                    }
                    if meta_category:
                        metadata["category"] = meta_category
                    if meta_source:
                        metadata["source"] = meta_source
                    if meta_tags:
                        metadata["tags"] = [tag.strip() for tag in meta_tags.split(",")]
                    
                    # Add memory
                    result = st.session_state.memory_layer.add_memory(
                        text=memory_text,
                        user_id=add_user_id if add_user_id else None,
                        agent_id=add_agent_id if add_agent_id else None,
                        run_id=add_run_id if add_run_id else None,
                        metadata=metadata
                    )
                    
                    # Parse the result
                    memory_id = None
                    results_list = []
                    
                    if isinstance(result, dict):
                        # Check for different response formats
                        if 'results' in result:
                            results_list = result.get('results', [])
                            if results_list and len(results_list) > 0:
                                memory_count = len(results_list)
                                memory_id = results_list[0].get('id') if isinstance(results_list[0], dict) else None
                                st.success(f"✅ Memory added successfully! Extracted {memory_count} memories!")
                                
                                # Show extracted memories
                                st.markdown("**Extracted Memories:**")
                                for idx, mem in enumerate(results_list, 1):
                                    if isinstance(mem, dict):
                                        mem_text = mem.get('memory', str(mem))
                                        mem_event = mem.get('event', 'N/A')
                                        st.markdown(f"{idx}. {mem_text} *({mem_event})*")
                            else:
                                st.warning("⚠️ No memories extracted from your text!")
                                st.markdown("""
                                **Why this happened:**
                                Mem0's AI couldn't find meaningful facts in your text. 
                                
                                **Try adding content like:**
                                - "Customer is 35 years old and works as an engineer"
                                - "User prefers comprehensive insurance with $500 deductible"
                                - "Driver has 10 years accident-free history"
                                
                                **Avoid generic text like:**
                                - "test", "hello", "memory 123"
                                """)
                        elif 'id' in result:
                            memory_id = result.get('id')
                            st.success(f"✅ Memory added successfully! ID: `{memory_id}`")
                        else:
                            st.success("✅ Memory operation completed!")
                    else:
                        st.success("✅ Memory added!")
                    
                    # Show full result for debugging
                    with st.expander("View API Response (Debug Info)"):
                        st.json(result)
                    
                    # Provide helpful next steps
                    if results_list and len(results_list) > 0:
                        if add_user_id or add_agent_id or add_run_id:
                            st.info("💡 Go to the 'View All Memories' tab and click 'Load Memories' to see all your memories.")
                    
                except Exception as e:
                    st.error(f"❌ Error adding memory: {str(e)}")
                    import traceback
                    with st.expander("Error Details"):
                        st.code(traceback.format_exc())

# Tab 2: Search Memories
with tab2:
    st.markdown('<div class="section-header">Search Memories</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([3, 1])
    with col1:
        search_query = st.text_input(
            "Search Query",
            placeholder="Enter your search query...",
            help="Use natural language to search for relevant memories"
        )
    with col2:
        search_limit = st.number_input("Max Results", min_value=1, max_value=50, value=10)
    
    if st.button("🔍 Search", use_container_width=True):
        if not search_query:
            st.warning("⚠️ Please enter a search query")
        else:
            try:
                with st.spinner("Searching memories..."):
                    results = st.session_state.memory_layer.search_memories(
                        query=search_query,
                        user_id=user_id if user_id else None,
                        agent_id=agent_id if agent_id else None,
                        run_id=run_id if run_id else None,
                        limit=search_limit
                    )
                
                if not results:
                    st.info("No memories found matching your query")
                else:
                    st.success(f"Found {len(results)} relevant memories")
                    
                    for idx, memory in enumerate(results, 1):
                        # Handle both dict and string responses
                        if isinstance(memory, dict):
                            score = memory.get('score', 'N/A')
                            memory_text = memory.get('memory', memory.get('text', str(memory)))
                            memory_id = memory.get('id', 'N/A')
                            
                            with st.expander(f"Memory {idx} (Score: {score})"):
                                st.markdown(f"**Content:** {memory_text}")
                                st.markdown(f"**ID:** `{memory_id}`")
                                
                                # Display metadata
                                if 'metadata' in memory and isinstance(memory.get('metadata'), dict):
                                    st.markdown("**Metadata:**")
                                    st.json(memory['metadata'])
                                
                                # Display identifiers
                                col_a, col_b, col_c = st.columns(3)
                                with col_a:
                                    if 'user_id' in memory:
                                        st.markdown(f"👤 User: `{memory['user_id']}`")
                                with col_b:
                                    if 'agent_id' in memory:
                                        st.markdown(f"🤖 Agent: `{memory['agent_id']}`")
                                with col_c:
                                    if 'run_id' in memory:
                                        st.markdown(f"▶️ Run: `{memory['run_id']}`")
                        else:
                            # Handle string or other non-dict responses
                            with st.expander(f"Memory {idx}"):
                                st.markdown(f"**Content:** {str(memory)}")
                                st.info("(Non-dictionary format)")
                    
            except Exception as e:
                st.error(f"❌ Error searching memories: {str(e)}")

# Tab 3: View All Memories
with tab3:
    st.markdown('<div class="section-header">View All Memories</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown("View all memories based on the filters in the sidebar")
    with col2:
        view_limit = st.number_input("Limit", min_value=1, max_value=100, value=20, key="view_limit")
    
    if st.button("📋 Load Memories", use_container_width=True):
        try:
            # Show what we're querying
            query_params = {}
            if user_id:
                query_params["user_id"] = user_id
            if agent_id:
                query_params["agent_id"] = agent_id
            if run_id:
                query_params["run_id"] = run_id
            
            if query_params:
                st.info(f"🔍 Querying with filters: {query_params}")
            else:
                st.info("🔍 Querying all memories (no filters)")
            
            with st.spinner("Loading memories..."):
                memories = st.session_state.memory_layer.get_memories(
                    user_id=user_id if user_id else None,
                    agent_id=agent_id if agent_id else None,
                    run_id=run_id if run_id else None,
                    limit=view_limit
                )
            
            # Debug info
            st.write(f"📊 Raw API returned {type(memories).__name__}: {len(memories) if isinstance(memories, list) else 'N/A'} items")
            
            if not memories:
                st.info("No memories found with the current filters")
            else:
                st.success(f"Loaded {len(memories)} memories")
                
                # Display in a table format
                for idx, memory in enumerate(memories, 1):
                    with st.container():
                        st.markdown(f"### Memory {idx}")
                        
                        # Handle both dict and string responses
                        if isinstance(memory, dict):
                            memory_text = memory.get('memory', memory.get('text', str(memory)))
                            memory_id = memory.get('id', f'unknown_{idx}')
                            
                            col_a, col_b = st.columns([3, 1])
                            with col_a:
                                st.markdown(f"**Content:** {memory_text}")
                                st.markdown(f"**ID:** `{memory_id}`")
                            
                            with col_b:
                                if st.button("📝 Edit", key=f"edit_{memory_id}"):
                                    st.session_state.edit_memory = memory
                                    st.info("Switch to 'Update/Delete' tab to edit this memory")
                                
                                if st.button("🗑️ Delete", key=f"del_{memory_id}"):
                                    try:
                                        st.session_state.memory_layer.delete_memory(
                                            memory_id=memory_id,
                                            user_id=memory.get('user_id'),
                                            agent_id=memory.get('agent_id'),
                                            run_id=memory.get('run_id')
                                        )
                                        st.success("✅ Memory deleted!")
                                        st.rerun()
                                    except Exception as e:
                                        st.error(f"❌ Error: {str(e)}")
                            
                            # Display metadata if available
                            if 'metadata' in memory and isinstance(memory.get('metadata'), dict):
                                with st.expander("View Metadata"):
                                    st.json(memory['metadata'])
                        else:
                            # Handle string or other non-dict responses
                            col_a, col_b = st.columns([3, 1])
                            with col_a:
                                st.markdown(f"**Content:** {str(memory)}")
                                st.markdown(f"**ID:** `unknown_{idx}`")
                            with col_b:
                                st.info("(Non-dictionary format)")
                        
                        st.divider()
                
        except Exception as e:
            st.error(f"❌ Error loading memories: {str(e)}")

# Tab 4: Update/Delete Memory
with tab4:
    st.markdown('<div class="section-header">Update or Delete Memory</div>', unsafe_allow_html=True)
    
    # Check if a memory was selected for editing
    if 'edit_memory' in st.session_state:
        st.info(f"Editing memory: {st.session_state.edit_memory.get('id', 'N/A')}")
        default_memory_id = st.session_state.edit_memory.get('id', '')
        default_text = st.session_state.edit_memory.get('memory', '')
    else:
        default_memory_id = ''
        default_text = ''
    
    # Update section
    st.subheader("✏️ Update Memory")
    with st.form("update_memory_form"):
        update_memory_id = st.text_input("Memory ID", value=default_memory_id, help="Enter the ID of the memory to update")
        
        col1, col2 = st.columns([2, 1])
        with col1:
            update_text = st.text_area("New Content", height=150, value=default_text)
        with col2:
            update_user_id = st.text_input("User ID", value=user_id, key="update_user")
            update_agent_id = st.text_input("Agent ID", value=agent_id, key="update_agent")
            update_run_id = st.text_input("Run ID", value=run_id, key="update_run")
        
        update_button = st.form_submit_button("💾 Update Memory", use_container_width=True)
        
        if update_button:
            if not update_memory_id or not update_text:
                st.error("⚠️ Please provide both Memory ID and new content")
            else:
                try:
                    result = st.session_state.memory_layer.update_memory(
                        memory_id=update_memory_id,
                        text=update_text,
                        user_id=update_user_id if update_user_id else None,
                        agent_id=update_agent_id if update_agent_id else None,
                        run_id=update_run_id if update_run_id else None
                    )
                    st.success("✅ Memory updated successfully!")
                    st.json(result)
                    
                    # Clear edit state
                    if 'edit_memory' in st.session_state:
                        del st.session_state.edit_memory
                    
                except Exception as e:
                    st.error(f"❌ Error updating memory: {str(e)}")
    
    st.divider()
    
    # Delete section
    st.subheader("🗑️ Delete Memory")
    with st.form("delete_memory_form"):
        delete_memory_id = st.text_input("Memory ID to Delete", help="Enter the ID of the memory to delete")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            delete_user_id = st.text_input("User ID", value=user_id, key="delete_user")
        with col2:
            delete_agent_id = st.text_input("Agent ID", value=agent_id, key="delete_agent")
        with col3:
            delete_run_id = st.text_input("Run ID", value=run_id, key="delete_run")
        
        delete_button = st.form_submit_button("🗑️ Delete Memory", use_container_width=True)
        
        if delete_button:
            if not delete_memory_id:
                st.error("⚠️ Please provide a Memory ID")
            else:
                try:
                    result = st.session_state.memory_layer.delete_memory(
                        memory_id=delete_memory_id,
                        user_id=delete_user_id if delete_user_id else None,
                        agent_id=delete_agent_id if delete_agent_id else None,
                        run_id=delete_run_id if delete_run_id else None
                    )
                    st.success("✅ Memory deleted successfully!")
                    st.json(result)
                except Exception as e:
                    st.error(f"❌ Error deleting memory: {str(e)}")
    
    st.divider()
    
    # Delete all section
    st.subheader("⚠️ Delete All Memories")
    st.warning("This will delete ALL memories matching the specified filters. This action cannot be undone!")
    
    with st.form("delete_all_form"):
        st.markdown("Delete all memories for:")
        col1, col2, col3 = st.columns(3)
        with col1:
            del_all_user = st.text_input("User ID", value=user_id, key="del_all_user")
        with col2:
            del_all_agent = st.text_input("Agent ID", value=agent_id, key="del_all_agent")
        with col3:
            del_all_run = st.text_input("Run ID", value=run_id, key="del_all_run")
        
        confirm_delete = st.checkbox("I understand this will delete all matching memories")
        delete_all_button = st.form_submit_button("🗑️ Delete All Memories", use_container_width=True)
        
        if delete_all_button:
            if not confirm_delete:
                st.error("⚠️ Please confirm the deletion by checking the box")
            elif not any([del_all_user, del_all_agent, del_all_run]):
                st.error("⚠️ Please specify at least one filter (User ID, Agent ID, or Run ID)")
            else:
                try:
                    result = st.session_state.memory_layer.delete_all_memories(
                        user_id=del_all_user if del_all_user else None,
                        agent_id=del_all_agent if del_all_agent else None,
                        run_id=del_all_run if del_all_run else None
                    )
                    st.success("✅ All matching memories deleted!")
                    st.json(result)
                except Exception as e:
                    st.error(f"❌ Error deleting memories: {str(e)}")

# Tab 5: Memory History
with tab5:
    st.markdown('<div class="section-header">Memory History</div>', unsafe_allow_html=True)
    
    st.markdown("View the history of changes for a specific memory")
    
    with st.form("history_form"):
        col1, col2 = st.columns([2, 1])
        
        with col1:
            history_memory_id = st.text_input("Memory ID", help="Enter the ID of the memory to view history")
        
        with col2:
            history_user_id = st.text_input("User ID", value=user_id, key="history_user")
            history_agent_id = st.text_input("Agent ID", value=agent_id, key="history_agent")
            history_run_id = st.text_input("Run ID", value=run_id, key="history_run")
        
        history_button = st.form_submit_button("📜 Get History", use_container_width=True)
        
        if history_button:
            if not history_memory_id:
                st.error("⚠️ Please provide a Memory ID")
            else:
                try:
                    with st.spinner("Loading history..."):
                        history = st.session_state.memory_layer.get_memory_history(
                            memory_id=history_memory_id,
                            user_id=history_user_id if history_user_id else None,
                            agent_id=history_agent_id if history_agent_id else None,
                            run_id=history_run_id if history_run_id else None
                        )
                    
                    if not history:
                        st.info("No history found for this memory")
                    else:
                        st.success(f"Found {len(history)} history entries")
                        
                        for idx, entry in enumerate(history, 1):
                            with st.expander(f"Version {idx}", expanded=(idx == 1)):
                                st.json(entry)
                    
                except Exception as e:
                    st.error(f"❌ Error loading history: {str(e)}")

# Footer
st.divider()
st.markdown("""
<div style='text-align: center; color: #666; padding: 1rem;'>
    <p>🧠 Agent Memory Manager | Powered by mem0ai</p>
    <p style='font-size: 0.8rem;'>Manage AI agent memories with semantic search and contextual storage</p>
</div>
""", unsafe_allow_html=True)

