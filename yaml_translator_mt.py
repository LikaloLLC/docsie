#!/usr/bin/env python3
"""
Multi-threaded YAML translator with caching support.
Translates YAML files for supplementary pages using multiple threads.
"""

import os
import yaml
import json
import hashlib
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading
import time
from datetime import datetime
import argparse

# Import the translation system
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from translation_system import TranslationSystem

# Cache configuration
CACHE_DIR = Path('.translation_cache')
CACHE_FILE = CACHE_DIR / 'yaml_translations.json'
cache_lock = threading.Lock()
translation_cache = {}

def load_cache():
    """Load translation cache from disk"""
    global translation_cache
    if CACHE_FILE.exists():
        try:
            with open(CACHE_FILE, 'r', encoding='utf-8') as f:
                translation_cache = json.load(f)
                print(f"Loaded {len(translation_cache)} cached translations")
        except Exception as e:
            print(f"Warning: Failed to load cache: {e}")
            translation_cache = {}
    else:
        CACHE_DIR.mkdir(exist_ok=True)
        translation_cache = {}

def save_cache():
    """Save translation cache to disk"""
    try:
        with cache_lock:
            with open(CACHE_FILE, 'w', encoding='utf-8') as f:
                json.dump(translation_cache, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"Warning: Failed to save cache: {e}")

def get_cache_key(text, target_language, context=''):
    """Generate a cache key for a translation"""
    content = f"{text}|{target_language}|{context}"
    return hashlib.md5(content.encode('utf-8')).hexdigest()

def translate_with_cache(translator, text, target_language, context=''):
    """Translate text with caching"""
    if not text or not isinstance(text, str):
        return text
        
    cache_key = get_cache_key(text, target_language, context)
    
    # Check cache first
    with cache_lock:
        if cache_key in translation_cache:
            return translation_cache[cache_key]
    
    # Not in cache, translate
    try:
        translated = translator.translate_with_anthropic(text, target_language)
        
        # Save to cache
        with cache_lock:
            translation_cache[cache_key] = translated
            
        return translated
    except Exception as e:
        print(f"Translation error: {e}")
        return text

def should_translate(value, context=''):
    """Determine if a value should be translated"""
    if not isinstance(value, str):
        return False
        
    # Skip empty or very short strings
    if len(value.strip()) < 2:
        return False
        
    # Skip URLs, IDs, and technical values
    skip_patterns = [
        'http://', 'https://', 'mailto:', 'tel:', '#',
        '.png', '.jpg', '.jpeg', '.gif', '.svg', '.webp',
        '.css', '.js', '.html',
    ]
    
    lower_value = value.lower()
    if any(pattern in lower_value for pattern in skip_patterns):
        return False
        
    # Skip if context suggests it's an ID or technical field
    skip_fields = [
        '.id', '.url', '.link', '.href', '.category', '.icon', 
        '.image', '.alt', '.ui_version', '.hero_version', 
        '.calendly_url', '.video_link', '.class', '.type',
        '.component', '.template', '.slug'
    ]
    if any(context.endswith(field) for field in skip_fields):
        return False
        
    # Skip if it's just numbers or special characters
    if value.replace(' ', '').replace('-', '').replace('_', '').replace('.', '').isdigit():
        return False
        
    return True

def translate_yaml_content(translator, data, target_language, context='', progress_callback=None):
    """Recursively translate YAML content"""
    if isinstance(data, dict):
        result = {}
        for key, value in data.items():
            new_context = f"{context}.{key}" if context else key
            result[key] = translate_yaml_content(
                translator, value, target_language, new_context, progress_callback
            )
        return result
    elif isinstance(data, list):
        return [
            translate_yaml_content(
                translator, item, target_language, f"{context}[{i}]", progress_callback
            ) for i, item in enumerate(data)
        ]
    elif isinstance(data, str) and should_translate(data, context):
        translated = translate_with_cache(translator, data, target_language, context)
        if progress_callback:
            progress_callback()
        return translated
    else:
        return data

