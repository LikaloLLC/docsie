#!/usr/bin/env python3
"""
Translate fuzzy strings for a single language
"""

import os
import sys
from pathlib import Path
from babel.messages.pofile import read_po, write_po
import anthropic
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def main():
    if len(sys.argv) != 2:
        print("Usage: python translate_fuzzy_single.py <language_code>")
        print("Example: python translate_fuzzy_single.py es")
        sys.exit(1)
        
    lang_code = sys.argv[1]
    
    # Check for API key
    api_key = os.getenv('ANTHROPIC_API_KEY')
    if not api_key:
        print("❌ ANTHROPIC_API_KEY not found in environment")
        sys.exit(1)
        
    # Initialize Anthropic client
    client = anthropic.Anthropic(api_key=api_key)
    
    locale_dir = Path("locale")
    po_path = locale_dir / lang_code / "LC_MESSAGES" / "messages.po"
    
    if not po_path.exists():
        print(f"❌ No .po file found for {lang_code}")
        sys.exit(1)
        
    try:
        # Read the .po file
        with open(po_path, 'rb') as f:
            catalog = read_po(f)
            
        # Find fuzzy strings
        fuzzy_messages = []
        for message in catalog:
            if message.id and 'fuzzy' in message.flags:
                fuzzy_messages.append(message)
                
        if not fuzzy_messages:
            print(f"✅ No fuzzy strings found in {lang_code}")
            return
            
        print(f"🔍 Found {len(fuzzy_messages)} fuzzy strings in {lang_code}:")
        for msg in fuzzy_messages:
            print(f"  - {msg.id}")
            
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
        
        # Translate each fuzzy string
        for i, message in enumerate(fuzzy_messages):
            print(f"\n📝 Translating ({i+1}/{len(fuzzy_messages)}): '{message.id}'")
            
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

            try:
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
                
                print(f"  ✅ Translated to: '{translated_text}'")
                
            except Exception as e:
                print(f"  ❌ Failed: {e}")
                
        # Write back the .po file
        with open(po_path, 'wb') as f:
            write_po(f, catalog)
            
        print(f"\n✅ Updated {lang_code}/LC_MESSAGES/messages.po")
        print("\nNext: Run 'python translation_system.py compile' to compile this language")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()