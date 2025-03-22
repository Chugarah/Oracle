#!/bin/bash

# Activate the virtual environment and run the script
source downloader/script/venv/oracle-downloader/bin/activate
PYTHONPATH="$PYTHONPATH:$(pwd)/downloader/script" python downloader/script/main.py 