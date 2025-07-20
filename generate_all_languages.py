#!/usr/bin/env python3
"""
Generate translated versions of the site for all languages in locale directory.
Based on the commented-out code in main.py
"""

from staticjinja import Site
from jinja2 import Environment, FileSystemLoader
import gettext
import os
import sys
from pathlib import Path
import feedparser
import dateutil.parser
import arrow
import yaml

# Import the custom classes from main.py
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from main import CustomSite, render_template_file, is_binary_file

# Legacy pages that should not be translated
LEGACY_PAGES_TO_SKIP = {
    '2020_websummit',
    'collision_2020',
    'collision_2021',
    'codepen',
    'carbon',
    'affiliate-program',
    'docsie_manager',
    'docsie_publishing',
    'docsie_product',
    'docsie_vocally',
    'docsie-free-consultation',
    'discovery_call',
    'feedback_preview_demo',
    'gather_feedback',
    'incident',
    'manager',
    'markdown_editor',
    'pilot',
    'press',
    'release_notes',
    'publish_documentation',
    'self-writing-documentation',
    'see-it-in-action',
    'software_documentation',
    'collaboration_software',
    'careers',
    'cookies',
    'investors',
    'resources',
    'terms',
    'support',
    'privacy',
    'about',
    'features',
    'documentation',
    'modern-home',
    'eml',
    'content',
    'validation_page',
    # Additional directories to skip
    'assets',
    'g2',
    'co-jp',
    'new_home',
    'pricing_v2',
    'styles',
    'try_docsie',
    'version_language',
    'vocally',
    'blog',
    'beta'
}

def generate_language_version(locale_dir, locale_code):
    """Generate site for a specific language."""
    print(f"\n🌐 Generating {locale_code} version...")
    
    # Special handling for locale codes
    if locale_code == 'ja':
        loc_name = '/jp'
    else:
        loc_name = '/' + locale_code
    
    # Get blog feeds (same as main.py)
    feed = feedparser.parse('https://www.docsie.io/blog/rss.xml?skip=1&limit=3').entries
    feed.reverse()

    feed_videos = feedparser.parse('https://www.youtube.com/feeds/videos.xml?channel_id=UCnQm591jTzvHwb003Y8e1XA').entries
    feed_videos.reverse()

    for f in feed:
        f['link'] = f['link'].replace('/blog/blog/', '/blog/')
        f['published'] = arrow.get(dateutil.parser.parse(f['published'])).humanize()

    for v in feed_videos:
        v['video_link'] = v['link'].replace('https://www.youtube.com/watch?v=', 'https://www.youtube.com/embed/')
        v['published'] = arrow.get(dateutil.parser.parse(v['published'])).humanize()
    
    # Create output directory
    if locale_code == 'en':
        outpath = '.'  # English goes to root
    elif locale_code == 'ja':
        outpath = 'jp'
        os.makedirs(outpath, exist_ok=True)
    else:
        outpath = locale_code
        os.makedirs(outpath, exist_ok=True)
    
    # Create site with locale
    site = CustomSite.make_site(
        searchpath='./src', 
        outpath=outpath,
        env_globals={
            "locale": loc_name,
            "lang": locale_code,  # Pass the language code for the HTML lang attribute
            "feed": feed[-12:][::-1],
            "videos": feed_videos
        },
        locale=locale_code, 
        extensions=['jinja2.ext.i18n', 'jinja_markdown.MarkdownExtension'],
        rules=[
            (".*", render_template_file)
        ]
    )
    
    # Render the site
    site.render(use_reloader=False)
    print(f"✅ Generated {locale_code} in '{outpath}' directory")

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
    """Generate all language versions."""
    print("🚀 Starting multilingual site generation...")
    
    # Get all locale directories
    locale_path = 'locale'
    if not os.path.exists(locale_path):
        print(f"❌ Locale directory '{locale_path}' not found!")
        return
    
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
    
    print(f"Found {len(languages)} enabled languages with compiled translations")
    print(f"Languages: {', '.join(sorted(languages))}")
    
    # Always generate English first (even if not in locale dir)
    print("\n📝 Generating English (base) version first...")
    os.system('python main.py')
    
    # Generate English supplementary pages
    print("\n📝 Generating English supplementary pages...")
    os.system('python supplementary_site_generator.py')
    
    # Generate other languages
    for locale_code in sorted(languages):
        generate_language_version(locale_path, locale_code)
    
    # Generate supplementary pages for all languages
    print("\n🔧 Generating supplementary pages for all languages...")
    os.system('python generate_supplementary_multilingual.py')
    
    print("\n✅ All language versions generated successfully!")
    print("\nLanguage URLs:")
    print("  English: /")
    for locale_code in sorted(languages):
        if locale_code == 'ja':
            print(f"  {locale_code}: /jp/")
        else:
            print(f"  {locale_code}: /{locale_code}/")

if __name__ == "__main__":
    main()