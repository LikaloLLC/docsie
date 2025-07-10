#!/usr/bin/env python3
"""
Translate supplementary pages into all available languages
"""
import os
import subprocess
import sys

def get_available_languages():
    """Get all available language codes from locale directory"""
    locale_dir = 'locale'
    languages = []
    
    for item in os.listdir(locale_dir):
        item_path = os.path.join(locale_dir, item)
        # Check if it's a directory and not a .pot file
        if os.path.isdir(item_path) and not item.startswith('.'):
            languages.append(item)
    
    # Sort languages for consistent processing
    languages.sort()
    return languages

def translate_to_language(language, workers=25):
    """Run yaml_translator_mt.py for a specific language"""
    print(f"\n{'='*60}")
    print(f"Translating to {language.upper()}")
    print(f"{'='*60}")
    
    cmd = [
        sys.executable,
        'yaml_translator_mt.py',
        '--language', language,
        '--workers', str(workers)
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Successfully translated to {language}")
            if result.stdout:
                print(result.stdout)
        else:
            print(f"❌ Failed to translate to {language}")
            if result.stderr:
                print(f"Error: {result.stderr}")
            if result.stdout:
                print(f"Output: {result.stdout}")
        return result.returncode == 0
    except Exception as e:
        print(f"❌ Exception while translating to {language}: {str(e)}")
        return False

def main():
    """Main function to translate all languages"""
    # Get number of workers from command line or use default
    workers = 25
    if len(sys.argv) > 1:
        try:
            workers = int(sys.argv[1])
        except ValueError:
            print(f"Invalid workers number: {sys.argv[1]}, using default: 25")
    
    print(f"Starting translation of supplementary pages to all languages")
    print(f"Using {workers} workers per language")
    
    languages = get_available_languages()
    print(f"\nFound {len(languages)} languages: {', '.join(languages)}")
    
    # Skip English if it exists
    if 'en' in languages:
        languages.remove('en')
        print("Skipping English (source language)")
    
    # Track success/failure
    successful = []
    failed = []
    
    # Translate to each language
    for i, language in enumerate(languages, 1):
        print(f"\n[{i}/{len(languages)}] Processing {language}...")
        
        if translate_to_language(language, workers):
            successful.append(language)
        else:
            failed.append(language)
    
    # Summary
    print("\n" + "="*60)
    print("TRANSLATION SUMMARY")
    print("="*60)
    print(f"✅ Successful: {len(successful)} languages")
    if successful:
        print(f"   {', '.join(successful)}")
    
    print(f"\n❌ Failed: {len(failed)} languages")
    if failed:
        print(f"   {', '.join(failed)}")
    
    print(f"\nTotal: {len(successful)} / {len(languages)} languages translated successfully")
    
    # Exit with error code if any failed
    sys.exit(0 if len(failed) == 0 else 1)

if __name__ == "__main__":
    main()