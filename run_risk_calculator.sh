#!/bin/bash

# Risk Calculator Streamlit App Runner
# This script runs the risk calculation table generator web app

echo "🚀 Starting Risk Calculator Streamlit App..."
echo ""

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    echo "📦 Activating virtual environment..."
    source venv/bin/activate
fi

# Run the Streamlit app
echo "🌐 Launching web application..."
echo "📍 URL will open in your browser automatically"
echo ""
streamlit run src/streamlit_risk_calculator.py




