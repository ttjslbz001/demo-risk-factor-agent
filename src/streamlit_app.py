import os
import json
import streamlit as st
import time
from datetime import datetime

# Ensure project root is on sys.path so `from src...` works when run via Streamlit
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.utils.data_parser import parse_application
from src.agents.risk_factor_agent import assess
from src.agents.multi_agent_graph import create_rating_engine

st.set_page_config(page_title="Multi-Agent Insurance Rating Engine", layout="wide")

st.title("🚗 Multi-Agent Insurance Rating Engine")
st.markdown("*Powered by Strands Agents Graph Orchestration*")

# Sidebar configuration
st.sidebar.header("⚙️ Configuration")
product_code = st.sidebar.selectbox(
    "Product Package", 
    ["Monthly-Comfort", "Monthly-Economy", "Monthly-Turbo"], 
    index=0,
    help="Select the insurance product package"
)

# Multi-agent system toggle
use_multi_agent = st.sidebar.checkbox(
    "Use Multi-Agent Graph System", 
    value=True,
    help="Enable the multi-agent graph orchestration system"
)

# Show system status
if use_multi_agent:
    with st.sidebar:
        st.subheader("🔍 System Status")
        try:
            engine = create_rating_engine(product_code)
            status = engine.get_graph_status()
            
            st.metric("Strands Available", "✅" if status['strands_available'] else "❌")
            st.metric("Graph Built", "✅" if status['graph_built'] else "❌")
            st.metric("Agents Initialized", status['agents_initialized'])
            st.metric("Product", status['product_code'])
            
        except Exception as e:
            st.error(f"System status error: {e}")

# Sample data button
if st.sidebar.button("📝 Load Sample Application"):
    sample_data = {
        "household": {
            "address": "123 Main Street, Anytown, CA 90210",
            "zip_code": "90210",
            "home_ownership": "own"
        },
        "drivers": [
            {
                "name": "John Smith",
                "age": 35,
                "gender": "M",
                "marital_status": "married",
                "license_years": 18,
                "violations": [],
                "claims": []
            }
        ],
        "vehicles": [
            {
                "make": "Toyota",
                "model": "Camry",
                "year": 2021,
                "usage": "commuting",
                "annual_mileage": 12000
            }
        ]
    }
    st.session_state.sample_json = json.dumps(sample_data, indent=2)

# Main input area
st.markdown("### 📄 Insurance Application Data")
st.markdown("Paste your JSON application data below or use the sample data button in the sidebar.")

# Use session state for the text area if sample data was loaded
raw_json = st.text_area(
    "Application JSON", 
    value=st.session_state.get('sample_json', ''),
    height=240,
    help="Paste your insurance application JSON data here"
)

# Processing buttons
col1, col2, col3 = st.columns([2, 2, 1])

with col1:
    run_assessment = st.button("🚀 Run Assessment", type="primary")

with col2:
    if use_multi_agent:
        run_multi_agent = st.button("🔗 Run Multi-Agent Graph")
    else:
        run_multi_agent = False

with col3:
    clear_results = st.button("🗑️ Clear")

if clear_results:
    st.session_state.clear()
    st.rerun()

