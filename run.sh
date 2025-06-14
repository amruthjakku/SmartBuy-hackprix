#!/bin/bash

# SmartShop - Quick Start Script for Hackathon

echo "🛍️ Starting SmartShop - Product Discovery Platform"
echo "============================================="

# Activate virtual environment
echo "📦 Activating virtual environment..."
source venv/bin/activate

# Check if requirements are installed
echo "🔍 Checking dependencies..."
pip list | grep streamlit > /dev/null
if [ $? -ne 0 ]; then
    echo "📥 Installing dependencies..."
    pip install -r requirements.txt
fi

# Start the Streamlit app
echo "🚀 Starting the application..."
echo "💡 The app will open in your browser at: http://localhost:8501"
echo "🛑 Press Ctrl+C to stop the application"
echo ""

streamlit run app.py