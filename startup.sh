#!/bin/bash

# Startup script for Nova AI application on Render.com
# This script ensures proper environment setup before starting the application

echo "===== Starting Nova AI application setup ====="

# Print environment information
echo "Python version:"
python --version

# Ensure correct werkzeug version is installed
echo "\nInstalling werkzeug==2.0.3..."
pip install werkzeug==2.0.3

# Pin setuptools to avoid pkg_resources deprecation warning
echo "\nInstalling setuptools<81.0.0..."
pip install "setuptools<81.0.0"

# Run pre-start checks
echo "\nRunning pre-start checks..."
python pre_start.py

# Start the application with gunicorn
echo "\n===== Starting application with gunicorn ====="
exec gunicorn app:app