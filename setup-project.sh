#!/bin/bash

# Exit immediately if a command fails
set -e

echo "📂 Creating folders: agent/, backend/, frontend/"
mkdir -p agent backend frontend

echo "✅ Empty project folders created successfully!"


echo "✅ Done setting up project structure."

echo "🧹 Updating __init__.py files..."
touch agent/__init__.py
touch backend/__init__.py

echo "🎉 Project structure is ready!"
