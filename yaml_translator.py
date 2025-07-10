#!/usr/bin/env python3
"""
YAML Translation System - A DRY approach to translating YAML content
Integrates with existing translation infrastructure
"""

import os
import yaml
import json
import hashlib
from pathlib import Path
from typing import Dict, Any, List, Optional
from translation_system import TranslationSystem
import shutil


class YAMLTranslator:
    """Translates YAML content files using the existing translation system"""
    
    def __init__(self, translation_system: Optional[TranslationSystem] = None):
        self.translation_system = translation_system or TranslationSystem()
        self.src_data_dir = Path("src/.data")
        self.cache_dir = Path(".yaml_translation_cache")
        self.cache_dir.mkdir(exist_ok=True)
        
        # Initialize the Anthropic client if not already done
        if not self.translation_system.client:
            api_key = os.getenv('ANTHROPIC_API_KEY')
            if api_key:
                self.translation_system.setup_anthropic_client(api_key)
            else:
                print("⚠️  No ANTHROPIC_API_KEY found in environment")
        
    def _get_content_hash(self, content: str) -> str:
        """Generate hash for content to check if translation is needed"""
        return hashlib.md5(content.encode()).hexdigest()
    
    def _load_translation_cache(self, yaml_file: Path, target_lang: str) -> Optional[dict]:
        """Load cached translation if available and valid"""
        cache_file = self.cache_dir / f"{yaml_file.stem}_{target_lang}.json"
        if not cache_file.exists():
            return None
            
        try:
            with open(cache_file, 'r', encoding='utf-8') as f:
                cache_data = json.load(f)
                
            # Check if source file has changed
            with open(yaml_file, 'r', encoding='utf-8') as f:
                current_hash = self._get_content_hash(f.read())
                
            if cache_data.get('source_hash') == current_hash:
                return cache_data.get('translated_data')
        except:
            pass
        return None
    
    def _save_translation_cache(self, yaml_file: Path, target_lang: str, 
                               translated_data: dict, source_hash: str):
        """Save translation to cache"""
        cache_file = self.cache_dir / f"{yaml_file.stem}_{target_lang}.json"
        cache_data = {
            'source_hash': source_hash,
            'translated_data': translated_data
        }
        with open(cache_file, 'w', encoding='utf-8') as f:
            json.dump(cache_data, f, ensure_ascii=False, indent=2)
    
    def _translate_value(self, value: Any, target_lang: str, context: str = "") -> Any:
        """Translate a single value using the translation system"""
        if isinstance(value, str) and value.strip():
            # Skip translation for certain patterns
            if value.startswith(('http://', 'https://', '/', '#', 'fas ', 'fab ')):
                return value
            if len(value) < 3:  # Skip very short strings
                return value
            # Skip translation for fields that should remain in English
            skip_fields = ['.id', '.url', '.link', '.href', '.category', '.icon', 
                          '.image', '.alt', '.ui_version', '.hero_version', 
                          '.calendly_url', '.video_link']
            if any(context.endswith(field) for field in skip_fields):
                return value
                
            # Use existing translation system
            try:
                translated = self.translation_system.translate_with_anthropic(
                    value, 
                    target_lang,
                    source_lang="en"
                )
                return translated if translated else value
            except Exception as e:
                print(f"    ⚠️  Translation failed for '{value[:50]}...': {str(e)}")
                return value
            
        elif isinstance(value, dict):
            return {k: self._translate_value(v, target_lang, f"{context}.{k}") 
                   for k, v in value.items()}
                   
        elif isinstance(value, list):
            return [self._translate_value(item, target_lang, f"{context}[{i}]") 
                   for i, item in enumerate(value)]
        else:
            return value
    
    def translate_yaml_file(self, yaml_file: Path, target_lang: str, 
                           force: bool = False) -> dict:
        """Translate a YAML file to target language"""
        # Check cache first
        if not force:
            cached = self._load_translation_cache(yaml_file, target_lang)
            if cached:
                print(f"  ✅ Using cached translation for {yaml_file.name} -> {target_lang}")
                return cached
        
        print(f"  🔄 Translating {yaml_file.name} -> {target_lang}")
        
        # Load source YAML
        with open(yaml_file, 'r', encoding='utf-8') as f:
            source_data = yaml.safe_load(f)
            source_content = f.read()
        
        # Translate recursively
        translated_data = self._translate_value(source_data, target_lang, yaml_file.stem)
        
        # Save to cache
        self._save_translation_cache(
            yaml_file, target_lang, translated_data, 
            self._get_content_hash(source_content)
        )
        
        return translated_data
    
    def generate_translated_yaml_files(self, target_langs: Optional[List[str]] = None,
                                     output_dir: Optional[Path] = None):
        """Generate translated YAML files for all target languages"""
        if target_langs is None:
            target_langs = list(self.translation_system.languages.keys())
        
        if output_dir is None:
            output_dir = self.src_data_dir
            
        # Find all YAML files
        yaml_files = list(self.src_data_dir.rglob("*.yaml"))
        print(f"\n📁 Found {len(yaml_files)} YAML files to translate")
        
        for lang in target_langs:
            if lang == 'en':  # Skip English
                continue
                
            print(f"\n🌍 Processing language: {lang}")
            lang_dir = output_dir / f"_{lang}"
            lang_dir.mkdir(exist_ok=True, parents=True)
            
            for yaml_file in yaml_files:
                # Maintain directory structure
                relative_path = yaml_file.relative_to(self.src_data_dir)
                output_file = lang_dir / relative_path
                output_file.parent.mkdir(exist_ok=True, parents=True)
                
                try:
                    # Translate the file
                    translated_data = self.translate_yaml_file(yaml_file, lang)
                    
                    # Save translated YAML
                    with open(output_file, 'w', encoding='utf-8') as f:
                        yaml.dump(translated_data, f, allow_unicode=True, 
                                default_flow_style=False, sort_keys=False)
                    
                    print(f"    ✅ {relative_path}")
                except Exception as e:
                    print(f"    ❌ {relative_path}: {str(e)}")