def translate_yaml_file(args):
    """Translate a single YAML file (for use with ThreadPoolExecutor)"""
    yaml_file, output_file, target_language = args
    
    # Create a new translator instance for this thread
    translator = TranslationSystem()
    
    # Initialize Anthropic client
    api_key = os.getenv('ANTHROPIC_API_KEY')
    if api_key:
        translator.setup_anthropic_client(api_key)
    else:
        print(f"  ✗ Error: ANTHROPIC_API_KEY not found in environment")
        return None
    
    try:
        # Load YAML
        with open(yaml_file, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
        
        if not data:
            print(f"  Skipping empty file: {yaml_file}")
            return None
            
        print(f"  Translating: {yaml_file}")
        start_time = time.time()
        
        # Count translatable strings for progress
        def count_strings(d, context=''):
            count = 0
            if isinstance(d, dict):
                for k, v in d.items():
                    count += count_strings(v, f"{context}.{k}" if context else k)
            elif isinstance(d, list):
                for i, item in enumerate(d):
                    count += count_strings(item, f"{context}[{i}]")
            elif isinstance(d, str) and should_translate(d, context):
                count += 1
            return count
        
        total_strings = count_strings(data)
        translated_count = 0
        
        def progress_callback():
            nonlocal translated_count
            translated_count += 1
            if translated_count % 10 == 0:
                print(f"    Progress: {translated_count}/{total_strings} strings")
        
        # Translate
        translated_data = translate_yaml_content(
            translator, data, target_language, progress_callback=progress_callback
        )
        
        # Save translated YAML
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        with open(output_file, 'w', encoding='utf-8') as f:
            yaml.dump(translated_data, f, allow_unicode=True, sort_keys=False, default_flow_style=False)
        
        elapsed = time.time() - start_time
        print(f"  ✓ Completed: {yaml_file} ({translated_count} strings in {elapsed:.1f}s)")
        
        # Save cache periodically
        save_cache()
        
        return output_file
        
    except Exception as e:
        print(f"  ✗ Error translating {yaml_file}: {e}")
        return None

def translate_yamls_for_language(source_dir, target_language, output_dir, max_workers=4):
    """Translate all YAML files for a specific language using multiple threads"""
    print(f"\nTranslating YAMLs to {target_language} using {max_workers} threads...")
    
    # Collect all YAML files
    yaml_files = []
    for yaml_file in Path(source_dir).rglob('*.yaml'):
        # Skip language-specific directories
        if any(part.startswith('_') for part in yaml_file.parts):
            continue
            
        # Skip the main supplementary_pages.yaml
        if yaml_file.name == 'supplementary_pages.yaml':
            continue
            
        # Calculate output path
        relative_path = yaml_file.relative_to(source_dir)
        output_file = Path(output_dir) / f"_{target_language}" / relative_path
        
        yaml_files.append((yaml_file, output_file, target_language))
    
    print(f"Found {len(yaml_files)} YAML files to translate")
    
    # Process files in parallel
    translated_files = []
    failed_files = []
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Submit all tasks
        future_to_file = {
            executor.submit(translate_yaml_file, args): args[0] 
            for args in yaml_files
        }
        
        # Process completed tasks
        for future in as_completed(future_to_file):
            yaml_file = future_to_file[future]
            try:
                result = future.result()
                if result:
                    translated_files.append(result)
                else:
                    failed_files.append(yaml_file)
            except Exception as e:
                print(f"  ✗ Exception for {yaml_file}: {e}")
                failed_files.append(yaml_file)
    
    # Final cache save
    save_cache()
    
    # Summary
    print(f"\n✅ Successfully translated: {len(translated_files)} files")
    if failed_files:
        print(f"❌ Failed: {len(failed_files)} files")
        for f in failed_files:
            print(f"  - {f}")
    
    return translated_files

def main():
    parser = argparse.ArgumentParser(description='Multi-threaded YAML translator with caching')
    parser.add_argument('languages', nargs='*', default=['ru'], 
                      help='Target languages (default: ru)')
    parser.add_argument('--source-dir', default='src/.data',
                      help='Source directory with YAML files')
    parser.add_argument('--workers', type=int, default=4,
                      help='Number of worker threads (default: 4)')
    parser.add_argument('--clear-cache', action='store_true',
                      help='Clear translation cache before starting')
    
    args = parser.parse_args()
    
    # Load or clear cache
    if args.clear_cache:
        print("Clearing translation cache...")
        translation_cache.clear()
        if CACHE_FILE.exists():
            CACHE_FILE.unlink()
    else:
        load_cache()
    
    # Process each language
    start_time = time.time()
    
    for language in args.languages:
        print(f"\n{'='*60}")
        print(f"Translating to: {language}")
        print(f"{'='*60}")
        
        translate_yamls_for_language(
            args.source_dir,
            language,
            args.source_dir,
            max_workers=args.workers
        )
    
    total_time = time.time() - start_time
    print(f"\n🎉 All translations completed in {total_time:.1f} seconds")
    print(f"📊 Cache now contains {len(translation_cache)} translations")

if __name__ == "__main__":
    main()