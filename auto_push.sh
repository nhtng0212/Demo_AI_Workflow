#!/bin/bash

# Navigate to the directory containing this script
# This ensures git commands run in the correct repository folder
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$DIR"

echo "Starting automated Git push sequence..."

# Add all changes to staging
git add .
echo "[1/3] Added files to staging area."

# Commit changes with a timestamp
# Note: $() executes a command inside a string
CURRENT_TIME=$(date "+%Y-%m-%d %H:%M:%S")
git commit -m "Auto-commit: $CURRENT_TIME"
echo "[2/3] Committed changes."

# Push to the remote repository (main branch)
git push origin main
echo "[3/3] Pushed to origin/main successfully."