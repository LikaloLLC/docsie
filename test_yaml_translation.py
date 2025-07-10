#!/usr/bin/env python3
"""Test YAML translation with a single file"""

from yaml_translator import YAMLTranslator
from pathlib import Path

# Create translator
translator = YAMLTranslator()

# Test with one file
test_file = Path("src/.data/doc_chatbots.yaml")
if test_file.exists():
    print(f"Translating {test_file} to Russian...")
    translated = translator.translate_yaml_file(test_file, "ru", force=True)
    
    # Save to test location
    output_file = Path("test_ru_chatbots.yaml")
    import yaml
    with open(output_file, 'w', encoding='utf-8') as f:
        yaml.dump(translated, f, allow_unicode=True, default_flow_style=False, sort_keys=False)
    
    print(f"Saved to {output_file}")
    print("\nFirst few lines of translation:")
    with open(output_file, 'r', encoding='utf-8') as f:
        for i, line in enumerate(f):
            if i < 20:
                print(line.rstrip())
else:
    print(f"Test file {test_file} not found")