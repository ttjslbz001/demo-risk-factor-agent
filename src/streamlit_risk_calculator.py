import streamlit as st
import json
from typing import Dict, Any, List
import sys
import os

# Add parent directory to path to import from utils
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.risk_subject_ite import (
    risk_subject_iter, 
    prepare_risk_calculation_tables,
    AZ_HARDCODE_RISK_SUBJECT_MAP,
    RiskSubjectType,
    RiskCalculationTable
)

# Page configuration
st.set_page_config(
    page_title="Risk Calculation Table Generator",
    page_icon="📊",
    layout="wide"
)

# Title and description
st.title("📊 Risk Calculation Table Generator")
st.markdown("""
This app generates risk calculation tables from an insurance application JSON.
Paste your application JSON below to see all the risk calculation tables.
""")

# Sidebar with information
with st.sidebar:
    st.header("ℹ️ Information")
    st.markdown("""
    **How to use:**
    1. Paste your application JSON in the text area
    2. Click "Generate Risk Calculation Tables"
    3. View the results below
    
    **Risk Subject Types:**
    - 🚗 **Vehicle**: Vehicle-specific risk factors
    - 👤 **Driver**: Driver-specific risk factors
    - 🏠 **Household**: Household-specific risk factors
    """)
    
    # Load sample data button
    if st.button("📄 Load Sample Data"):
        sample_path = os.path.join(
            os.path.dirname(__file__),
            '../docs/insurance_risk_factor_agent/demo_application/economy.json'
        )
        try:
            with open(sample_path, 'r') as f:
                sample_data = f.read()
            st.session_state['sample_data'] = sample_data
            st.success("Sample data loaded! Paste it in the main area.")
        except Exception as e:
            st.error(f"Error loading sample data: {str(e)}")

# Main content area
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📝 Input: Application JSON")
    
    # Check if sample data is loaded
    default_text = ""
    if 'sample_data' in st.session_state:
        default_text = st.session_state['sample_data']
        del st.session_state['sample_data']
    
    application_json = st.text_area(
        "Paste your application JSON here:",
        height=400,
        placeholder='{\n  "riskProfile": {\n    "drivers": [...],\n    "vehicles": [...]\n  }\n}',
        value=default_text
    )

with col2:
    st.subheader("📊 Risk Factor Statistics")
    
    # Display risk factor distribution
    driver_factors = sum(1 for v in AZ_HARDCODE_RISK_SUBJECT_MAP.values() if v in ['driver', 'household'])
    vehicle_factors = sum(1 for v in AZ_HARDCODE_RISK_SUBJECT_MAP.values() if v == 'vehicle')
    
    col_a, col_b, col_c = st.columns(3)
    with col_a:
        st.metric("Total Risk Factors", len(AZ_HARDCODE_RISK_SUBJECT_MAP))
    with col_b:
        st.metric("Driver Factors", driver_factors)
    with col_c:
        st.metric("Vehicle Factors", vehicle_factors)

