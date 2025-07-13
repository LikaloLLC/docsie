#!/bin/bash

echo "=== Starting cleanup before deployment ==="
echo "Initial disk usage:"
df -h

# Remove unnecessary files that aren't needed for deployment
echo "Removing development files..."
find . -name "*.pyc" -delete
find . -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true
find . -name ".pytest_cache" -type d -exec rm -rf {} + 2>/dev/null || true
find . -name "*.log" -delete
find . -name ".DS_Store" -delete

# Remove source files that aren't needed for static site
echo "Removing source files not needed for deployment..."
rm -rf venv/
rm -rf node_modules/
rm -rf .git/objects/pack/tmp_*
rm -rf .git/lfs/
rm -rf src/.data/_*  # Remove translated YAML source files
rm -rf locale/  # Remove translation files
rm -rf backups/  # Remove any backup directories

# Remove Python scripts (keeping only static HTML/CSS/JS)
echo "Removing build scripts..."
find . -name "*.py" -not -path "./.github/*" -delete
rm -f requirements.txt
rm -f *.sh
rm -f *.cfg
rm -f *.yaml -not -path "./.github/*"
rm -f *.yml -not -path "./.github/*"

# Clean git cache
echo "Cleaning git cache..."
git reflog expire --expire=now --all
git gc --prune=now --aggressive

echo "=== Cleanup complete ==="
echo "Final disk usage:"
df -h
echo "Repository size:"
du -sh .