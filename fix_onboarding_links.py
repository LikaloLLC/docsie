#!/usr/bin/env python3
"""
Fix all /onboarding/ links in YAML files to use the full URL
"""
import os
import re

def fix_onboarding_links_in_file(filepath):
    """Fix onboarding links in a single file"""
    fixed = False
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Replace relative /onboarding/ URLs with full URL
        pattern = r'url:\s*/onboarding/'
        replacement = 'url: https://app.docsie.io/onboarding/'
        
        new_content = re.sub(pattern, replacement, content)
        
        if new_content != content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            fixed = True
            print(f"✅ Fixed: {filepath}")
        
        return fixed
    except Exception as e:
        print(f"❌ Error processing {filepath}: {e}")
        return False

def main():
    """Find and fix all YAML files with onboarding links"""
    data_dir = 'src/.data'
    total_fixed = 0
    
    print("🔍 Searching for YAML files with /onboarding/ links...")
    print()
    
    # Walk through all directories in .data
    for root, dirs, files in os.walk(data_dir):
        for filename in files:
            if filename.endswith('.yaml'):
                filepath = os.path.join(root, filename)
                
                # Check if file contains /onboarding/
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        if '/onboarding/' in f.read():
                            if fix_onboarding_links_in_file(filepath):
                                total_fixed += 1
                except Exception as e:
                    print(f"❌ Error reading {filepath}: {e}")
    
    print()
    print(f"✨ Fixed {total_fixed} files")
    print()
    print("Next steps:")
    print("1. Review the changes with: git diff")
    print("2. Regenerate the site: sh ./build_multilingual.sh")
    print("3. Test locally: sh start.sh")

if __name__ == "__main__":
    main()