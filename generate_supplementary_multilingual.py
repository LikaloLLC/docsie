#!/usr/bin/env python3
"""
Generate supplementary pages for all languages.
This extends the supplementary_site_generator.py to support multiple languages.
"""

from staticjinja import Site
from jinja2 import Environment
import gettext
import os
import sys
import yaml
import shutil
from pathlib import Path

# Import functions from the original supplementary generator
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from supplementary_site_generator import (
    is_hidden, copy_styles, load_component_data, 
    load_all_supplementary_pages, render_component_with_version,
    ensure_styles, get_available_css_files
)
from main import CustomSite
from utils.jinja_image_filter import register_filters

def load_supplementary_pages_for_language(locale_code='en'):
    """Load supplementary pages with language support"""
    pages_data = []
    data_dir = Path('src/.data')
    
    if not data_dir.exists():
        print(f"Error: Data directory not found at {data_dir}")
        return pages_data
    
    # For non-English, check if translated YAML exists
    if locale_code != 'en':
        # Try to load from language-specific directory first
        lang_data_dir = data_dir / f"_{locale_code}"
        if lang_data_dir.exists():
            print(f"  Loading translated YAML files from {lang_data_dir}")
            # Load from translated directory
            for yaml_file in lang_data_dir.rglob('*.yaml'):
                if yaml_file.stem in ['supplementary_pages', 'reviews']:
                    continue
                    
                # Skip nested language directories
                relative_path = yaml_file.relative_to(lang_data_dir)
                if any(part.startswith('_') for part in relative_path.parts[:-1]):
                    continue
                    
                try:
                    with open(yaml_file, 'r', encoding='utf-8') as f:
                        page_data = yaml.safe_load(f)
                        
                    if page_data:
                        if isinstance(page_data, list):
                            pages_data.extend(page_data)
                        else:
                            pages_data.append(page_data)
                        print(f"    Loaded: {yaml_file.relative_to(lang_data_dir)}")
                            
                except Exception as e:
                    print(f"    Error loading {yaml_file}: {e}")
                    
            if pages_data:
                print(f"  Total translated pages loaded: {len(pages_data)}")
                return pages_data
            else:
                print(f"  No translated pages found, falling back to English")
    
    # Fallback to English or load English directly
    return load_all_supplementary_pages()

def adjust_links_for_language(data, locale_code, output_base=''):
    """Recursively adjust all links in data structure to point to language-specific versions"""
    if locale_code == 'en':
        return data
        
    # Use output_base if provided, otherwise use locale_code
    lang_prefix = output_base if output_base else locale_code
        
    if isinstance(data, dict):
        for key, value in data.items():
            if key in ['link', 'url', 'href', 'action'] and isinstance(value, str):
                # Skip external links
                if value.startswith('http://') or value.startswith('https://') or value.startswith('#') or value.startswith('mailto:'):
                    continue
                # Skip if already has language prefix
                if value.startswith(f'/{lang_prefix}/'):
                    continue
                # Add language prefix
                if value.startswith('/'):
                    data[key] = f'/{lang_prefix}{value}'
            elif isinstance(value, (dict, list)):
                adjust_links_for_language(value, locale_code, output_base)
    elif isinstance(data, list):
        for item in data:
            if isinstance(item, (dict, list)):
                adjust_links_for_language(item, locale_code, output_base)
    return data

