#!/usr/bin/env python3
"""
Translation System for Docsie Site
Automated extraction, translation, and compilation of internationalization strings
"""

import os
import sys
import json
import subprocess
import time
import yaml
import hashlib
import pickle
from pathlib import Path
from typing import Dict, List, Optional
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading
import anthropic
from babel.messages import Catalog
from babel.messages.pofile import read_po, write_po
from babel.messages.extract import extract_from_dir
from babel.messages.mofile import write_mo
import click
from dotenv import load_dotenv


class TranslationSystem:
    """Main translation system manager"""
    
    def __init__(self, project_root: str = ".", config_file: str = "translation_config.yaml"):
        self.project_root = Path(project_root).resolve()
        self.config_file = self.project_root / config_file
        
        # Load environment variables from .env file
        env_file = self.project_root / ".env"
        if env_file.exists():
            load_dotenv(env_file)
            print(f"✅ Loaded .env from {env_file}")
        else:
            print(f"⚠️  No .env file found at {env_file}")
        
        # Load configuration
        self.config = self.load_config()
        
        # Set paths from config
        self.locale_dir = self.project_root / self.config['project']['locale_dir']
        self.src_dir = self.project_root / self.config['project']['source_dir']
        
        # Get enabled languages from config
        self.languages = {
            code: info for code, info in self.config['languages'].items()
            if info.get('enabled', False)
        }
        
        # API settings
        self.api_config = self.config.get('anthropic', {})
        
        # Translation settings
        self.translation_config = self.config.get('translation', {})
        
        self.client = None
        
        # Initialize caching and threading
        self.cache_dir = self.project_root / ".translation_cache"
        self._init_cache()
        self._lock = threading.Lock()
        
    def load_config(self) -> dict:
        """Load configuration from YAML file"""
        if not self.config_file.exists():
            print(f"⚠️  No config file found at {self.config_file}, using defaults")
            return self.get_default_config()
            
        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f)
                print(f"✅ Loaded configuration from {self.config_file}")
                return config
        except Exception as e:
            print(f"❌ Error loading config: {e}")
            return self.get_default_config()
    
    def _init_cache(self):
        """Initialize translation cache"""
        if self.api_config.get('cache_translations', True):
            self.cache_dir.mkdir(exist_ok=True)
            self.cache_file = self.cache_dir / "translations.pkl"
            
            # Load existing cache
            if self.cache_file.exists():
                try:
                    with open(self.cache_file, 'rb') as f:
                        self.cache = pickle.load(f)
                    print(f"✅ Loaded {len(self.cache)} cached translations")
                except Exception:
                    self.cache = {}
            else:
                self.cache = {}
        else:
            self.cache = None
    
    def _get_cache_key(self, text: str, target_lang: str, source_lang: str = "en") -> str:
        """Generate cache key for translation"""
        content = f"{source_lang}->{target_lang}:{text}"
        return hashlib.sha256(content.encode()).hexdigest()
    
    def _get_cached_translation(self, text: str, target_lang: str, source_lang: str = "en") -> Optional[str]:
        """Get cached translation if available"""
        if not self.cache:
            return None
            
        key = self._get_cache_key(text, target_lang, source_lang)
        return self.cache.get(key)
    
    def _cache_translation(self, text: str, target_lang: str, translation: str, source_lang: str = "en"):
        """Cache a translation"""
        if not self.cache:
            return
            
        key = self._get_cache_key(text, target_lang, source_lang)
        with self._lock:
            self.cache[key] = translation
            
            # Save cache periodically
            try:
                with open(self.cache_file, 'wb') as f:
                    pickle.dump(self.cache, f)
            except Exception as e:
                print(f"⚠️  Failed to save cache: {e}")
            
    def get_default_config(self) -> dict:
        """Get default configuration"""
        return {
            'project': {
                'name': 'Docsie',
                'source_language': 'en',
                'source_dir': 'src/',
                'locale_dir': 'locale/'
            },
            'languages': {
                'es': {'name': 'Español', 'enabled': True, 'rtl': False},
                'fr': {'name': 'Français', 'enabled': True, 'rtl': False},
                'de': {'name': 'Deutsch', 'enabled': True, 'rtl': False},
                'pt': {'name': 'Português', 'enabled': True, 'rtl': False},
                'ar': {'name': 'العربية', 'enabled': True, 'rtl': True}
            },
            'anthropic': {
                'model': 'claude-sonnet-4-20250514',
                'temperature': 0.1,
                'max_tokens': 1000,
                'batch_size': 20,
                'delay_between_batches': 1
            },
            'translation': {
                'skip_existing': True,
                'terminology': {'Docsie': 'Docsie'}
            }
        }
        
    def setup_babel_config(self):
        """Create babel.cfg file"""
        babel_cfg_path = self.project_root / "babel.cfg"
        with open(babel_cfg_path, 'w') as f:
            f.write("""[python: **.py]
[jinja2: **/templates/**.html]
[jinja2: **/src/**.html]
[jinja2: **.html]
""")
        print(f"✅ Created babel.cfg at {babel_cfg_path}")
        
    def extract_strings(self) -> bool:
        """Extract translatable strings from source files"""
        print("🔍 Extracting translatable strings...")
        
        # Ensure locale directory exists
        self.locale_dir.mkdir(exist_ok=True)
        
        # Create babel.cfg if it doesn't exist
        self.setup_babel_config()
        
        # Extract strings using pybabel
        pot_file = self.locale_dir / "messages.pot"
        
        try:
            # Try using pybabel directly first, then fallback to python -m babel.messages.frontend
            cmd = [
                sys.executable, "-m", "babel.messages.frontend", "extract",
                "-F", "babel.cfg",
                "-k", "trans",
                "-o", str(pot_file),
                "src/"
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, cwd=self.project_root)
            
            if result.returncode != 0:
                print(f"❌ Error extracting strings: {result.stderr}")
                return False
                
            print(f"✅ Extracted strings to {pot_file}")
            
            # Count extracted strings
            if pot_file.exists():
                with open(pot_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    string_count = content.count('msgid "')
                    print(f"📊 Found {string_count} translatable strings")
                    
            return True
            
        except Exception as e:
            print(f"❌ Error during extraction: {e}")
            return False
            
    def init_language(self, lang_code: str) -> bool:
        """Initialize a new language"""
        print(f"🌍 Initializing language: {lang_code} ({self.languages.get(lang_code, lang_code)})")
        
        pot_file = self.locale_dir / "messages.pot"
        if not pot_file.exists():
            print("❌ No .pot file found. Run extract_strings first.")
            return False
            
        try:
            cmd = [
                sys.executable, "-m", "babel.messages.frontend", "init",
                "-i", str(pot_file),
                "-d", str(self.locale_dir),
                "-l", lang_code
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, cwd=self.project_root)
            
            if result.returncode != 0:
                print(f"❌ Error initializing {lang_code}: {result.stderr}")
                return False
                
            print(f"✅ Initialized {lang_code} language files")
            return True
            
        except Exception as e:
            print(f"❌ Error initializing {lang_code}: {e}")
            return False
            
    def update_language(self, lang_code: str) -> bool:
        """Update existing language files with new strings"""
        print(f"🔄 Updating language: {lang_code}")
        
        pot_file = self.locale_dir / "messages.pot"
        if not pot_file.exists():
            print("❌ No .pot file found. Run extract_strings first.")
            return False
            
        try:
            cmd = [
                sys.executable, "-m", "babel.messages.frontend", "update",
                "-i", str(pot_file),
                "-d", str(self.locale_dir),
                "-l", lang_code
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, cwd=self.project_root)
            
            if result.returncode != 0:
                print(f"❌ Error updating {lang_code}: {result.stderr}")
                return False
                
            print(f"✅ Updated {lang_code} language files")
            return True
            
        except Exception as e:
            print(f"❌ Error updating {lang_code}: {e}")
            return False
            
    def compile_language(self, lang_code: str) -> bool:
        """Compile .po files to .mo files"""
        print(f"📦 Compiling language: {lang_code}")
        
        try:
            cmd = [
                sys.executable, "-m", "babel.messages.frontend", "compile",
                "-d", str(self.locale_dir),
                "-l", lang_code
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, cwd=self.project_root)
            
            if result.returncode != 0:
                print(f"❌ Error compiling {lang_code}: {result.stderr}")
                return False
                
            print(f"✅ Compiled {lang_code} language files")
            return True
            
        except Exception as e:
            print(f"❌ Error compiling {lang_code}: {e}")
            return False
            
    def setup_anthropic_client(self, api_key: str):
        """Setup Anthropic client for translation"""
        self.client = anthropic.Anthropic(api_key=api_key)
        print("✅ Anthropic client initialized")
        
    def translate_with_anthropic(self, text: str, target_lang: str, source_lang: str = "en") -> str:
        """Translate text using Anthropic API with caching"""
        if not self.client:
            raise ValueError("Anthropic client not initialized")
        
        # Check cache first
        cached_translation = self._get_cached_translation(text, target_lang, source_lang)
        if cached_translation:
            return cached_translation
            
        # Get language info from config or use defaults
        lang_info = self.languages.get(target_lang, {})
        target_lang_name = lang_info.get('name', target_lang)
        
        # Skip if translation should be preserved (terminology)
        terminology = self.translation_config.get('terminology', {})
        if text in terminology:
            preserved = terminology[text]
            self._cache_translation(text, target_lang, preserved, source_lang)
            return preserved
        
        # Build prompt with context from config
        context = self.translation_config.get('context', '')
        prompt = f"""You are a professional translator specializing in technical documentation and software interfaces.

{context}

Please translate the following text from {self.config['project']['source_language'].upper()} to {target_lang_name}:

"{text}"

Requirements:
- Maintain the same tone and style appropriate for a professional documentation platform
- Keep technical terms accurate and consistent
- If the text contains HTML tags, preserve them exactly
- For software interface elements, use standard conventions for {target_lang_name}
- Return ONLY the translated text, no explanations or additional content

Translation:"""

        try:
            message = self.client.messages.create(
                model=self.api_config.get('model', 'claude-3-sonnet-20240229'),
                max_tokens=self.api_config.get('max_tokens', 1000),
                temperature=self.api_config.get('temperature', 0.1),
                messages=[{"role": "user", "content": prompt}]
            )
            
            translated_text = message.content[0].text.strip()
            
            # Cache the translation
            self._cache_translation(text, target_lang, translated_text, source_lang)
            
            return translated_text
            
        except Exception as e:
            print(f"❌ Translation error: {e}")
            return text  # Return original if translation fails
            
    def translate_po_file(self, lang_code: str, api_key: str, batch_size: int = None) -> bool:
        """Translate a .po file using Anthropic API"""
        if not api_key:
            print("❌ API key required for translation")
            return False
            
        self.setup_anthropic_client(api_key)
        
        # Use batch size from config if not provided
        if batch_size is None:
            batch_size = self.api_config.get('batch_size', 20)
            
        po_file = self.locale_dir / lang_code / "LC_MESSAGES" / "messages.po"
        
        if not po_file.exists():
            print(f"❌ No .po file found for {lang_code}")
            return False
            
        lang_info = self.languages.get(lang_code, {'name': lang_code})
        print(f"🤖 Translating to {lang_code} ({lang_info.get('name')})...")
        
        try:
            # Read the .po file
            with open(po_file, 'rb') as f:
                catalog = read_po(f)
                
            translated_count = 0
            total_count = len([msg for msg in catalog if msg.id])
            
            # Check if we should skip existing translations
            skip_existing = self.translation_config.get('skip_existing', True)
            
            # Translate messages in batches
            for i, message in enumerate(catalog):
                if message.id and (not message.string or not skip_existing):  # Translate based on config
                    try:
                        # Add delay to respect rate limits
                        if i > 0 and i % batch_size == 0:
                            delay = self.api_config.get('delay_between_batches', 1)
                            time.sleep(delay)
                            
                        translated_text = self.translate_with_anthropic(
                            message.id, 
                            lang_code
                        )
                        
                        message.string = translated_text
                        translated_count += 1
                        
                        # Progress indicator - show every translation for small batches
                        print(f"  📝 Translated {translated_count}/{total_count} strings: '{message.id[:50]}...' -> '{translated_text[:50]}...'")
                            
                    except Exception as e:
                        print(f"⚠️  Failed to translate: '{message.id}' - {e}")
                        continue
                        
            # Write back the translated .po file
            with open(po_file, 'wb') as f:
                write_po(f, catalog)
                
            print(f"✅ Translated {translated_count} strings for {lang_code}")
            return True
            
        except Exception as e:
            print(f"❌ Error translating {lang_code}: {e}")
            return False
    
    def translate_languages_parallel(self, languages: List[str], api_key: str, batch_size: int = None) -> Dict[str, bool]:
        """Translate multiple languages in parallel using ThreadPoolExecutor"""
        max_workers = self.api_config.get('max_concurrent_languages', 3)
        results = {}
        
        print(f"🚀 Starting parallel translation of {len(languages)} languages with {max_workers} threads")
        
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            # Submit all translation tasks
            future_to_lang = {
                executor.submit(self.translate_po_file, lang, api_key, batch_size): lang 
                for lang in languages
            }
            
            # Process completed translations
            for future in as_completed(future_to_lang):
                lang = future_to_lang[future]
                try:
                    result = future.result()
                    results[lang] = result
                    if result:
                        print(f"✅ Completed translation for {lang}")
                    else:
                        print(f"❌ Failed translation for {lang}")
                except Exception as e:
                    print(f"❌ Exception translating {lang}: {e}")
                    results[lang] = False
        
        # Summary
        successful = sum(1 for success in results.values() if success)
        print(f"📊 Translation summary: {successful}/{len(languages)} languages completed successfully")
        
        return results
            
    def create_language_picker_data(self) -> bool:
        """Create language picker data file"""
        print("📄 Creating language picker data...")
        
        # Create language data for the picker
        language_data = {
            "default_language": self.config['project']['source_language'],
            "languages": {}
        }
        
        # Add source language
        source_lang = self.config['project']['source_language']
        language_data["languages"][source_lang] = {
            "name": "English",
            "code": source_lang,
            "enabled": True,
            "rtl": False,
            "url": "/"
        }
        
        # Check which languages actually exist
        for lang_code, lang_info in self.languages.items():
            if lang_info.get('enabled', False):
                lang_dir = self.locale_dir / lang_code / "LC_MESSAGES"
                po_file = lang_dir / "messages.po"
                mo_file = lang_dir / "messages.mo"
                
                if po_file.exists():
                    language_data["languages"][lang_code] = {
                        "name": lang_info.get('name', lang_code),
                        "code": lang_code,
                        "enabled": mo_file.exists(),
                        "rtl": lang_info.get('rtl', False),
                        "flag": f"flag-{lang_code}" if self.config['ui']['language_picker']['show_flag_icons'] else None,
                        "url": f"/{lang_code}/" if lang_code != source_lang else "/"
                    }
                
        # Write language data file
        lang_data_file = self.project_root / "src" / "assets" / "languages.json"
        lang_data_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(lang_data_file, 'w', encoding='utf-8') as f:
            json.dump(language_data, f, indent=2, ensure_ascii=False)
            
        print(f"✅ Created language data at {lang_data_file}")
        return True
        
    def update_footer_language_picker(self) -> bool:
        """Update footer to show language picker"""
        print("🔄 Updating footer language picker...")
        
        footer_file = self.project_root / "src" / "_footer_v2.html"
        
        if not footer_file.exists():
            print("❌ Footer file not found")
            return False
            
        # Read current footer
        with open(footer_file, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Language picker HTML
        language_picker_html = """
        <!-- Language Picker -->
        <div class="relative">
          <button id="language-picker-btn" class="flex items-center gap-2 px-3 py-2 bg-white/10 rounded-lg hover:bg-white/20 transition-colors duration-300">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 5h12M9 3v2m1.048 9.5A18.022 18.022 0 016.412 9m6.088 9h7M11 21l5-10 5 10M12.751 5C11.783 10.77 8.07 15.61 3 18.129"/>
            </svg>
            <span id="current-language">English</span>
            <svg class="w-4 h-4 transition-transform duration-200" id="language-chevron" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"/>
            </svg>
          </button>
          
          <div id="language-dropdown" class="absolute bottom-full left-0 mb-2 w-48 bg-white rounded-lg shadow-xl border border-gray-200 hidden z-50">
            <div class="py-2" id="language-options">
              <!-- Languages will be populated by JavaScript -->
            </div>
          </div>
        </div>
        
        <script>
        // Language picker functionality
        document.addEventListener('DOMContentLoaded', function() {
          const languageBtn = document.getElementById('language-picker-btn');
          const dropdown = document.getElementById('language-dropdown');
          const chevron = document.getElementById('language-chevron');
          const currentLang = document.getElementById('current-language');
          const optionsContainer = document.getElementById('language-options');
          
          // Load language data
          fetch('/assets/languages.json')
            .then(response => response.json())
            .then(data => {
              // Populate dropdown
              Object.entries(data.languages).forEach(([code, info]) => {
                if (info.enabled) {
                  const option = document.createElement('a');
                  option.href = info.url;
                  option.className = 'block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 transition-colors duration-200';
                  option.innerHTML = `
                    <span class="font-medium">${info.name}</span>
                    <span class="text-gray-500 ml-2">${code.toUpperCase()}</span>
                  `;
                  optionsContainer.appendChild(option);
                }
              });
              
              // Set current language
              const currentCode = document.documentElement.lang || 'en';
              const currentInfo = data.languages[currentCode];
              if (currentInfo) {
                currentLang.textContent = currentInfo.name;
              }
            })
            .catch(error => console.error('Error loading languages:', error));
          
          // Toggle dropdown
          languageBtn.addEventListener('click', function() {
            dropdown.classList.toggle('hidden');
            chevron.classList.toggle('rotate-180');
          });
          
          // Close dropdown when clicking outside
          document.addEventListener('click', function(e) {
            if (!languageBtn.contains(e.target) && !dropdown.contains(e.target)) {
              dropdown.classList.add('hidden');
              chevron.classList.remove('rotate-180');
            }
          });
        });
        </script>"""
        
        # Replace the language picker placeholder
        if "docsie-lang-picker-container" in content:
            content = content.replace(
                '<div class="docsie-lang-picker-container">',
                f'<div class="docsie-lang-picker-container">{language_picker_html}'
            )
        else:
            # If no placeholder, add before the closing footer tag
            content = content.replace(
                '</div>\n    \n  </div>\n</footer>',
                f'        {language_picker_html}\n        \n      </div>\n    \n  </div>\n</footer>'
            )
            
        # Write updated footer
        with open(footer_file, 'w', encoding='utf-8') as f:
            f.write(content)
            
        print("✅ Updated footer with language picker")
        return True


@click.group()
def cli():
    """Docsie Translation System"""
    pass


@cli.command()
def extract():
    """Extract translatable strings from source files"""
    system = TranslationSystem()
    success = system.extract_strings()
    if success:
        system.create_language_picker_data()
        print("✅ Extraction completed successfully")
    else:
        print("❌ Extraction failed")
        sys.exit(1)


@cli.command()
@click.argument('languages', nargs=-1)
def init(languages):
    """Initialize new language(s)"""
    system = TranslationSystem()
    
    if not languages:
        # If no languages specified, init all enabled languages from config
        languages = [code for code, info in system.languages.items() if info.get('enabled', False)]
        if not languages:
            print("No enabled languages found in config. Available languages:")
            for code, info in system.config['languages'].items():
                status = "✅ Enabled" if info.get('enabled', False) else "❌ Disabled"
                rtl = "(RTL)" if info.get('rtl', False) else ""
                print(f"  {code}: {info['name']} {rtl} - {status}")
            return
        else:
            print(f"📋 Initializing all enabled languages: {', '.join(languages)}")
        
    for lang in languages:
        if lang not in system.config['languages']:
            print(f"❌ Unknown language: {lang}")
            continue
            
        system.init_language(lang)
        
    system.create_language_picker_data()


@cli.command()
@click.argument('languages', nargs=-1)
def update(languages):
    """Update existing language(s)"""
    system = TranslationSystem()
    
    if not languages:
        # Update all existing languages
        languages = []
        for lang_code in system.languages:
            lang_dir = system.locale_dir / lang_code / "LC_MESSAGES"
            if (lang_dir / "messages.po").exists():
                languages.append(lang_code)
                
    for lang in languages:
        system.update_language(lang)
        
    system.create_language_picker_data()


@cli.command()
@click.argument('languages', nargs=-1)
def compile(languages):
    """Compile language(s) to .mo files"""
    system = TranslationSystem()
    
    if not languages:
        # Compile all existing languages
        languages = []
        for lang_code in system.languages:
            lang_dir = system.locale_dir / lang_code / "LC_MESSAGES"
            if (lang_dir / "messages.po").exists():
                languages.append(lang_code)
                
    for lang in languages:
        system.compile_language(lang)
        
    system.create_language_picker_data()


@cli.command()
@click.argument('languages', nargs=-1)
@click.option('--api-key', help='Anthropic API key (overrides .env file)')
@click.option('--batch-size', help='Batch size for API calls (overrides config)')
def translate(languages, api_key, batch_size):
    """Translate language(s) using Anthropic API"""
    # Load .env file first
    env_file = Path(".") / ".env"
    if env_file.exists():
        load_dotenv(env_file)
        print(f"✅ Loaded .env from {env_file.resolve()}")
    
    # Get API key from parameter, environment variable, or .env file
    if not api_key:
        api_key = os.getenv('ANTHROPIC_API_KEY')
        if api_key:
            print(f"✅ Using API key from environment: {api_key[:10]}...")
        else:
            print("❌ No API key found in environment")
    
    if not api_key:
        print("❌ API key required. Add ANTHROPIC_API_KEY to .env file or use --api-key")
        print(f"🔍 Current working directory: {os.getcwd()}")
        print(f"🔍 Environment variables containing 'ANTHROPIC': {[k for k in os.environ.keys() if 'ANTHROPIC' in k]}")
        sys.exit(1)
        
    system = TranslationSystem()
    
    if not languages:
        # Translate all enabled languages from config
        languages = [code for code, info in system.languages.items() if info.get('enabled', False)]
        if not languages:
            print("❌ No enabled languages found in config")
            sys.exit(1)
        print(f"📋 Translating all enabled languages: {', '.join(languages)}")
        
    # Convert batch_size to int if provided
    batch_size = int(batch_size) if batch_size else None
    
    # Filter valid languages
    valid_languages = []
    for lang in languages:
        if lang not in system.config['languages']:
            print(f"❌ Unknown language: {lang}")
            continue
            
        if not system.languages.get(lang, {}).get('enabled', False):
            print(f"⚠️  Language {lang} is disabled in config, skipping")
            continue
            
        valid_languages.append(lang)
    
    if not valid_languages:
        print("❌ No valid languages to translate")
        sys.exit(1)
    
    # Use parallel translation if more than 1 language
    if len(valid_languages) > 1:
        system.translate_languages_parallel(valid_languages, api_key, batch_size)
    else:
        system.translate_po_file(valid_languages[0], api_key, batch_size)
        
    system.create_language_picker_data()


@cli.command()
@click.argument('languages', nargs=-1)
@click.option('--api-key', help='Anthropic API key (overrides .env file)')
@click.option('--all-enabled', is_flag=True, help='Setup all enabled languages from config')
def setup(languages, api_key, all_enabled):
    """Complete setup: extract, init, translate, and compile"""
    # Load .env file first
    env_file = Path(".") / ".env"
    if env_file.exists():
        load_dotenv(env_file)
        print(f"✅ Loaded .env from {env_file.resolve()}")
    
    system = TranslationSystem()
    
    # Step 1: Extract strings
    print("🔍 Step 1: Extracting strings...")
    if not system.extract_strings():
        print("❌ Failed to extract strings")
        sys.exit(1)
        
    # Determine which languages to setup
    if all_enabled or not languages:
        languages = [code for code, info in system.languages.items() if info.get('enabled', False)]
        print(f"📋 Setting up all enabled languages: {', '.join(languages)}")
        
    # Step 2: Initialize languages
    print("🌍 Step 2: Initializing languages...")
    for lang in languages:
        if lang not in system.config['languages']:
            print(f"❌ Unknown language: {lang}")
            continue
        system.init_language(lang)
        
    # Step 3: Translate (if API key provided)
    if not api_key:
        api_key = os.getenv('ANTHROPIC_API_KEY')
    
    if api_key:
        print("🤖 Step 3: Translating...")
        for lang in languages:
            if lang in system.languages:
                system.translate_po_file(lang, api_key)
                
    # Step 4: Compile
    print("📦 Step 4: Compiling...")
    for lang in languages:
        if lang in system.languages:
            system.compile_language(lang)
            
    # Step 5: Update UI
    print("🎨 Step 5: Updating UI...")
    system.create_language_picker_data()
    system.update_footer_language_picker()
    
    print("✅ Setup completed successfully!")


@cli.command()
def cache_status():
    """Show translation cache status"""
    system = TranslationSystem()
    
    if not system.cache:
        print("❌ Translation caching is disabled")
        return
        
    cache_file = system.cache_file
    print(f"📁 Cache file: {cache_file}")
    print(f"📊 Cached translations: {len(system.cache)}")
    
    if cache_file.exists():
        cache_size = cache_file.stat().st_size / 1024 / 1024  # MB
        print(f"💾 Cache size: {cache_size:.2f} MB")
        
        # Show cache breakdown by language
        lang_counts = {}
        for key in system.cache.keys():
            # Extract target language from cache key (format: hash of "en->lang:text")
            pass  # We'd need to reverse engineer this, but it's complex
            
        print(f"🗂️  Cache location: {cache_file}")
    else:
        print("📭 Cache file does not exist yet")


@cli.command()
@click.option('--confirm', is_flag=True, help='Confirm cache clearing')
def clear_cache(confirm):
    """Clear translation cache"""
    system = TranslationSystem()
    
    if not system.cache:
        print("❌ Translation caching is disabled")
        return
        
    if not confirm:
        print("⚠️  This will clear all cached translations.")
        print("Run with --confirm to proceed: python translation_system.py clear-cache --confirm")
        return
        
    system.cache.clear()
    if system.cache_file.exists():
        system.cache_file.unlink()
        
    print("✅ Translation cache cleared")


@cli.command()
def test_env():
    """Test .env file loading"""
    system = TranslationSystem()
    api_key = os.getenv('ANTHROPIC_API_KEY')
    print(f"🔍 Current directory: {os.getcwd()}")
    print(f"🔍 Project root: {system.project_root}")
    print(f"🔍 .env file exists: {(system.project_root / '.env').exists()}")
    print(f"🔍 API key found: {'Yes' if api_key else 'No'}")
    if api_key:
        print(f"🔍 API key preview: {api_key[:10]}...")


@cli.command()
def list_languages():
    """List all available languages"""
    system = TranslationSystem()
    print("\nLanguages configuration:")
    print(f"Source language: {system.config['project']['source_language']}\n")
    
    print("Available languages:")
    for lang_code, lang_info in system.config['languages'].items():
        # Check if initialized
        lang_dir = system.locale_dir / lang_code / "LC_MESSAGES"
        po_exists = (lang_dir / "messages.po").exists()
        mo_exists = (lang_dir / "messages.mo").exists()
        
        status = "✅" if mo_exists else "🔄" if po_exists else "❌"
        enabled = "[ENABLED]" if lang_info.get('enabled', False) else "[DISABLED]"
        rtl = "(RTL)" if lang_info.get('rtl', False) else ""
        
        print(f"  {status} {lang_code}: {lang_info['name']} {rtl} {enabled}")
    
    print("\nStatus legend:")
    print("  ✅ = Fully translated and compiled")
    print("  🔄 = Initialized but not compiled")
    print("  ❌ = Not initialized")


if __name__ == "__main__":
    cli()