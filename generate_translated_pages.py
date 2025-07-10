#!/usr/bin/env python3
"""
Generate translated versions of the website for all enabled languages.
This script creates language-specific directories and renders all templates
with the appropriate translations loaded.
"""

import os
import sys
import shutil
import gettext
import yaml
from pathlib import Path
from staticjinja import Site
from jinja2 import Environment, FileSystemLoader
import feedparser
import dateutil.parser
import arrow

# Import the custom site class from main.py
from main import CustomSite, render_template_file, is_binary_file

def load_translation_config():
    """Load translation configuration from YAML file."""
    config_path = Path(__file__).parent / 'translation_config.yaml'
    with open(config_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

def get_enabled_languages(config):
    """Get list of enabled languages from config."""
    languages = []
    for lang_code, lang_config in config['languages'].items():
        if lang_config.get('enabled', False):
            languages.append({
                'code': lang_code,
                'name': lang_config['name'],
                'native_name': lang_config.get('native_name', lang_config['name'])
            })
    return languages

def setup_translations(lang_code):
    """Set up gettext translations for a specific language."""
    locale_dir = Path(__file__).parent / 'locale'
    
    # Handle special cases like ja_JP
    if lang_code == 'ja':
        # Check if ja_JP exists
        ja_jp_path = locale_dir / 'ja_JP' / 'LC_MESSAGES' / 'messages.mo'
        if ja_jp_path.exists():
            lang_code = 'ja_JP'
    
    try:
        # Load the translation
        translation = gettext.translation(
            'messages',
            localedir=str(locale_dir),
            languages=[lang_code]
        )
        translation.install()
        return translation
    except FileNotFoundError:
        print(f"Warning: Translation file not found for {lang_code}")
        # Return a null translation that just returns the original text
        return gettext.NullTranslations()

def generate_language_site(lang_code, lang_name):
    """Generate the site for a specific language."""
    print(f"\n🌐 Generating {lang_name} ({lang_code}) version...")
    
    # Set up translations
    translation = setup_translations(lang_code)
    
    # Create output directory
    if lang_code == 'en':
        # English is the default, no subdirectory
        outpath = '.'
    else:
        outpath = lang_code
        os.makedirs(outpath, exist_ok=True)
    
    # Get blog feed data (same for all languages)
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
    
    # Create custom render function that includes translation
    def render_with_translation(site, template, **kwargs):
        """Render template with translation context."""
        kwargs['lang'] = lang_code
        kwargs['lang_name'] = lang_name
        kwargs['_'] = translation.gettext  # Add translation function
        kwargs['gettext'] = translation.gettext
        kwargs['ngettext'] = translation.ngettext
        
        # Call the original render function
        return render_template_file(site, template, **kwargs)
    
    # Create site with translation support
    site = CustomSite.make_site(
        searchpath='src/',
        outpath=outpath,
        env_globals={
            "feed": feed[-12:][::-1],
            "videos": feed_videos,
            "lang": lang_code,
            "lang_name": lang_name,
            "_": translation.gettext,
            "gettext": translation.gettext,
            "ngettext": translation.ngettext
        },
        extensions=['jinja2.ext.i18n', 'jinja_markdown.MarkdownExtension'],
        rules=[
            (".*", render_with_translation)
        ]
    )
    
    # Install translation in Jinja2 environment
    site.env.install_gettext_translations(translation)
    
    # Render the site
    site.render()
    
    # Copy static assets (they don't need translation)
    if lang_code != 'en':
        static_dirs = ['assets', 'styles', 'js', 'images', 'fonts']
        for static_dir in static_dirs:
            src_dir = Path(static_dir)
            if src_dir.exists():
                dest_dir = Path(outpath) / static_dir
                if dest_dir.exists():
                    shutil.rmtree(dest_dir)
                shutil.copytree(src_dir, dest_dir)
    
    print(f"✅ Generated {lang_name} version in '{outpath}' directory")

def main():
    """Main function to generate all translated versions."""
    print("🚀 Starting multilingual site generation...")
    
    # Load configuration
    config = load_translation_config()
    languages = get_enabled_languages(config)
    
    print(f"Found {len(languages)} enabled languages")
    
    # Always generate English first (it's the base)
    generate_language_site('en', 'English')
    
    # Generate other languages
    for lang in languages:
        if lang['code'] != 'en':
            generate_language_site(lang['code'], lang['native_name'])
    
    print("\n✅ All language versions generated successfully!")
    print("\nNext steps:")
    print("1. Test the generated sites locally")
    print("2. Update your web server configuration to serve language-specific directories")
    print("3. Ensure the language picker links to the correct URLs")

if __name__ == "__main__":
    main()