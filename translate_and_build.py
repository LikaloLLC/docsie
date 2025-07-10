#!/usr/bin/env python3
"""
Unified translation and build system for Docsie site
Combines all translation workflows into a single, DRY command
"""

import click
import subprocess
import sys
from pathlib import Path
from yaml_translator import YAMLTranslator
from translation_system import TranslationSystem
import time


class UnifiedTranslationBuilder:
    """Manages the complete translation and build workflow"""
    
    def __init__(self):
        self.translation_system = TranslationSystem()
        self.yaml_translator = YAMLTranslator(self.translation_system)
        
    def extract_strings(self):
        """Extract all translatable strings from templates and Python files"""
        print("\n📤 Extracting translatable strings...")
        
        # Extract from templates and Python files
        cmd = ["pybabel", "extract", "-F", "babel.cfg", "-o", "locale/messages.pot", "."]
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("  ✅ Extracted strings from templates and Python files")
        else:
            print(f"  ❌ Error extracting strings: {result.stderr}")
            return False
            
        return True
    
    def update_translations(self, langs=None):
        """Update translation files for all languages"""
        print("\n🔄 Updating translation files...")
        
        if langs is None:
            langs = list(self.translation_system.languages.keys())
            
        for lang in langs:
            if lang == 'en':
                continue
                
            po_file = Path(f"locale/{lang}/LC_MESSAGES/messages.po")
            
            if po_file.exists():
                # Update existing
                cmd = ["pybabel", "update", "-i", "locale/messages.pot", 
                       "-d", "locale", "-l", lang]
            else:
                # Initialize new
                cmd = ["pybabel", "init", "-i", "locale/messages.pot", 
                       "-d", "locale", "-l", lang]
                
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode == 0:
                print(f"  ✅ Updated {lang}")
            else:
                print(f"  ❌ Error updating {lang}: {result.stderr}")
    
    def translate_missing(self, langs=None):
        """Translate missing strings using Claude API"""
        print("\n🤖 Translating missing strings...")
        
        # Use the translation system's translate command
        from translation_system import translate_command
        
        # Prepare context for the translate command
        ctx = type('Context', (), {})()
        ctx.obj = self.translation_system
        
        try:
            translate_command.callback(
                all=True,
                extract=False,
                compile=True,
                force=False,
                stats=True,
                parallel=4,
                verbose=False,
                langs=langs or []
            )
            print("  ✅ Translations complete")
            return True
        except Exception as e:
            print(f"  ❌ Translation error: {e}")
            return False
    
    def translate_yaml_files(self, langs=None, force=False):
        """Translate all YAML content files"""
        print("\n📄 Translating YAML files...")
        
        self.yaml_translator.generate_translated_yaml_files(
            target_langs=langs,
            output_dir=Path("src/.data")
        )
        
        print("  ✅ YAML translations complete")
        return True
    
    def compile_translations(self, langs=None):
        """Compile .po files to .mo files"""
        print("\n📦 Compiling translations...")
        
        if langs is None:
            langs = list(self.translation_system.languages.keys())
            
        for lang in langs:
            if lang == 'en':
                continue
                
            cmd = ["pybabel", "compile", "-d", "locale", "-l", lang]
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                print(f"  ✅ Compiled {lang}")
            else:
                print(f"  ❌ Error compiling {lang}: {result.stderr}")
    
    def generate_multilingual_site(self, langs=None):
        """Generate the complete multilingual site"""
        print("\n🌍 Generating multilingual site...")
        
        # Generate main pages
        print("  📄 Generating main pages...")
        result = subprocess.run([sys.executable, "generate_all_languages.py"], 
                              capture_output=True, text=True)
        if result.returncode != 0:
            print(f"  ❌ Error generating main pages: {result.stderr}")
            return False
            
        # Generate supplementary pages
        print("  📑 Generating supplementary pages...")
        result = subprocess.run([sys.executable, "generate_supplementary_multilingual.py"], 
                              capture_output=True, text=True)
        if result.returncode != 0:
            print(f"  ❌ Error generating supplementary pages: {result.stderr}")
            return False
            
        print("  ✅ Site generation complete")
        return True
    
    def run_full_workflow(self, langs=None, skip_extract=False, skip_yaml=False, 
                         skip_translate=False, skip_generate=False):
        """Run the complete translation and build workflow"""
        start_time = time.time()
        
        print("🚀 Starting unified translation and build workflow...")
        print(f"   Languages: {langs or 'all enabled'}")
        
        # Step 1: Extract strings
        if not skip_extract:
            if not self.extract_strings():
                return False
                
            if not self.update_translations(langs):
                return False
        
        # Step 2: Translate missing strings
        if not skip_translate:
            if not self.translate_missing(langs):
                print("  ⚠️  Translation failed, continuing...")
        
        # Step 3: Translate YAML files
        if not skip_yaml:
            if not self.translate_yaml_files(langs):
                print("  ⚠️  YAML translation failed, continuing...")
        
        # Step 4: Compile translations
        self.compile_translations(langs)
        
        # Step 5: Generate site
        if not skip_generate:
            if not self.generate_multilingual_site(langs):
                return False
        
        elapsed = time.time() - start_time
        print(f"\n✅ Workflow complete in {elapsed:.1f} seconds!")
        return True


@click.command()
@click.option('--langs', '-l', multiple=True, 
              help='Target languages (e.g., -l de -l es). Defaults to all enabled.')
@click.option('--skip-extract', is_flag=True, 
              help='Skip string extraction step')
@click.option('--skip-yaml', is_flag=True, 
              help='Skip YAML translation step')
@click.option('--skip-translate', is_flag=True, 
              help='Skip API translation step')
@click.option('--skip-generate', is_flag=True, 
              help='Skip site generation step')
@click.option('--extract-only', is_flag=True, 
              help='Only extract strings and exit')
@click.option('--yaml-only', is_flag=True, 
              help='Only translate YAML files and exit')
@click.option('--quick', '-q', is_flag=True, 
              help='Quick mode: skip extraction and API translation')
def main(langs, skip_extract, skip_yaml, skip_translate, skip_generate, 
         extract_only, yaml_only, quick):
    """
    Unified translation and build system for Docsie site.
    
    This command combines all translation workflows into a single, DRY process:
    
    1. Extract translatable strings from templates
    2. Translate missing strings using Claude API  
    3. Translate YAML content files
    4. Compile translations
    5. Generate multilingual site
    
    Examples:
    
        # Full workflow for all languages
        python translate_and_build.py
        
        # Quick rebuild (skip extraction and API translation)
        python translate_and_build.py --quick
        
        # Specific languages only
        python translate_and_build.py -l de -l fr -l es
        
        # Only translate YAML files
        python translate_and_build.py --yaml-only
    """
    
    builder = UnifiedTranslationBuilder()
    
    # Convert language list
    target_langs = list(langs) if langs else None
    
    # Handle special modes
    if extract_only:
        builder.extract_strings()
        builder.update_translations(target_langs)
        return
        
    if yaml_only:
        builder.translate_yaml_files(target_langs)
        return
    
    # Quick mode settings
    if quick:
        skip_extract = True
        skip_translate = True
    
    # Run full workflow
    success = builder.run_full_workflow(
        langs=target_langs,
        skip_extract=skip_extract,
        skip_yaml=skip_yaml,
        skip_translate=skip_translate,
        skip_generate=skip_generate
    )
    
    if not success:
        sys.exit(1)


if __name__ == "__main__":
    main()