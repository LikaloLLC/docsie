#!/usr/bin/env python3
"""
Show translation delta - what strings actually need translation
"""

import os
import sys
from pathlib import Path
from babel.messages.pofile import read_po
from collections import defaultdict

def analyze_po_file(po_path):
    """Analyze a .po file and return statistics"""
    stats = {
        'total': 0,
        'translated': 0,
        'untranslated': 0,
        'fuzzy': 0,
        'untranslated_strings': []
    }
    
    try:
        with open(po_path, 'rb') as f:
            catalog = read_po(f)
            
        for message in catalog:
            if message.id and not message.pluralizable:  # Skip header and plural forms
                stats['total'] += 1
                
                # Debug specific strings
                if "View All AI Solutions" in message.id:
                    print(f"DEBUG: Found '{message.id}', string='{message.string}', flags={message.flags}")
                
                if message.string:
                    if 'fuzzy' in message.flags:
                        stats['fuzzy'] += 1
                        stats['untranslated_strings'].append({
                            'id': message.id,
                            'current': message.string,
                            'status': 'fuzzy'
                        })
                    else:
                        stats['translated'] += 1
                else:
                    stats['untranslated'] += 1
                    stats['untranslated_strings'].append({
                        'id': message.id,
                        'current': '',
                        'status': 'empty'
                    })
                    
    except Exception as e:
        print(f"Error reading {po_path}: {e}")
        
    return stats

def main():
    locale_dir = Path("locale")
    
    if not locale_dir.exists():
        print("❌ No locale directory found")
        sys.exit(1)
        
    # Get all language directories
    languages = []
    for lang_dir in locale_dir.iterdir():
        if lang_dir.is_dir() and lang_dir.name != '.cache':
            po_file = lang_dir / "LC_MESSAGES" / "messages.po"
            if po_file.exists():
                languages.append(lang_dir.name)
                
    languages.sort()
    
    print("📊 Translation Delta Analysis")
    print("=" * 80)
    print(f"Found {len(languages)} languages: {', '.join(languages)}")
    print()
    
    # Analyze each language
    total_untranslated = 0
    all_untranslated = defaultdict(list)
    
    for lang in languages:
        po_path = locale_dir / lang / "LC_MESSAGES" / "messages.po"
        stats = analyze_po_file(po_path)
        
        if stats['untranslated'] > 0 or stats['fuzzy'] > 0:
            print(f"\n🔍 {lang}: {stats['untranslated']} untranslated, {stats['fuzzy']} fuzzy")
            
            # Show first 5 untranslated strings
            for i, item in enumerate(stats['untranslated_strings'][:5]):
                status_icon = "❓" if item['status'] == 'fuzzy' else "❌"
                print(f"   {status_icon} {item['id'][:60]}...")
                
            if len(stats['untranslated_strings']) > 5:
                print(f"   ... and {len(stats['untranslated_strings']) - 5} more")
                
            # Collect for summary
            for item in stats['untranslated_strings']:
                all_untranslated[item['id']].append(lang)
                
        total_untranslated += stats['untranslated'] + stats['fuzzy']
        
    print("\n" + "=" * 80)
    print(f"📊 Summary: {total_untranslated} total strings need translation")
    
    if total_untranslated == 0:
        print("✅ All translations are complete! No delta to translate.")
        print("\nℹ️  Running 'python translation_system.py translate' would:")
        print("   - Process all strings but skip them (skip_existing=True)")
        print("   - Make 0 API calls")
        print("   - Cost $0")
    else:
        # Show strings that need translation across multiple languages
        print(f"\n🌍 Strings needing translation in multiple languages:")
        multi_lang_strings = [(k, v) for k, v in all_untranslated.items() if len(v) > 1]
        multi_lang_strings.sort(key=lambda x: -len(x[1]))
        
        for string_id, langs in multi_lang_strings[:10]:
            print(f"   '{string_id[:50]}...' - needed in: {', '.join(langs)}")
            
        # Cost estimate
        total_strings_to_translate = sum(len(v) for v in all_untranslated.values())
        # Rough estimate: ~$0.003 per 1000 input tokens, ~100 tokens per string
        estimated_cost = (total_strings_to_translate * 100 / 1000) * 0.003
        print(f"\n💰 Estimated translation cost: ${estimated_cost:.2f}")
        
    # Check cache status
    cache_file = locale_dir / ".cache" / "translations.pkl"
    if cache_file.exists():
        import pickle
        try:
            with open(cache_file, 'rb') as f:
                cache = pickle.load(f)
            print(f"\n📦 Cache status: {len(cache)} cached translations available")
        except:
            print("\n📦 Cache status: Unable to read cache file")
    else:
        print("\n📦 Cache status: No cache file exists")

if __name__ == "__main__":
    main()