def generate_supplementary_pages_for_language(locale_code, locale_dir, output_base=''):
    """Generate supplementary pages for a specific language"""
    print(f"\n🔧 Generating supplementary pages for {locale_code}...")
    
    # Setup locale
    if locale_code != 'en':
        try:
            # Handle special cases
            actual_locale = locale_code
            
            # Load translation
            translation = gettext.translation(
                'messages',
                localedir=locale_dir,
                languages=[actual_locale]
            )
            translation.install()
            _ = translation.gettext
        except FileNotFoundError:
            print(f"Warning: Translation not found for {locale_code}, using English")
            _ = lambda x: x
    else:
        _ = lambda x: x
    
    
    # Create custom site for this language
    site = CustomSite.make_site(
        searchpath='./src',
        outpath=output_base or '.',
        env_globals={
            "locale": f"/{locale_code}" if locale_code != 'en' else '/',
            "lang": locale_code,  # Pass the language code for the HTML lang attribute
            "_": _,
            "gettext": _,
            "render_component": lambda name, config, **kwargs: render_component_with_version(
                site._env, name, config, 'v2', **kwargs
            )
        },
        extensions=['jinja2.ext.i18n', 'jinja_markdown.MarkdownExtension']
    )
    
    # Install translations in Jinja environment
    if locale_code != 'en':
        try:
            site._env.install_gettext_translations(translation)
        except:
            pass
    
    # Register custom image optimization filters
    register_filters(site._env)
    
    # Import language helpers into the environment
    site._env.globals.update({
        'lang_helpers': {
            'abs_lang_url': lambda path: f"/{locale_code}/{path}" if locale_code != 'en' else f"/{path}"
        }
    })
    
    # Use V2 template
    template = site._env.get_template('.templates/supplementary_page_v2.html')
    
    # Load all page data with language support
    pages_data = load_supplementary_pages_for_language(locale_code)
    
    # Adjust all links in pages data for the current language
    if locale_code != 'en':
        for page in pages_data:
            adjust_links_for_language(page, locale_code, output_base)
    
    # Create lookup dictionary
    pages_by_url = {}
    for page in pages_data:
        page_id = page.get('id', '')
        category = page.get('category', '').lower()
        if category and category != 'solutions':
            url = f"/solutions/{category}/{page_id}"
        else:
            url = f"/solutions/{page_id}"
        pages_by_url[url] = page
        pages_by_url[url + "/"] = page
    
    # Define lookup function
    def get_page_by_url(url):
        clean_url = url.rstrip('/')
        return pages_by_url.get(clean_url) or pages_by_url.get(clean_url + "/")
    
    site._env.globals['get_page_by_url'] = get_page_by_url
    
    # Load component configurations
    components_data = load_component_data()
    
    # Create base output directory
    if locale_code == 'en':
        base_dir = 'solutions'
    else:
        base_dir = os.path.join(output_base or locale_code, 'solutions')
    
    os.makedirs(base_dir, exist_ok=True)
    
    # Copy styles to language-specific directory
    if locale_code == 'en':
        # Only copy styles for English (they're the same for all languages)
        copy_styles()
    
    # Generate each page
    generated_count = 0
    for page in pages_data:
        try:
            # Force UI version
            page['ui_version'] = 'v2'
            
            # Generate the URL for this page
            category = page.get('category', '').lower()
            if category and category != 'solutions':
                page_url = f"/solutions/{category}/{page['id']}/"
            else:
                page_url = f"/solutions/{page['id']}/"
            
            # Add language prefix for non-English pages
            if locale_code != 'en':
                # Handle Japanese special case
                if locale_code == 'jp':
                    landing_url = f"/jp{page_url}"
                else:
                    landing_url = f"/{locale_code}{page_url}"
            else:
                landing_url = page_url
            
            # Create context
            context = {
                'page': page,
                'components': components_data,
                'styles_path': '/styles',
                'available_css': get_available_css_files(),
                'get_page_by_url': get_page_by_url,
                'locale': f"/{locale_code}" if locale_code != 'en' else '/',
                'landing_url': landing_url,  # Add canonical URL
                'lang': 'ja' if locale_code == 'jp' else locale_code,  # Language code for HTML lang attribute
                '_': _,
                'gettext': _
            }
            
            output = template.render(**context)
            
            # Create output path
            category = page.get('category', '').lower()
            if category and category != 'solutions':
                output_path = os.path.join(base_dir, category, page['id'], 'index.html')
            else:
                output_path = os.path.join(base_dir, page['id'], 'index.html')
            
            # Ensure directory exists
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            
            # Write the file
            with open(output_path, 'w', encoding='utf-8') as file:
                file.write(output)
            
            generated_count += 1
            
        except Exception as e:
            print(f"Error processing page {page.get('id', 'unknown')}: {str(e)}")
    
    print(f"✅ Generated {generated_count} supplementary pages for {locale_code}")

def load_enabled_languages():
    """Load only enabled languages from translation_config.yaml"""
    config_file = Path('translation_config.yaml')
    if not config_file.exists():
        print("❌ translation_config.yaml not found!")
        return []
    
    with open(config_file, 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)
    
    enabled_languages = []
    for code, lang_config in config.get('languages', {}).items():
        if lang_config.get('enabled', False):
            enabled_languages.append(code)
    
    return enabled_languages

def main():
    """Generate supplementary pages for all languages"""
    print("🚀 Starting multilingual supplementary page generation...")
    
    # Get locale directory
    locale_path = 'locale'
    if not os.path.exists(locale_path):
        print(f"❌ Locale directory '{locale_path}' not found!")
        return
    
    # Ensure styles are copied first
    ensure_styles()
    
    # Generate for English first
    print("\n📝 Generating English supplementary pages...")
    generate_supplementary_pages_for_language('en', locale_path)
    
    # Get only enabled languages from config
    enabled_languages = load_enabled_languages()
    if not enabled_languages:
        print("❌ No enabled languages found in config!")
        return
    
    # Filter to only include languages that have compiled translations
    languages = []
    for lang_code in enabled_languages:
        item_path = os.path.join(locale_path, lang_code)
        if os.path.isdir(item_path):
            # Check if it has compiled messages
            mo_file = os.path.join(item_path, 'LC_MESSAGES', 'messages.mo')
            if os.path.exists(mo_file):
                languages.append(lang_code)
            else:
                print(f"⚠️  Warning: {lang_code} is enabled but has no compiled translations")
    
    print(f"\nFound {len(languages)} enabled languages with translations")
    
    # Generate for each language
    for locale_code in sorted(languages):
        # Special handling for Japanese
        if locale_code == 'ja':
            output_dir = 'jp'
        else:
            output_dir = locale_code
            
        generate_supplementary_pages_for_language(locale_code, locale_path, output_dir)
    
    print("\n✅ All supplementary pages generated for all enabled languages!")

if __name__ == "__main__":
    main()