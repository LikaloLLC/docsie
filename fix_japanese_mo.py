#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Fix Japanese .mo file compilation issues"""

import subprocess
import os

print("Fixing Japanese translation compilation...")

# Use msgfmt with options that skip format checking
cmd = [
    'msgfmt',
    '--no-hash',           # Don't include hash table
    '-o', 'locale/ja/LC_MESSAGES/messages.mo',
    'locale/ja/LC_MESSAGES/messages.po'
]

try:
    # Run msgfmt without format checking
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode != 0:
        print("Errors encountered:")
        print(result.stderr)
    else:
        print("Successfully compiled Japanese translations")
        
    # Test if it worked
    from babel.support import Translations
    trans = Translations.load('locale', ['ja'])
    test_msg = trans.gettext('Create documentation that your customers love')
    print(f"\nTest translation: '{test_msg}'")
    
    if test_msg != 'Create documentation that your customers love':
        print("✓ Translation is working!")
    else:
        print("✗ Translation still not working")
        
except Exception as e:
    print(f"Error: {e}")

print("\nChecking .mo file size...")
if os.path.exists('locale/ja/LC_MESSAGES/messages.mo'):
    size = os.path.getsize('locale/ja/LC_MESSAGES/messages.mo')
    print(f"Japanese .mo file size: {size} bytes")