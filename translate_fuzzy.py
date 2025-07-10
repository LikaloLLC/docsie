#!/usr/bin/env python3
"""
Translate only fuzzy strings in .po files
"""

import os
import sys
from pathlib import Path
from babel.messages.pofile import read_po, write_po
import anthropic
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def translate_fuzzy_strings(po_path, lang_code, client):
    """Translate only fuzzy strings in a .po file"""
    
    try:
        # Read the .po file
        with open(po_path, 'rb') as f:
            catalog = read_po(f)
            
        translated_count = 0
        fuzzy_count = 0
        
        # Count fuzzy strings first
        for message in catalog:
            if message.id and 'fuzzy' in message.flags:
                fuzzy_count += 1
                
        if fuzzy_count == 0:
            print(f"✅ {lang_code}: No fuzzy strings found")
            return 0
            
        print(f"🔍 {lang_code}: Found {fuzzy_count} fuzzy strings")
        
        # Translate fuzzy strings
        for message in catalog:
            if message.id and 'fuzzy' in message.flags:
                try:
                    # Get language name
                    lang_names = {
                        'es': 'Spanish', 'fr': 'French', 'de': 'German',
                        'it': 'Italian', 'pt': 'Portuguese', 'nl': 'Dutch',
                        'pl': 'Polish', 'ru': 'Russian', 'cs': 'Czech',
                        'hu': 'Hungarian', 'ro': 'Romanian', 'sv': 'Swedish',
                        'da': 'Danish', 'no': 'Norwegian', 'fi': 'Finnish',
                        'is': 'Icelandic', 'zh': 'Chinese (Simplified)',
                        'ja': 'Japanese', 'ko': 'Korean', 'hi': 'Hindi',
                        'bn': 'Bengali', 'id': 'Indonesian', 'ar': 'Arabic',
                        'he': 'Hebrew', 'tr': 'Turkish', 'el': 'Greek',
                        'uk': 'Ukrainian'
                    }
                    
                    target_lang_name = lang_names.get(lang_code, lang_code)
                    
                    prompt = f"""You are a professional translator specializing in technical documentation and software interfaces.

Please translate the following text from English to {target_lang_name}:

"{message.id}"

Requirements:
- Maintain the same tone and style appropriate for a professional documentation platform
- Keep technical terms accurate and consistent
- If the text contains HTML tags, preserve them exactly
- For software interface elements, use standard conventions for {target_lang_name}
- Return ONLY the translated text, no explanations or additional content

Translation:"""

                    response = client.messages.create(
                        model="claude-sonnet-4-20250514",
                        max_tokens=1000,
                        temperature=0.1,
                        messages=[{"role": "user", "content": prompt}]
                    )
                    
                    translated_text = response.content[0].text.strip()
                    
                    # Update the message
                    message.string = translated_text
                    message.flags.discard('fuzzy')  # Remove fuzzy flag
                    
                    translated_count += 1
                    print(f"  ✅ Translated: '{message.id}' -> '{translated_text}'")
                    
                except Exception as e:
                    print(f"  ❌ Failed to translate '{message.id}': {e}")
                    
        # Write back the .po file
        if translated_count > 0:
            with open(po_path, 'wb') as f:
                write_po(f, catalog)
            print(f"✅ {lang_code}: Translated {translated_count} fuzzy strings")
            
        return translated_count
        
    except Exception as e:
        print(f"❌ Error processing {lang_code}: {e}")
        return 0

def main():
    # Check for API key
    api_key = os.getenv('ANTHROPIC_API_KEY')
    if not api_key:
        print("❌ ANTHROPIC_API_KEY not found in environment")
        sys.exit(1)
        
    # Initialize Anthropic client
    client = anthropic.Anthropic(api_key=api_key)
    
    locale_dir = Path("locale")
    
    # Get all language directories
    languages = []
    for lang_dir in locale_dir.iterdir():
        if lang_dir.is_dir() and lang_dir.name not in ['.cache', 'ja_JP']:
            po_file = lang_dir / "LC_MESSAGES" / "messages.po"
            if po_file.exists():
                languages.append(lang_dir.name)
                
    languages.sort()
    
    print(f"🌍 Processing {len(languages)} languages for fuzzy translations")
    print("=" * 80)
    
    total_translated = 0
    
    for lang in languages:
        po_path = locale_dir / lang / "LC_MESSAGES" / "messages.po"
        count = translate_fuzzy_strings(po_path, lang, client)
        total_translated += count
        
    print("=" * 80)
    print(f"✅ Total fuzzy strings translated: {total_translated}")
    
    if total_translated > 0:
        print("\n📦 Next steps:")
        print("1. Compile the translations: python translation_system.py compile")
        print("2. Generate translated pages: python generate_translated_pages.py")

if __name__ == "__main__":
    main()