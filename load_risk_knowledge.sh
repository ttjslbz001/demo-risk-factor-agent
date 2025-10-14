#!/bin/bash

# Load Risk Factor Knowledge into Memory
# This script loads risk factor knowledge from markdown files into the memory system

echo "📚 Loading Risk Factor Knowledge into Memory..."
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

# Check if knowledge files exist
echo ""
echo "Checking knowledge files..."

if [ ! -f "docs/audit_file_demo/risk_factor_point_tables.md" ]; then
    echo "❌ Error: risk_factor_point_tables.md not found"
    exit 1
fi

if [ ! -f "docs/audit_file_demo/risk_factor_list_knowlege.md" ]; then
    echo "⚠️  Warning: risk_factor_list_knowlege.md not found"
fi

echo "✅ Knowledge files found"
echo ""

# Display information
echo "================================================================"
echo "📚 Risk Factor Knowledge Loader"
echo "================================================================"
echo ""
echo "This will load the following knowledge into memory:"
echo "  • Risk factor point tables (79 factors)"
echo "  • Risk factor list (70 factors)"
echo "  • Product domain knowledge"
echo "  • Coverage types and categories"
echo ""
echo "Target Agent: product_definition_agent"
echo "User ID: system"
echo ""
echo "================================================================"
echo ""

# Run the knowledge loader
python src/agents/load_risk_factor_knowledge.py

# Check exit status
if [ $? -eq 0 ]; then
    echo ""
    echo "================================================================"
    echo "✅ Knowledge loading completed successfully!"
    echo "================================================================"
    echo ""
    echo "Next steps:"
    echo "  1. Run the Product Agent app:"
    echo "     ./run_product_agent.sh"
    echo "  2. Or use the Streamlit app directly:"
    echo "     streamlit run src/streamlit_product_agent.py"
    echo ""
else
    echo ""
    echo "❌ Knowledge loading failed"
    echo "   Check the error messages above"
    exit 1
fi

