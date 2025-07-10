#!/usr/bin/env python3
"""
Update component templates to use translation helpers for YAML content.
"""

import os
import re
from pathlib import Path

def update_component_template(template_path):
    """Update a component template to use translation helpers."""
    
    with open(template_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if already has translation import
    if 'yaml_trans' in content:
        print(f"  ⏭️  Already updated: {template_path}")
        return False
    
    # Add import at the beginning if not exists
    if '{% import' not in content or 'yaml_translation_helpers' not in content:
        content = '{% import "yaml_translation_helpers.html" as yaml_trans %}\n' + content
    
    # Replace common patterns
    patterns = [
        # Simple variable replacements
        (r'{{ section\.title }}', '{{ yaml_trans.translate_yaml_string(section.title) }}'),
        (r'{{ section\.subtitle }}', '{{ yaml_trans.translate_yaml_string(section.subtitle) }}'),
        (r'{{ section\.description }}', '{{ yaml_trans.translate_yaml_string(section.description) }}'),
        (r'{{ section\.badge }}', '{{ yaml_trans.translate_yaml_string(section.badge) }}'),
        (r'{{ section\.heading }}', '{{ yaml_trans.translate_yaml_string(section.heading) }}'),
        (r'{{ section\.text }}', '{{ yaml_trans.translate_yaml_string(section.text) }}'),
        (r'{{ section\.label }}', '{{ yaml_trans.translate_yaml_string(section.label) }}'),
        
        # Button text
        (r'{{ section\.cta_text }}', '{{ yaml_trans.translate_yaml_string(section.cta_text) }}'),
        (r'{{ section\.button_text }}', '{{ yaml_trans.translate_yaml_string(section.button_text) }}'),
        (r'{{ section\.primary_cta\.text }}', '{{ yaml_trans.translate_yaml_string(section.primary_cta.text) }}'),
        (r'{{ section\.secondary_cta\.text }}', '{{ yaml_trans.translate_yaml_string(section.secondary_cta.text) }}'),
        
        # Item properties in loops
        (r'{{ item\.title }}', '{{ yaml_trans.translate_yaml_string(item.title) }}'),
        (r'{{ item\.description }}', '{{ yaml_trans.translate_yaml_string(item.description) }}'),
        (r'{{ item\.text }}', '{{ yaml_trans.translate_yaml_string(item.text) }}'),
        (r'{{ item\.label }}', '{{ yaml_trans.translate_yaml_string(item.label) }}'),
        (r'{{ item\.name }}', '{{ yaml_trans.translate_yaml_string(item.name) }}'),
        (r'{{ item\.role }}', '{{ yaml_trans.translate_yaml_string(item.role) }}'),
        (r'{{ item\.content }}', '{{ yaml_trans.translate_yaml_string(item.content) }}'),
        (r'{{ item\.question }}', '{{ yaml_trans.translate_yaml_string(item.question) }}'),
        (r'{{ item\.answer }}', '{{ yaml_trans.translate_yaml_string(item.answer) }}'),
        
        # Feature items
        (r'{{ feature\.title }}', '{{ yaml_trans.translate_yaml_string(feature.title) }}'),
        (r'{{ feature\.description }}', '{{ yaml_trans.translate_yaml_string(feature.description) }}'),
        (r'{{ feature\.text }}', '{{ yaml_trans.translate_yaml_string(feature.text) }}'),
        
        # Stat items
        (r'{{ stat\.label }}', '{{ yaml_trans.translate_yaml_string(stat.label) }}'),
        (r'{{ stat\.number }}', '{{ yaml_trans.translate_yaml_string(stat.number) }}'),
        (r'{{ stat\.description }}', '{{ yaml_trans.translate_yaml_string(stat.description) }}'),
        
        # Benefit items
        (r'{{ benefit\.title }}', '{{ yaml_trans.translate_yaml_string(benefit.title) }}'),
        (r'{{ benefit\.description }}', '{{ yaml_trans.translate_yaml_string(benefit.description) }}'),
        
        # Review items
        (r'{{ review\.content }}', '{{ yaml_trans.translate_yaml_string(review.content) }}'),
        (r'{{ review\.author }}', '{{ yaml_trans.translate_yaml_string(review.author) }}'),
        (r'{{ review\.role }}', '{{ yaml_trans.translate_yaml_string(review.role) }}'),
        (r'{{ review\.company }}', '{{ yaml_trans.translate_yaml_string(review.company) }}'),
    ]
    
    # Apply replacements
    original_content = content
    for pattern, replacement in patterns:
        content = re.sub(pattern, replacement, content)
    
    # Write back if changed
    if content != original_content:
        with open(template_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"  ✅ Updated: {template_path}")
        return True
    else:
        print(f"  ℹ️  No changes needed: {template_path}")
        return False

def update_all_components():
    """Update all component templates."""
    components_dir = 'src/.templates/components'
    updated_count = 0
    
    print("🔄 Updating component templates for translation support...\n")
    
    for component_dir in os.listdir(components_dir):
        component_path = os.path.join(components_dir, component_dir)
        
        if os.path.isdir(component_path):
            # Look for HTML templates
            for file in os.listdir(component_path):
                if file.endswith('.html'):
                    template_path = os.path.join(component_path, file)
                    if update_component_template(template_path):
                        updated_count += 1
    
    print(f"\n✅ Updated {updated_count} component templates")

def main():
    update_all_components()

if __name__ == "__main__":
    main()