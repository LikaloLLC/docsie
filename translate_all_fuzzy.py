#!/usr/bin/env python3
"""
Translate all fuzzy strings across all languages
"""

import os
import sys
import subprocess
from pathlib import Path

def main():
    # Languages that have fuzzy strings based on our analysis
    languages_with_fuzzy = [
        'ar', 'bn', 'cs', 'da', 'de', 'el', 'es', 'fi', 'fr', 'he', 'hi', 'hu', 
        'id', 'is', 'it', 'ja', 'ko', 'nl', 'no', 'pl', 'pt', 'ro', 'ru', 
        'sv', 'tr', 'uk', 'zh'
    ]
    
    print(f"🌍 Translating fuzzy strings for {len(languages_with_fuzzy)} languages")
    print("=" * 80)
    
    successful = []
    failed = []
    
    for i, lang in enumerate(languages_with_fuzzy):
        print(f"\n[{i+1}/{len(languages_with_fuzzy)}] Processing {lang}...")
        
        try:
            result = subprocess.run(
                ['python', 'translate_fuzzy_single.py', lang],
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                if "No fuzzy strings found" in result.stdout:
                    print(f"  ✅ {lang}: Already up to date")
                else:
                    print(f"  ✅ {lang}: Fuzzy strings translated")
                successful.append(lang)
            else:
                print(f"  ❌ {lang}: Translation failed")
                print(f"     Error: {result.stderr}")
                failed.append(lang)
                
        except Exception as e:
            print(f"  ❌ {lang}: Exception: {e}")
            failed.append(lang)
    
    print("\n" + "=" * 80)
    print(f"✅ Successfully processed: {len(successful)} languages")
    if failed:
        print(f"❌ Failed: {len(failed)} languages - {', '.join(failed)}")
    
    if successful:
        print("\n📦 Next steps:")
        print("1. Compile all translations: python translation_system.py compile")
        print("2. Generate translated pages: python generate_translated_pages.py")

if __name__ == "__main__":
    main()