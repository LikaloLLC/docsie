#!/usr/bin/env python3
"""
Fix yaml_trans references in component templates
"""

import os
import re
from pathlib import Path

def fix_yaml_trans_references(file_path):
    """Remove yaml_trans references from a template file"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if file has yaml_trans references
    if 'yaml_trans.translate_yaml_string' not in content:
        return False
    
    print(f"Fixing {file_path}")
    
    # Remove the import line if it exists
    content = re.sub(r'{% import [\'"]yaml_translation_helpers\.html[\'"] as yaml_trans %}\n?', '', content)
    
    # Replace all yaml_trans.translate_yaml_string calls with direct variable access
    content = re.sub(r'{{ yaml_trans\.translate_yaml_string\(([^)]+)\) }}', r'{{ \1 }}', content)
    
    # Write back
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return True

def main():
    components_dir = Path('src/.templates/components')
    supplementary_template = Path('src/.templates/supplementary_page_v2.html')
    
    fixed_count = 0
    
    # Fix component files
    for component_file in components_dir.rglob('*.html'):
        if fix_yaml_trans_references(component_file):
            fixed_count += 1
    
    # Fix supplementary template
    if supplementary_template.exists():
        if fix_yaml_trans_references(supplementary_template):
            fixed_count += 1
    
    print(f"\n✅ Fixed {fixed_count} files")

if __name__ == "__main__":
    main()