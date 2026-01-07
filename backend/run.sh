#!/bin/bash

# Gomoku Flask API Server Startup Script

echo "Starting Gomoku Flask API Server..."
echo "======================================"

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python3 is not installed. Please install Python3 to continue."
    exit 1
fi

# Check if virtual environment exists, create if not
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install/upgrade dependencies
echo "Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Check if Flask is installed
if ! python3 -c "import flask" &> /dev/null; then
    echo "Error: Flask installation failed. Please check requirements.txt"
    exit 1
fi

# Run the server
echo ""
echo "Starting Flask development server..."
echo "Server will run at: http://localhost:5000"
echo "Press Ctrl+C to stop the server"
echo ""
echo "To test the server, open another terminal and run:"
echo "  python test_api.py"
echo ""
echo "Or use curl to test endpoints:"
echo "  curl http://localhost:5000/"
echo "  curl -X POST http://localhost:5000/api/new-game -H \"Content-Type: application/json\" -d '{}'"
echo ""

python app.py