#!/bin/bash

echo "=========================================="
echo "Memory System Fix - Diagnostic Test"
echo "=========================================="
echo ""
echo "This script will:"
echo "1. Run diagnostic tests on the memory system"
echo "2. Help identify any remaining issues"
echo ""

# Change to script directory
cd "$(dirname "$0")"

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    echo "Activating virtual environment..."
    source venv/bin/activate
fi

echo ""
echo "Running diagnostic test..."
echo "=========================================="
python src/memory/test_memory_debug.py

echo ""
echo "=========================================="
echo "Test complete!"
echo ""
echo "Next steps:"
echo "1. If the test passed, restart the Streamlit app:"
echo "   streamlit run src/memory/memory_manager_app.py"
echo ""
echo "2. If the test failed, check the error messages above"
echo "=========================================="