# Generate button
if st.button("🚀 Generate Risk Calculation Tables", type="primary"):
    if not application_json.strip():
        st.error("⚠️ Please paste an application JSON first!")
    else:
        try:
            # Parse JSON
            with st.spinner("Parsing JSON..."):
                application = json.loads(application_json)
            
            # Validate structure
            if 'riskProfile' not in application:
                st.error("⚠️ Invalid JSON structure: 'riskProfile' key not found!")
                st.stop()
            
            if 'drivers' not in application['riskProfile'] or 'vehicles' not in application['riskProfile']:
                st.error("⚠️ Invalid JSON structure: 'drivers' or 'vehicles' not found in riskProfile!")
                st.stop()
            
            # Get dimensions and create tables
            with st.spinner("Generating risk calculation tables..."):
                ris_dimension = risk_subject_iter(AZ_HARDCODE_RISK_SUBJECT_MAP)
                risk_calculation_tables = prepare_risk_calculation_tables(application, ris_dimension)
            
            st.success(f"✅ Successfully generated {len(risk_calculation_tables)} risk calculation tables!")
            
            # Display summary
            st.divider()
            st.header("📈 Summary")
            
            num_drivers = len(application['riskProfile']['drivers'])
            num_vehicles = len(application['riskProfile']['vehicles'])
            driver_tables = sum(1 for t in risk_calculation_tables if t.risk_subject_type == RiskSubjectType.DRIVER)
            vehicle_tables = sum(1 for t in risk_calculation_tables if t.risk_subject_type == RiskSubjectType.VEHICLE)
            
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Total Tables", len(risk_calculation_tables))
            with col2:
                st.metric("Driver Tables", driver_tables)
            with col3:
                st.metric("Vehicle Tables", vehicle_tables)
            with col4:
                st.metric("Drivers × Vehicles", f"{num_drivers} × {num_vehicles}")
            
            # Display breakdown
            st.info(f"""
            **Calculation Breakdown:**
            - Driver Tables: {driver_tables} = {len(ris_dimension['driver'])} driver dimensions × {num_drivers} drivers
            - Vehicle Tables: {vehicle_tables} = {len(ris_dimension['vehicle'])} vehicle dimensions × {num_vehicles} vehicles
            """)
            
            # Display tables
            st.divider()
            st.header("📋 Risk Calculation Tables")
            
            # Tabs for different views
            tab1, tab2, tab3 = st.tabs(["📊 All Tables", "👤 Driver Tables", "🚗 Vehicle Tables"])
            
            with tab1:
                st.subheader(f"All Risk Calculation Tables ({len(risk_calculation_tables)})")
                
                # Create a table view
                table_data = []
                for idx, table in enumerate(risk_calculation_tables, 1):
                    subject_id = table.risk_subject.get('id', 'N/A')
                    table_data.append({
                        "#": idx,
                        "Type": table.risk_subject_type.value.upper(),
                        "Risk Dimension": table.risk_dimension,
                        "Subject ID": subject_id
                    })
                
                st.dataframe(
                    table_data,
                    use_container_width=True,
                    height=400
                )
                
                # Download button
                json_output = json.dumps([
                    {
                        "index": idx,
                        "type": table.risk_subject_type.value,
                        "risk_dimension": table.risk_dimension,
                        "subject_id": table.risk_subject.get('id', 'N/A')
                    }
                    for idx, table in enumerate(risk_calculation_tables, 1)
                ], indent=2)
                
                st.download_button(
                    label="📥 Download as JSON",
                    data=json_output,
                    file_name="risk_calculation_tables.json",
                    mime="application/json"
                )
            
            with tab2:
                driver_tables_list = [t for t in risk_calculation_tables if t.risk_subject_type == RiskSubjectType.DRIVER]
                st.subheader(f"Driver Risk Calculation Tables ({len(driver_tables_list)})")
                
                table_data = []
                for idx, table in enumerate(driver_tables_list, 1):
                    driver_id = table.risk_subject.get('id', 'N/A')
                    table_data.append({
                        "#": idx,
                        "Risk Dimension": table.risk_dimension,
                        "Driver ID": driver_id,
                        "Driver Name": f"{table.risk_subject.get('firstName', '')} {table.risk_subject.get('lastName', '')}".strip()
                    })
                
                st.dataframe(
                    table_data,
                    use_container_width=True,
                    height=400
                )
            
            with tab3:
                vehicle_tables_list = [t for t in risk_calculation_tables if t.risk_subject_type == RiskSubjectType.VEHICLE]
                st.subheader(f"Vehicle Risk Calculation Tables ({len(vehicle_tables_list)})")
                
                table_data = []
                for idx, table in enumerate(vehicle_tables_list, 1):
                    vin = table.risk_subject.get('id', 'N/A')
                    table_data.append({
                        "#": idx,
                        "Risk Dimension": table.risk_dimension,
                        "VIN": vin,
                        "Make/Model": f"{table.risk_subject.get('make', '')} {table.risk_subject.get('model', '')}".strip()
                    })
                
                st.dataframe(
                    table_data,
                    use_container_width=True,
                    height=400
                )
            
            # Detailed view expander
            st.divider()
            with st.expander("🔍 View Detailed Table Information"):
                st.markdown("### Detailed Risk Calculation Tables")
                
                # Search/filter
                search_term = st.text_input("🔍 Search by risk dimension name:")
                
                filtered_tables = risk_calculation_tables
                if search_term:
                    filtered_tables = [
                        t for t in risk_calculation_tables 
                        if search_term.lower() in t.risk_dimension.lower()
                    ]
                    st.info(f"Found {len(filtered_tables)} tables matching '{search_term}'")
                
                # Display first 50 tables in detail
                display_limit = min(50, len(filtered_tables))
                st.warning(f"Displaying first {display_limit} of {len(filtered_tables)} tables")
                
                for idx, table in enumerate(filtered_tables[:display_limit], 1):
                    with st.container():
                        col1, col2 = st.columns([1, 3])
                        with col1:
                            st.markdown(f"**Table #{idx}**")
                            st.markdown(f"Type: **{table.risk_subject_type.value.upper()}**")
                        with col2:
                            st.markdown(f"**Risk Dimension:** `{table.risk_dimension}`")
                            st.markdown(f"**Subject ID:** `{table.risk_subject.get('id', 'N/A')}`")
                        st.divider()
                        
        except json.JSONDecodeError as e:
            st.error(f"⚠️ Invalid JSON format: {str(e)}")
        except Exception as e:
            st.error(f"⚠️ Error processing application: {str(e)}")
            st.exception(e)

# Footer
st.divider()
st.markdown("""
<div style='text-align: center; color: #666; padding: 20px;'>
    <p>Risk Calculation Table Generator v1.0</p>
    <p>Built with Streamlit 🎈</p>
</div>
""", unsafe_allow_html=True)



