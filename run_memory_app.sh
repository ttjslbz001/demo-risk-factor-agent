#!/bin/bash

# Memory Manager App Launcher
# This script launches the Streamlit Memory Manager application

echo "🧠 Starting Agent Memory Manager..."
echo "=================================="
echo ""

# Change to the src/memory directory
cd "$(dirname "$0")/src/memory"

# Check if test_memory.py exists
if [ ! -f "test_memory.py" ]; then
    echo "❌ Error: test_memory.py not found in src/memory directory"
    exit 1
fi

# Check if memory_manager_app.py exists
if [ ! -f "memory_manager_app.py" ]; then
    echo "❌ Error: memory_manager_app.py not found in src/memory directory"
    exit 1
fi

# Check if streamlit is installed
if ! command -v streamlit &> /dev/null; then
    echo "❌ Error: streamlit is not installed"
    echo "Please install it with: pip install streamlit"
    exit 1
fi

echo "✅ All checks passed"
echo "🚀 Launching Memory Manager App..."
echo ""
echo "The app will open in your default browser at http://localhost:8501"
echo "Press Ctrl+C to stop the server"
echo ""

# Run the Streamlit app
streamlit run memory_manager_app.py