def integrate_with_supplementary_generator():
    """
    Modify the supplementary generator to load language-specific YAML files.
    This function shows how to integrate the translation system.
    """
    integration_code = '''
# In supplementary_site_generator.py or generate_supplementary_multilingual.py

def load_all_supplementary_pages(locale_code='en'):
    """Load all supplementary pages from YAML files with language support"""
    all_pages = []
    
    # Determine data directory based on locale
    if locale_code != 'en' and locale_code:
        data_dir = Path(f'src/.data/_{locale_code}')
        if not data_dir.exists():
            # Fallback to English if translated version doesn't exist
            data_dir = Path('src/.data')
    else:
        data_dir = Path('src/.data')
    
    # Rest of the loading logic remains the same...
    for yaml_file in data_dir.rglob('*.yaml'):
        if yaml_file.stem == 'supplementary_pages':
            continue
        # Load and process YAML files...
    '''
    print("\n📝 Integration example:")
    print(integration_code)


if __name__ == "__main__":
    import click
    
    @click.command()
    @click.option('--langs', '-l', multiple=True, help='Target languages (defaults to all enabled)')
    @click.option('--force', '-f', is_flag=True, help='Force regeneration, ignore cache')
    @click.option('--integrate', '-i', is_flag=True, help='Show integration instructions')
    def main(langs, force, integrate):
        """Generate translated YAML files for supplementary pages"""
        
        if integrate:
            integrate_with_supplementary_generator()
            return
            
        translator = YAMLTranslator()
        
        # Clear cache if forced
        if force:
            print("🗑️  Clearing translation cache...")
            shutil.rmtree(translator.cache_dir, ignore_errors=True)
            translator.cache_dir.mkdir(exist_ok=True)
        
        # Generate translations
        target_langs = list(langs) if langs else None
        translator.generate_translated_yaml_files(target_langs)
        
        print("\n✅ YAML translation complete!")
        print("\n📌 Next steps:")
        print("1. Run: python generate_supplementary_multilingual.py")
        print("2. The system will automatically use translated YAML files")
        
    main()