# Results area
if run_assessment or run_multi_agent:
    if not raw_json.strip():
        st.error("Please provide application JSON data")
    else:
        # Parse application data
        try:
            profile = parse_application(raw_json)
            
            if profile.get("issues"):
                st.warning("⚠️ **Application Issues Found:**\n" + "\n".join(f"• {issue}" for issue in profile["issues"]))
            
            # Create tabs for different processing methods
            if use_multi_agent and run_multi_agent:
                tab1, tab2, tab3, tab4 = st.tabs(["📊 Results", "🔍 Risk Assessment", "💰 Premium Calculation", "🔧 System Details"])
                
                # Run multi-agent system
                with st.spinner("Processing with multi-agent graph system..."):
                    start_time = time.time()
                    
                    try:
                        engine = create_rating_engine(product_code)
                        result = engine.process_application_with_graph(raw_json, product_code)
                        
                        processing_time = time.time() - start_time
                        
                        with tab1:
                            st.subheader("📊 Processing Results")
                            
                            # Status indicators
                            col1, col2, col3, col4 = st.columns(4)
                            with col1:
                                status_color = "🟢" if result.status == "completed" else "🔴"
                                st.metric("Status", f"{status_color} {result.status.title()}")
                            with col2:
                                st.metric("Processing Time", f"{processing_time:.2f}s")
                            with col3:
                                st.metric("Agents Executed", len(result.execution_order))
                            with col4:
                                st.metric("Session ID", result.session_id[-8:])
                            
                            # Execution flow
                            if result.execution_order:
                                st.subheader("🔄 Agent Execution Flow")
                                flow_text = " → ".join(result.execution_order)
                                st.code(flow_text, language="text")
                            
                            # Errors and warnings
                            if result.errors:
                                st.subheader("❌ Errors")
                                for error in result.errors:
                                    st.error(error)
                            
                            if result.warnings:
                                st.subheader("⚠️ Warnings")
                                for warning in result.warnings:
                                    st.warning(warning)
                        
                        with tab2:
                            st.subheader("🔍 Risk Assessment Results")
                            if result.risk_assessment:
                                risk_data = result.risk_assessment
                                
                                # Risk tier display
                                if "overall_risk_tier" in risk_data:
                                    tier = risk_data["overall_risk_tier"]
                                    tier_colors = {"LOW": "🟢", "MEDIUM": "🟡", "HIGH": "🟠", "VERY_HIGH": "🔴"}
                                    st.markdown(f"### Overall Risk Tier: {tier_colors.get(tier, '⚪')} {tier}")
                                
                                # Confidence score
                                if "confidence" in risk_data:
                                    confidence = risk_data["confidence"]
                                    st.progress(confidence)
                                    st.caption(f"Confidence: {confidence:.1%}")
                                
                                # Key factors
                                if "key_factors" in risk_data:
                                    st.subheader("Key Risk Factors")
                                    for factor in risk_data["key_factors"]:
                                        st.write(f"• {factor}")
                                
                                # Full risk assessment data
                                with st.expander("📋 Detailed Risk Assessment", expanded=False):
                                    st.json(risk_data)
                            else:
                                st.info("No risk assessment data available")
                        
                        with tab3:
                            st.subheader("💰 Premium Calculation")
                            if result.premium_calculation:
                                premium_data = result.premium_calculation
                                
                                # Premium display
                                col1, col2, col3 = st.columns(3)
                                
                                with col1:
                                    if "base_premium" in premium_data:
                                        st.metric("Base Premium", f"${premium_data['base_premium']:.2f}")
                                
                                with col2:
                                    if "total_premium" in premium_data:
                                        st.metric("Total Premium", f"${premium_data['total_premium']:.2f}")
                                
                                with col3:
                                    if "base_premium" in premium_data and "total_premium" in premium_data:
                                        savings = premium_data["base_premium"] - premium_data["total_premium"]
                                        st.metric("Savings", f"${savings:.2f}", delta=f"{savings:.2f}")
                                
                                # Premium breakdown
                                with st.expander("📊 Premium Breakdown", expanded=False):
                                    st.json(premium_data)
                            else:
                                st.info("No premium calculation data available")
                        
                        with tab4:
                            st.subheader("🔧 System Details")
                            
                            # Graph status
                            status = engine.get_graph_status()
                            st.json(status)
                            
                            # Full result data
                            with st.expander("📋 Complete Result Data", expanded=False):
                                result_dict = {
                                    "status": result.status,
                                    "session_id": result.session_id,
                                    "execution_order": result.execution_order,
                                    "execution_time_ms": result.execution_time_ms,
                                    "risk_profile": result.risk_profile,
                                    "product_definition": result.product_definition,
                                    "risk_assessment": result.risk_assessment,
                                    "premium_calculation": result.premium_calculation,
                                    "errors": result.errors,
                                    "warnings": result.warnings
                                }
                                st.json(result_dict)
                        
                    except Exception as e:
                        st.error(f"Multi-agent processing failed: {e}")
                        st.exception(e)
            
            elif run_assessment:
                # Single agent processing (fallback)
                tab1, tab2 = st.tabs(["📊 Assessment Results", "🔍 Parsed Profile"])
                
                with tab1:
                    st.subheader("📊 Single Agent Assessment")
                    
                    with st.spinner("Running single agent assessment..."):
                        try:
                            result = assess(profile, product_code=product_code)
                            
                            # Display result
                            st.subheader("Final Assessment")
                            st.json(result)
                            
                        except Exception as e:
                            st.error(f"Single agent assessment failed: {e}")
                            st.exception(e)
                
                with tab2:
                    st.subheader("🔍 Parsed Profile")
                    st.json(profile)
        
        except ValueError as e:
            st.error(f"❌ **JSON Parsing Error:** {e}")
        except Exception as e:
            st.error(f"❌ **Processing Error:** {e}")
            st.exception(e)

# Footer
st.markdown("---")
st.markdown("""
### 📖 About This Demo

This multi-agent insurance rating engine demonstrates:
- **Graph-based agent orchestration** using Strands Agents
- **Modular risk assessment** with specialized agents
- **Premium calculation** with detailed breakdowns
- **Real-time processing** with comprehensive error handling

**Architecture:**
1. **Orchestrator Agent** - Coordinates the workflow
2. **Product Definition Agent** - Defines risk factors and rules
3. **Risk Factor Reasoning Agent** - Assesses risk tiers
4. **Data Lookup Agent** - Provides mapping values  
5. **Premium Calculation Agent** - Calculates final premium

Built with ❤️ using [Strands Agents](https://strandsagents.com/) and Streamlit.
""")
