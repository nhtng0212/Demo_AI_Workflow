#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$DIR"

echo "Starting automated Git push sequence..."

git add .
echo "[1/3] Added files to staging area."

CURRENT_TIME=$(date "+%Y-%m-%d %H:%M:%S")
git commit -m "Auto-commit: $CURRENT_TIME"
echo "[2/3] Committed changes."

git push origin main
echo "[3/3] Pushed to origin/main successfully."