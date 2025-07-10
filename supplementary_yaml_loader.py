#!/usr/bin/env python3
"""
Enhanced YAML loader that supports language-specific YAML files
This can be integrated into existing supplementary_site_generator.py
"""

import yaml
from pathlib import Path
from typing import List, Dict, Any, Optional


def load_yaml_with_language_support(yaml_path: str, locale_code: str = 'en') -> dict:
    """
    Load YAML file with language support.
    First tries to load language-specific version, falls back to English.
    """
    yaml_path = Path(yaml_path)
    
    # Try language-specific version first
    if locale_code != 'en':
        # Look for translated version in _locale directory
        lang_specific_path = yaml_path.parent / f"_{locale_code}" / yaml_path.name
        
        if lang_specific_path.exists():
            print(f"  📖 Loading translated YAML: {lang_specific_path}")
            with open(lang_specific_path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
    
    # Fallback to original/English version
    with open(yaml_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)


def load_all_supplementary_pages_with_lang(locale_code: str = 'en') -> List[Dict[str, Any]]:
    """
    Load all supplementary pages from YAML files with language support.
    This is a drop-in replacement for the original function.
    """
    all_pages = []
    data_dir = Path('src/.data')
    
    # Process all YAML files in the data directory and subdirectories
    for yaml_file in data_dir.rglob('*.yaml'):
        # Skip the main supplementary_pages.yaml as it's just metadata
        if yaml_file.stem == 'supplementary_pages':
            continue
            
        # Skip language-specific directories
        if yaml_file.parts[-2].startswith('_'):
            continue
        
        try:
            # Load with language support
            page_data = load_yaml_with_language_support(yaml_file, locale_code)
            
            if page_data:
                if isinstance(page_data, list):
                    all_pages.extend(page_data)
                else:
                    all_pages.append(page_data)
                    
        except Exception as e:
            print(f"  ⚠️  Error loading {yaml_file}: {e}")
    
    return all_pages


def patch_supplementary_generator():
    """
    Show how to patch the existing supplementary_site_generator.py
    to use language-aware YAML loading
    """
    patch_code = '''
# In supplementary_site_generator.py, replace the load_all_supplementary_pages function:

from supplementary_yaml_loader import load_all_supplementary_pages_with_lang

# Then in generate_supplementary_pages_for_language function:
def generate_supplementary_pages_for_language(locale_code, locale_dir, output_base=''):
    # ... existing code ...
    
    # Replace this line:
    # pages_data = load_all_supplementary_pages()
    
    # With this:
    pages_data = load_all_supplementary_pages_with_lang(locale_code)
    
    # ... rest of the function remains the same ...
'''
    return patch_code


# Integration helper
def get_integration_instructions():
    """Get step-by-step integration instructions"""
    return """
INTEGRATION INSTRUCTIONS:

1. Generate translated YAML files:
   python yaml_translator.py
   
2. Update supplementary_site_generator.py:
   - Import: from supplementary_yaml_loader import load_all_supplementary_pages_with_lang
   - Replace load_all_supplementary_pages() calls with load_all_supplementary_pages_with_lang(locale_code)

3. Update generate_supplementary_multilingual.py:
   - Pass locale_code to the loading function
   
4. Run the multilingual generator:
   python generate_supplementary_multilingual.py

The system will now automatically use translated YAML files when generating
pages for different languages, falling back to English if translations are missing.
"""

if __name__ == "__main__":
    print(get_integration_instructions())