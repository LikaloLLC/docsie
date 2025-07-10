#!/usr/bin/env python3
"""
Diagnose translation behavior and explain why progress shows X/550
"""

from babel.messages import pofile
from pathlib import Path
import hashlib
import pickle
import os

def get_cache_key(text: str, target_lang: str, source_lang: str = "en") -> str:
    """Generate cache key for translation (matching translation_system.py)"""
    content = f"{source_lang}->{target_lang}:{text}"
    return hashlib.sha256(content.encode()).hexdigest()

def diagnose_translation_behavior():
    print("=" * 80)
    print("TRANSLATION SYSTEM DIAGNOSTIC")
    print("=" * 80)
    print()
    
    # Configuration from translation_system.py
    skip_existing = True  # Default value
    print(f"Configuration: skip_existing = {skip_existing}")
    print()
    
    # Check a sample language
    lang = 'es'
    po_path = f'locale/{lang}/LC_MESSAGES/messages.po'
    
    with open(po_path, 'rb') as f:
        catalog = pofile.read_po(f)
    
    # Count messages
    all_messages = [msg for msg in catalog if msg.id and not msg.pluralizable]
    total_count = len(all_messages)
    
    # Apply the same logic as translation_system.py line 398
    messages_to_translate = []
    for msg in all_messages:
        if not msg.string or not skip_existing:
            messages_to_translate.append(msg)
    
    print(f"Analysis for Spanish (es):")
    print(f"  Total messages in catalog: {total_count}")
    print(f"  Messages with translations: {sum(1 for m in all_messages if m.string)}")
    print(f"  Empty messages: {sum(1 for m in all_messages if not m.string)}")
    print()
    
    print(f"Translation logic (line 398):")
    print(f"  if message.id and (not message.string or not skip_existing):")
    print()
    print(f"  With skip_existing={skip_existing}:")
    print(f"    - Will translate if: not message.string (empty) OR not {skip_existing}")
    print(f"    - Simplifies to: not message.string OR False")  
    print(f"    - Which means: only translate empty messages")
    print()
    
    print(f"Messages that would be translated: {len(messages_to_translate)}")
    
    if messages_to_translate:
        print("\nFirst 3 messages that would be translated:")
        for i, msg in enumerate(messages_to_translate[:3]):
            print(f"  {i+1}. ID: '{msg.id[:50]}...' | String: '{msg.string}'")
    else:
        print("\n✅ No messages need translation (all have existing translations)")
    
    print("\n" + "-" * 80)
    print("WHY THE PROGRESS SHOWS X/550:")
    print("-" * 80)
    print()
    print("The progress indicator shows 'Translated X/550' where:")
    print(f"  - X = number of strings actually translated so far")
    print(f"  - 550 = total messages in the catalog (not just empty ones)")
    print()
    print("This is misleading because:")
    print("  1. It suggests 550 strings need translation")
    print("  2. But with skip_existing=True, only empty strings are translated")
    print("  3. If all strings already have translations, nothing is sent to API")
    print("  4. The cache check happens INSIDE translate_with_anthropic()")
    print()
    print("What you're seeing is probably:")
    print("  - Old translations being read from cache")
    print("  - OR the system was run before and already translated everything")
    
    # Check cache
    print("\n" + "-" * 80)
    print("CACHE ANALYSIS:")
    print("-" * 80)
    
    cache_dir = Path("locale/.cache")
    cache_file = cache_dir / "translations.pkl"
    
    if cache_file.exists():
        print(f"✅ Cache file exists: {cache_file}")
        try:
            with open(cache_file, 'rb') as f:
                cache = pickle.load(f)
            print(f"   Cache contains {len(cache)} entries")
            
            # Check if any of our messages are in cache
            if messages_to_translate:
                cached_count = 0
                for msg in messages_to_translate[:10]:  # Check first 10
                    key = get_cache_key(msg.id, lang)
                    if key in cache:
                        cached_count += 1
                print(f"   Of first 10 messages to translate, {cached_count} are in cache")
        except Exception as e:
            print(f"   Error reading cache: {e}")
    else:
        print(f"❌ No cache file found at {cache_file}")
        print("   This means all translations would call the API")
        
    # Check if .po files were recently modified
    print("\n" + "-" * 80)
    print("FILE MODIFICATION TIMES:")
    print("-" * 80)
    
    import datetime
    for lang in ['es', 'fr', 'de', 'ar', 'ko']:
        po_file = Path(f'locale/{lang}/LC_MESSAGES/messages.po')
        if po_file.exists():
            mtime = datetime.datetime.fromtimestamp(po_file.stat().st_mtime)
            print(f"  {lang.upper()}: {mtime.strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    diagnose_translation_behavior()