#!/usr/bin/env python3
"""Fix /demo links to have trailing slashes"""

import os
import re

def fix_demo_links(filepath):
    """Fix /demo links in a file"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Pattern to match url: /demo (without trailing slash)
    pattern = r'(url:\s*/demo)(?!/)(\s|$)'
    
    # Find all matches
    matches = re.findall(pattern, content)
    if matches:
        print(f"Found {len(matches)} /demo URLs without trailing slash in {filepath}")
        # Replace with trailing slash
        new_content = re.sub(pattern, r'\1/\2', content)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        return len(matches)
    return 0

# Process all YAML files
total_fixed = 0
for root, dirs, files in os.walk('src/.data'):
    for file in files:
        if file.endswith('.yaml') or file.endswith('.yml'):
            filepath = os.path.join(root, file)
            total_fixed += fix_demo_links(filepath)

print(f"\nTotal /demo URLs fixed: {total_fixed}")