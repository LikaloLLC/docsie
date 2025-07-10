#!/usr/bin/env python3
"""
Extract translatable strings from YAML files and add them to the translation system.
This allows YAML content to be translated along with template strings.
"""

import os
import yaml
import sys
from pathlib import Path
import subprocess
import tempfile

def extract_strings_from_yaml(yaml_data, path_prefix=""):
    """
    Recursively extract all string values from YAML data structure.
    Returns a list of (path, string) tuples.
    """
    strings = []
    
    if isinstance(yaml_data, dict):
        for key, value in yaml_data.items():
            new_path = f"{path_prefix}.{key}" if path_prefix else key
            strings.extend(extract_strings_from_yaml(value, new_path))
    
    elif isinstance(yaml_data, list):
        for i, item in enumerate(yaml_data):
            new_path = f"{path_prefix}[{i}]"
            strings.extend(extract_strings_from_yaml(item, new_path))
    
    elif isinstance(yaml_data, str) and yaml_data.strip():
        # Only extract non-empty strings
        # Skip certain technical fields
        skip_fields = ['id', 'category', 'template', 'url', 'image', 'icon', 'color', 'type', 'link', '_source_file']
        field_name = path_prefix.split('.')[-1] if '.' in path_prefix else path_prefix
        
        if field_name not in skip_fields and not yaml_data.startswith('http'):
            strings.append((path_prefix, yaml_data))
    
    return strings

def create_yaml_pot_file():
    """Create a POT file with all strings from YAML files."""
    print("🔍 Extracting strings from YAML files...")
    
    all_strings = {}
    yaml_dir = 'src/.data'
    
    # Walk through all YAML files
    for root, dirs, files in os.walk(yaml_dir):
        for filename in files:
            if filename.endswith('.yaml'):
                file_path = os.path.join(root, filename)
                relative_path = os.path.relpath(file_path, yaml_dir)
                
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        data = yaml.safe_load(f)
                        
                    strings = extract_strings_from_yaml(data)
                    
                    for path, string in strings:
                        # Use string as key to avoid duplicates
                        if string not in all_strings:
                            all_strings[string] = []
                        all_strings[string].append(f"{relative_path}:{path}")
                    
                except Exception as e:
                    print(f"Error processing {file_path}: {e}")
    
    print(f"Found {len(all_strings)} unique strings in YAML files")
    
    # Create POT file
    pot_content = """# YAML Content Translations
# This file contains translatable strings extracted from YAML data files
# Generated automatically - do not edit manually
#
msgid ""
msgstr ""
"Content-Type: text/plain; charset=UTF-8\\n"
"Language: \\n"
"MIME-Version: 1.0\\n"

"""
    
    for string, locations in sorted(all_strings.items()):
        # Add location comments
        for loc in locations[:5]:  # Limit to 5 locations to avoid huge comments
            pot_content += f"#: {loc}\n"
        if len(locations) > 5:
            pot_content += f"#: ... and {len(locations) - 5} more locations\n"
        
        # Escape the string properly
        escaped_string = string.replace('"', '\\"').replace('\n', '\\n"\n"')
        pot_content += f'msgid "{escaped_string}"\n'
        pot_content += 'msgstr ""\n\n'
    
    # Save POT file
    pot_file = 'locale/yaml_content.pot'
    with open(pot_file, 'w', encoding='utf-8') as f:
        f.write(pot_content)
    
    print(f"✅ Created {pot_file} with {len(all_strings)} strings")
    return pot_file

def merge_yaml_strings_with_existing():
    """Merge YAML strings with existing messages.pot file."""
    print("\n🔄 Merging YAML strings with existing translations...")
    
    # Create YAML POT file
    yaml_pot = create_yaml_pot_file()
    
    # Create a temporary combined POT file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.pot', delete=False) as tmp:
        tmp_file = tmp.name
    
    try:
        # Merge the two POT files
        cmd = [
            'msgcat',
            'locale/messages.pot',
            yaml_pot,
            '-o', tmp_file
        ]
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            # Replace original with merged version
            import shutil
            shutil.move(tmp_file, 'locale/messages_with_yaml.pot')
            print("✅ Created locale/messages_with_yaml.pot with combined strings")
            
            # Update all language files to include new strings
            update_language_files('locale/messages_with_yaml.pot')
        else:
            print(f"❌ Error merging POT files: {result.stderr}")
    
    finally:
        # Clean up temp file if it exists
        if os.path.exists(tmp_file):
            os.remove(tmp_file)

def update_language_files(pot_file):
    """Update all .po files with new strings from POT file."""
    print("\n📝 Updating language files with new strings...")
    
    locale_dir = 'locale'
    updated_count = 0
    
    for lang_dir in os.listdir(locale_dir):
        po_file = os.path.join(locale_dir, lang_dir, 'LC_MESSAGES', 'messages.po')
        
        if os.path.exists(po_file):
            # Update the PO file with new strings
            cmd = [
                'msgmerge',
                '--update',
                '--no-fuzzy-matching',
                po_file,
                pot_file
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                updated_count += 1
                print(f"  ✅ Updated {lang_dir}")
            else:
                print(f"  ❌ Error updating {lang_dir}: {result.stderr}")
    
    print(f"\n✅ Updated {updated_count} language files")

def create_yaml_aware_template_wrapper():
    """Create a template wrapper that handles YAML content translation."""
    wrapper_content = '''<!-- YAML-aware supplementary page template wrapper -->
{% macro translate_yaml_string(text) -%}
    {%- if text -%}
        {{ _(text) }}
    {%- else -%}
        {{ text }}
    {%- endif -%}
{%- endmacro %}

{% macro render_yaml_content(data) -%}
    {%- if data is string -%}
        {{ translate_yaml_string(data) }}
    {%- elif data is mapping -%}
        {%- for key, value in data.items() -%}
            {%- if key not in ['id', 'category', 'template', 'url', 'image', 'icon', 'color', 'type', 'link'] -%}
                {{ render_yaml_content(value) }}
            {%- endif -%}
        {%- endfor -%}
    {%- elif data is iterable -%}
        {%- for item in data -%}
            {{ render_yaml_content(item) }}
        {%- endfor -%}
    {%- endif -%}
{%- endmacro %}
'''
    
    wrapper_file = 'src/.templates/yaml_translation_helpers.html'
    with open(wrapper_file, 'w', encoding='utf-8') as f:
        f.write(wrapper_content)
    
    print(f"\n✅ Created {wrapper_file}")

def main():
    """Main function to extract and prepare YAML strings for translation."""
    print("🚀 Starting YAML string extraction for translations...\n")
    
    # Check if required tools are available
    for tool in ['msgcat', 'msgmerge']:
        if subprocess.run(['which', tool], capture_output=True).returncode != 0:
            print(f"❌ Error: {tool} not found. Please install gettext tools.")
            sys.exit(1)
    
    # Extract and merge strings
    merge_yaml_strings_with_existing()
    
    # Create template helpers
    create_yaml_aware_template_wrapper()
    
    print("\n✅ YAML string extraction complete!")
    print("\nNext steps:")
    print("1. Translate the new strings in locale/*/LC_MESSAGES/messages.po files")
    print("2. Compile translations: python translation_system.py compile")
    print("3. Update supplementary templates to use translation helpers")
    print("4. Regenerate the site with translations")

if __name__ == "__main__":
    main()