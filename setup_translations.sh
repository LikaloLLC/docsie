#!/bin/bash

echo "🚀 Setting up Docsie Translation System"

# Install requirements
echo "📦 Installing translation requirements..."
pip install -r requirements_translation.txt

# Make translation script executable
chmod +x translation_system.py

# Extract strings
echo "🔍 Extracting translatable strings..."
python translation_system.py extract

# Initialize enabled languages from config
echo "🌍 Initializing enabled languages from config..."
python translation_system.py init

# Show available commands
echo "
✅ Translation system setup complete!

Configuration is managed via translation_config.yaml

Available commands:
  python translation_system.py extract                    # Extract strings
  python translation_system.py init                       # Initialize enabled languages
  python translation_system.py translate                  # Translate all enabled languages
  python translation_system.py compile                    # Compile all languages
  python translation_system.py setup --all-enabled        # Complete setup for all enabled
  python translation_system.py list-languages             # Show all languages

Environment variables:
  Add ANTHROPIC_API_KEY='your-api-key-here' to .env file

Example usage:
  # Translate all enabled languages
  python translation_system.py translate

  # Complete setup for all enabled languages  
  python translation_system.py setup --all-enabled

  # Translate specific languages
  python translation_system.py translate es fr de

  # Check configuration
  python translation_system.py list-languages
"