#!/bin/bash

# Install UV if not already installed
if ! command -v uv &> /dev/null; then
    echo "Installing UV package manager..."
    pip install uv
fi

# Create virtual environment
echo "Creating oracle-downloader virtual environment..."
uv venv downloader/script/venv/oracle-downloader

# Activate the environment and install dependencies
echo "Installing dependencies..."
source downloader/script/venv/oracle-downloader/bin/activate
uv pip install -r downloader/script/requirements.txt

echo "Environment setup complete. Activate with:"
echo "source downloader/script/venv/oracle-downloader/bin/activate" 