#!/bin/bash

echo "======================================"
echo "Installing Backend Dependencies"
echo "======================================"
echo ""

pip install flask flask-cors akshare pandas schedule requests

echo ""
echo "✓ Backend dependencies installed successfully."
echo ""
echo "Next steps:"
echo "  1. Copy .env.example to .env and configure your settings"
echo "  2. Start backend: cd backend && python server.py"
echo "  3. Start scheduler: cd backend && python scheduler.py"
