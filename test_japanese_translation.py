#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Test script to debug Japanese translation issue"""

import os
from jinja2 import Environment, FileSystemLoader
from jinja2.ext import i18n
from babel.support import Translations

# Test translation loading
print("=== Testing Translation Loading ===")
locales = ['en', 'ja', 'ru', 'es']
for locale in locales:
    try:
        trans = Translations.load('locale', [locale])
        msg_count = len([m for m in trans._catalog.items() if m[1]])
        print(f"\n{locale}: Loaded {msg_count} translations")
        
        # Test specific message
        test_msg = "Create documentation that your customers love"
        translated = trans.gettext(test_msg)
        print(f"  '{test_msg}' -> '{translated}'")
        
        # Check if it's actually translated
        if translated != test_msg:
            print(f"  ✓ Translation working!")
        else:
            print(f"  ✗ Translation NOT working!")
            
    except Exception as e:
        print(f"{locale}: Error - {e}")

# Test Jinja2 rendering with Japanese locale
print("\n\n=== Testing Jinja2 Rendering ===")
env = Environment(
    loader=FileSystemLoader('./src'),
    extensions=['jinja2.ext.i18n']
)

# Test template content
test_template_content = """
{% trans %}Create documentation that your customers love{% endtrans %}
"""

# Test with Japanese locale
ja_trans = Translations.load('locale', ['ja'])
env.install_gettext_translations(ja_trans)

template = env.from_string(test_template_content)
rendered = template.render()
print(f"Japanese rendering: {rendered.strip()}")

# Test with Russian locale for comparison
ru_trans = Translations.load('locale', ['ru'])
env.install_gettext_translations(ru_trans)

template = env.from_string(test_template_content)
rendered = template.render()
print(f"Russian rendering: {rendered.strip()}")

# Check if locale directory exists and has proper structure
print("\n\n=== Checking Locale Directory Structure ===")
for locale in ['ja', 'ru']:
    po_file = f'locale/{locale}/LC_MESSAGES/messages.po'
    mo_file = f'locale/{locale}/LC_MESSAGES/messages.mo'
    
    print(f"\n{locale}:")
    if os.path.exists(po_file):
        print(f"  ✓ {po_file} exists")
        # Count translations in PO file
        with open(po_file, 'r', encoding='utf-8') as f:
            content = f.read()
            msgstr_count = content.count('msgstr "')
            empty_msgstr = content.count('msgstr ""')
            filled_msgstr = msgstr_count - empty_msgstr
            print(f"    Total msgstr: {msgstr_count}, Filled: {filled_msgstr}, Empty: {empty_msgstr}")
    else:
        print(f"  ✗ {po_file} missing")
        
    if os.path.exists(mo_file):
        print(f"  ✓ {mo_file} exists")
        # Check file size
        size = os.path.getsize(mo_file)
        print(f"    Size: {size} bytes")
    else:
        print(f"  ✗ {mo_file} missing")