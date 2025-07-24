#!/usr/bin/env python3
"""
Remove legacy pages from all language directories based on .gitignore patterns
"""

import os
import shutil
from pathlib import Path

# Legacy pages to remove (from .gitignore lines 82-120)
LEGACY_PAGES = [
    'validation_page',
    '2020_websummit', 
    'collision_2020',
    'collision_2021',
    'codepen',
    'carbon',
    'affiliate-program',
    'docsie_manager',
    'docsie_publishing',
    'docsie_product',
    'docsie_vocally',
    'docsie-free-consultation',
    'discovery_call',
    'feedback_preview_demo',
    'gather_feedback',
    'incident',
    'manager',
    'markdown_editor',
    'pilot',
    'press',
    'release_notes',
    'publish_documentation',
    'self-writing-documentation',
    'see-it-in-action',
    'software_documentation',
    'collaboration_software',
    'careers',
    'cookies',
    'investors',
    'resources',
    'terms',
    'support',
    'privacy',
    'about',
    'features',
    'documentation',
    'modern-home',
    'eml',
    'content',
    # Additional directories to remove
    'assets',
    'g2',
    'co-jp',
    'new_home',
    'pricing_v2',
    'styles',
    'try_docsie',
    'version_language',
    'vocally',
    'blog',
    'beta'
]

def remove_legacy_pages():
    """Remove legacy pages from all language directories"""
    print("🧹 Removing legacy pages from all language directories...")
    
    total_removed = 0
    
    # Get all language directories (2-letter directories with index.html)
    for item in os.listdir('.'):
        if os.path.isdir(item) and len(item) == 2:
            index_path = os.path.join(item, 'index.html')
            if os.path.exists(index_path):
                print(f"\n📁 Processing {item}/...")
                removed_in_lang = 0
                
                # Remove each legacy page if it exists
                for page in LEGACY_PAGES:
                    page_path = os.path.join(item, page)
                    if os.path.exists(page_path):
                        try:
                            if os.path.isdir(page_path):
                                shutil.rmtree(page_path)
                            else:
                                os.remove(page_path)
                            print(f"  ✓ Removed {page}")
                            removed_in_lang += 1
                            total_removed += 1
                        except Exception as e:
                            print(f"  ✗ Error removing {page}: {e}")
                
                if removed_in_lang == 0:
                    print(f"  No legacy pages found")
                else:
                    print(f"  Removed {removed_in_lang} legacy pages")
    
    print(f"\n✅ Total removed: {total_removed} legacy pages across all languages")

if __name__ == "__main__":
    remove_legacy_pages()