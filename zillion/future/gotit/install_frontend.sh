#!/bin/bash

echo "======================================"
echo "Installing Frontend Dependencies"
echo "======================================"
echo ""

cd frontend
npm install

echo ""
echo "✓ Frontend dependencies installed successfully."
echo ""
echo "To start the frontend dev server:"
echo "  cd frontend && npm run dev"
