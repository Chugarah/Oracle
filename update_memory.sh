#!/bin/bash

# Enhanced wrapper script for the memory update system

# Check if we need to create a new template
if [ "$1" = "--new" ] || [ "$1" = "-n" ]; then
    # Get optional filename
    if [ -n "$2" ]; then
        FILENAME="$2"
    else
        # Generate a timestamp-based filename
        TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
        FILENAME="update_${TIMESTAMP}.md"
    fi
    
    # Create the file from template
    cp .memory/inputs/template.md .memory/inputs/${FILENAME}
    echo "Created new update file: .memory/inputs/${FILENAME}"
    
    # Open in default editor if available
    if [ -n "$EDITOR" ]; then
        $EDITOR .memory/inputs/${FILENAME}
    else
        echo "Edit this file and then run:"
        echo "./update_memory.sh .memory/inputs/${FILENAME}"
    fi
    exit 0
fi

# Check if we need to list existing input files
if [ "$1" = "--list" ] || [ "$1" = "-l" ]; then
    echo "Available memory update input files:"
    ls -l .memory/inputs/ | grep -v "README\|template" | awk '{print $9, "("$5" bytes, created: "$6,$7,$8")"}'
    exit 0
fi

# Check if we need to show help
if [ "$1" = "--help" ] || [ "$1" = "-h" ]; then
    echo "Memory Update System"
    echo ""
    echo "Usage:"
    echo "  ./update_memory.sh                      - Interactive mode (paste update text)"
    echo "  ./update_memory.sh [file]               - Process specific file"
    echo "  ./update_memory.sh --new [name]         - Create new update from template"
    echo "  ./update_memory.sh --list               - List available input files"
    echo "  ./update_memory.sh --help               - Show this help"
    echo ""
    echo "Examples:"
    echo "  ./update_memory.sh                      - Paste update text interactively"
    echo "  ./update_memory.sh .memory/inputs/my_update.md - Process a specific file"
    echo "  ./update_memory.sh --new                - Create new update with timestamp name"
    echo "  ./update_memory.sh --new feature_x.md   - Create new update with specific name"
    exit 0
fi

# Pass arguments to the main script
.memory/tools/update_memory.sh "$@" 