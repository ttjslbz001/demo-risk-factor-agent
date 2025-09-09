import os
import json
import streamlit as st

# Ensure project root is on sys.path so `from src...` works when run via Streamlit
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.utils.data_parser import parse_application
from src.agents.risk_factor_agent import assess

st.set_page_config(page_title="Insurance Risk Factor Agent", layout="wide")

st.title("Insurance Risk Factor Agent (Demo)")

st.sidebar.header("Configuration")
product_code = st.sidebar.selectbox(
    "Product", ["Monthly-Comfort", "Monthly-Economy", "Monthly-Turbo"], index=0
)

st.markdown("Paste your JSON application:")
raw_json = st.text_area("Application JSON", height=240)

col1, col2 = st.columns(2)
with col1:
    if st.button("Run Assessment"):
        try:
            profile = parse_application(raw_json)
        except ValueError as e:
            st.error(f"JSON error: {e}")
        else:
            if profile.get("issues"):
                st.warning("\n".join(profile["issues"]))
            try:
                result = assess(profile, product_code=product_code)
                st.subheader("Final Assessment")
                st.json({
                    "product_code": result.get("product_code"),
                    "overall_risk_tier": result.get("overall_risk_tier"),
                    "key_factors": result.get("key_factors", []),
                    "confidence": result.get("confidence"),
                })
            except Exception as e:
                st.error(f"Agent error: {e}")

with col2:
    st.subheader("Reasoning Steps")
    if raw_json.strip():
        try:
            profile = parse_application(raw_json)
            # Show a preview of parsed structure
            st.expander("Parsed Profile", expanded=False).json(profile)
        except Exception:
            pass
    # Placeholder for reasoning steps after run; advise user to run first
    st.info("Click 'Run Assessment' to view reasoning steps.")
