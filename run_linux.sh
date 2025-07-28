#!/bin/bash

echo "==============================================="
echo "    Titan Viewer Deployment (Linux)"
echo "==============================================="
echo ""
echo "Starting deployment process..."
echo ""

# Make sure we have python3
if ! command -v python3 &> /dev/null; then
    echo "ERROR: python3 is not installed"
    echo "Please install python3 first:"
    echo "  sudo apt-get update && sudo apt-get install python3 python3-pip"
    exit 1
fi

# Run the deployment script
python3 deploy_viewer_system.py

echo ""
echo "==============================================="
echo "Deployment complete!"
echo "==============================================="