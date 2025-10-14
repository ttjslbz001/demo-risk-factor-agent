#!/bin/bash

# Run Product Definition Agent Streamlit App
# This script launches the memory-based product definition agent interface

echo "🧠 Starting Memory-Based Product Definition Agent..."
echo "================================================================"
echo ""

# Check if virtual environment exists
if [ -d "venv" ]; then
    echo "✅ Virtual environment found"
    source venv/bin/activate
else
    echo "⚠️  Warning: Virtual environment not found at ./venv"
    echo "   The script will continue but you may need to activate it manually"
fi

# Check if required packages are installed
echo ""
echo "Checking dependencies..."
python -c "import streamlit" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "❌ Error: streamlit not installed"
    echo "   Install with: pip install streamlit"
    exit 1
fi

python -c "from src.memory.test_memory import MemoryLayer" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "⚠️  Warning: Memory layer not available"
    echo "   The agent will run without memory features"
fi

echo "✅ Dependencies OK"
echo ""

# Display information
echo "================================================================"
echo "📚 Product Definition Agent - Memory-Based"
echo "================================================================"
echo ""
echo "Features:"
echo "  • Ask questions about risk factors and products"
echo "  • Search knowledge base using semantic search"
echo "  • View product definitions and risk factors"
echo "  • Monitor learning and memory statistics"
echo ""
echo "💡 First time running?"
echo "   1. Load knowledge first: python src/agents/load_risk_factor_knowledge.py"
echo "   2. Then run this app"
echo ""
echo "================================================================"
echo ""

# Run the Streamlit app
streamlit run src/streamlit_product_agent.py \
    --server.port 8502 \
    --server.headless true \
    --browser.serverAddress localhost

