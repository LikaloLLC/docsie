#!/usr/bin/env python3
"""
Update translations for the new pricing page strings.
This script will help extract and prepare strings for translation.
"""

import os
import subprocess
from pathlib import Path

# New pricing strings that need translation
PRICING_STRINGS = [
    # Plan features
    "50 AI Writing Actions/month",
    "100 AI Writing Actions/month", 
    "500 AI Writing Actions/month",
    "1000 AI Writing Actions/month",
    "In-App Help Widget",
    "Multiple In-App Help Widgets",
    "AI Chatbot",
    "50 GB Storage",
    "100 GB Storage",
    "1 TB Storage",
    "90+ Team Accounts",
    "Unlimited Workspaces",
    "10 Documentation Portals",
    "10 Custom Domains",
    
    # Plan descriptions (already in trans blocks)
    "Perfect for small teams starting their documentation journey",
    "Ideal for growing teams needing advanced features",
    "For teams managing complex documentation at scale",
    "Custom solutions for enterprise-grade security and control",
]

def extract_translations():
    """Extract translations from the source files"""
    print("Extracting translation strings from source files...")
    
    # Run pybabel extract
    cmd = [
        'pybabel', 'extract',
        '-F', 'babel.cfg',
        '-o', 'locale/messages.pot',
        '--sort-output',
        '--add-comments=NOTE',
        'src/'
    ]
    
    subprocess.run(cmd, check=True)
    print("✅ Extracted strings to locale/messages.pot")

def update_language_files():
    """Update all language .po files with new strings"""
    languages = ['de', 'es', 'fr', 'ja', 'ko', 'pt_BR', 'pt_PT', 
                 'zh', 'ru', 'it', 'nl', 'sv', 'da', 'no', 'fi',
                 'pl', 'cs', 'hu', 'ro', 'tr', 'ar', 'he', 'th',
                 'vi', 'id', 'ms', 'hi', 'bn', 'ta', 'te']
    
    for lang in languages:
        print(f"Updating {lang}...")
        cmd = [
            'pybabel', 'update',
            '-i', 'locale/messages.pot',
            '-d', 'locale',
            '-l', lang
        ]
        
        try:
            subprocess.run(cmd, check=True)
            print(f"  ✅ Updated {lang}")
        except subprocess.CalledProcessError:
            print(f"  ❌ Failed to update {lang}")

def compile_translations():
    """Compile all translation files"""
    print("\nCompiling translations...")
    
    languages = ['de', 'es', 'fr', 'ja', 'ko', 'pt_BR', 'pt_PT', 
                 'zh', 'ru', 'it', 'nl', 'sv', 'da', 'no', 'fi',
                 'pl', 'cs', 'hu', 'ro', 'tr', 'ar', 'he', 'th',
                 'vi', 'id', 'ms', 'hi', 'bn', 'ta', 'te']
    
    for lang in languages:
        po_file = f'locale/{lang}/LC_MESSAGES/messages.po'
        if os.path.exists(po_file):
            cmd = ['pybabel', 'compile', '-d', 'locale', '-l', lang]
            subprocess.run(cmd, check=True)
            print(f"  ✅ Compiled {lang}")

def main():
    """Main function"""
    print("🔄 Updating pricing page translations\n")
    
    # Extract translations
    extract_translations()
    
    # Update language files
    print("\n📝 Updating language files...")
    update_language_files()
    
    # Compile translations
    compile_translations()
    
    print("\n✅ Translation files updated!")
    print("\nNext steps:")
    print("1. Review the new strings in locale/*/LC_MESSAGES/messages.po files")
    print("2. Run translation scripts to translate the new strings")
    print("3. Rebuild the site with: python main.py")
    
    # Also print the strings that need translation for reference
    print("\n📋 New strings added for translation:")
    for string in PRICING_STRINGS:
        print(f"  - {string}")

if __name__ == "__main__":
    main()