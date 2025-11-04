#!/bin/bash

# Quick Start Script - People Analytics Turnover System

echo "===================================="
echo " People Analytics - Quick Start"
echo "===================================="

# Check dependencies
echo "Checking dependencies..."
which python3 > /dev/null || { echo "Python 3 required"; exit 1; }
which node > /dev/null || { echo "Node.js required"; exit 1; }
which psql > /dev/null || { echo "PostgreSQL required"; exit 1; }

# Setup database
echo "Setting up database..."
python3 scripts/setup_database.py

# Install backend dependencies
echo "Installing backend dependencies..."
cd backend
pip3 install -r requirements.txt
cd ..

# Install frontend dependencies  
echo "Installing frontend dependencies..."
cd frontend
npm install
cd ..

echo "Setup completed!"
echo ""
echo "To run the system:"
echo "1. Backend: cd backend && python -m uvicorn main:app --reload"
echo "2. Frontend: cd frontend && npm start"
echo "3. Access: http://localhost:4200"
echo ""
echo "To run with Docker: docker-compose up -d"
echo "===================================="
