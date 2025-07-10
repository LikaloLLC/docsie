#!/usr/bin/env python3
"""
Analyze translation status and show what needs to be translated
"""

from babel.messages import pofile
import os
from pathlib import Path
from typing import Dict, List, Tuple
import hashlib
import pickle

def get_cache_key(text: str, target_lang: str, source_lang: str = "en") -> str:
    """Generate cache key for translation (matching translation_system.py)"""
    content = f"{source_lang}->{target_lang}:{text}"
    return hashlib.sha256(content.encode()).hexdigest()

def analyze_po_file(po_path: str) -> Dict:
    """Analyze a single .po file"""
    with open(po_path, 'rb') as f:
        catalog = pofile.read_po(f)
    
    total = 0
    translated = 0
    empty_strings = []
    
    for msg in catalog:
        if msg.id and not msg.pluralizable:
            total += 1
            if msg.string:
                translated += 1
            else:
                empty_strings.append(msg.id)
    
    return {
        'total': total,
        'translated': translated,
        'empty': len(empty_strings),
        'empty_strings': empty_strings,
        'percent': (translated/total*100) if total > 0 else 0
    }

def check_cache_status(empty_strings: List[str], lang: str, cache_file: Path) -> Tuple[List[str], List[str]]:
    """Check which strings are in cache vs need translation"""
    cached = []
    not_cached = []
    
    if cache_file.exists():
        try:
            with open(cache_file, 'rb') as f:
                cache = pickle.load(f)
            
            for text in empty_strings:
                key = get_cache_key(text, lang)
                if key in cache:
                    cached.append(text)
                else:
                    not_cached.append(text)
        except Exception:
            not_cached = empty_strings
    else:
        not_cached = empty_strings
    
    return cached, not_cached

def main():
    # Check all language files
    locale_dir = Path("locale")
    cache_dir = locale_dir / ".cache"
    cache_file = cache_dir / "translations.pkl" if cache_dir.exists() else None
    
    languages = ['es', 'fr', 'de', 'pt', 'ar', 'ko', 'ja', 'zh', 'ru', 'it', 'nl', 
                 'sv', 'no', 'da', 'fi', 'pl', 'cs', 'hu', 'ro', 'tr', 'el', 
                 'he', 'hi', 'bn', 'id', 'uk', 'is']
    
    print("=" * 80)
    print("TRANSLATION STATUS ANALYSIS")
    print("=" * 80)
    print()
    
    summary_data = []
    total_to_translate = 0
    
    for lang in languages:
        po_file = locale_dir / lang / "LC_MESSAGES" / "messages.po"
        if po_file.exists():
            data = analyze_po_file(str(po_file))
            summary_data.append((lang, data))
            
            if data['empty'] > 0:
                total_to_translate += data['empty']
    
    # Display summary table
    print(f"{'Lang':6} | {'Total':>6} | {'Done':>6} | {'Empty':>6} | {'Progress':>8}")
    print("-" * 50)
    
    for lang, data in summary_data:
        if data['total'] > 0:
            print(f"{lang.upper():6} | {data['total']:6} | {data['translated']:6} | "
                  f"{data['empty']:6} | {data['percent']:6.1f}%")
    
    print()
    print(f"Total strings needing translation: {total_to_translate}")
    
    # Show details for languages with missing translations
    print("\n" + "=" * 80)
    print("LANGUAGES NEEDING TRANSLATION")
    print("=" * 80)
    
    for lang, data in summary_data:
        if data['empty'] > 0:
            print(f"\n{lang.upper()} - {data['empty']} strings need translation:")
            print("-" * 40)
            
            # Check cache status if cache exists
            if cache_file:
                cached, not_cached = check_cache_status(data['empty_strings'], lang, cache_file)
                
                if cached:
                    print(f"  ✓ {len(cached)} strings found in cache")
                if not_cached:
                    print(f"  ✗ {len(not_cached)} strings NOT in cache (will call API)")
                    print("\n  First 5 strings that need API translation:")
                    for i, text in enumerate(not_cached[:5]):
                        print(f"    {i+1}. \"{text[:60]}...\"" if len(text) > 60 else f"    {i+1}. \"{text}\"")
            else:
                print(f"  ℹ️  No cache file found - all {data['empty']} strings would call API")
                print("\n  First 5 strings needing translation:")
                for i, text in enumerate(data['empty_strings'][:5]):
                    print(f"    {i+1}. \"{text[:60]}...\"" if len(text) > 60 else f"    {i+1}. \"{text}\"")
    
    # Check if cache exists
    print("\n" + "=" * 80)
    print("CACHE STATUS")
    print("=" * 80)
    
    if cache_file and cache_file.exists():
        try:
            with open(cache_file, 'rb') as f:
                cache = pickle.load(f)
            print(f"✅ Cache file exists: {cache_file}")
            print(f"   Total cached translations: {len(cache)}")
            
            # Analyze cache by language
            lang_counts = {}
            for key in cache.keys():
                # Keys are SHA256 hashes, so we can't directly extract language
                # But we can estimate based on patterns
                pass
                
        except Exception as e:
            print(f"⚠️  Cache file exists but couldn't read it: {e}")
    else:
        print("❌ No cache file found")
        print(f"   Expected location: {cache_dir / 'translations.pkl'}")
        print("   This means ALL translations will call the API")
    
    print("\n" + "=" * 80)
    print("RECOMMENDATIONS")
    print("=" * 80)
    
    if total_to_translate == 0:
        print("✅ All languages are fully translated!")
    else:
        print(f"⚠️  {total_to_translate} strings need translation across all languages")
        print("\nTo translate only missing strings:")
        print("  python translation_system.py translate")
        print("\nThis will:")
        print("  - Only translate empty strings (skip_existing=true is default)")
        print("  - Use cached translations where available")
        print("  - Only call the API for strings not in cache")

if __name__ == "__main__":
    main()