#!/bin/bash
# AI Employee System Startup Script
# Starts all watchers with process monitoring

echo "=========================================="
echo "AI Employee System - Starting"
echo "=========================================="
echo ""

# Check if Python is available
if ! command -v python &> /dev/null; then
    echo "[ERROR] Python not found. Please install Python 3.8+"
    exit 1
fi

# Check if required directories exist
if [ ! -d "AI_Employee_Vault" ]; then
    echo "[ERROR] AI_Employee_Vault directory not found"
    exit 1
fi

if [ ! -d "watchers" ]; then
    echo "[ERROR] watchers directory not found"
    exit 1
fi

echo "[OK] Prerequisites checked"
echo ""

# Start process manager
echo "Starting AI Employee Process Manager..."
echo "This will start and monitor:"
echo "  - Gmail Watcher"
echo "  - LinkedIn Watcher"
echo ""
echo "Press Ctrl+C to stop all processes"
echo ""

python process_manager.py
