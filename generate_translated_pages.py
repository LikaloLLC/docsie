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
import fnmatch
from pathlib import Path
from staticjinja import Site
from jinja2 import Environment, FileSystemLoader
import feedparser
import dateutil.parser
import arrow

# Import the custom site class from main.py
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

def load_gitignore_patterns():
    """Load patterns from .gitignore file"""
    patterns = []
    gitignore_path = Path('.gitignore')
    if gitignore_path.exists():
        with open(gitignore_path, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    patterns.append(line)
    return patterns

def is_ignored_by_gitignore(path, patterns):
    """Check if a path matches any gitignore pattern"""
    path_str = str(path)
    for pattern in patterns:
        # Handle directory patterns ending with /
        if pattern.endswith('/'):
            if path_str.startswith(pattern[:-1]):
                return True
        # Handle wildcard patterns
        if fnmatch.fnmatch(path_str, pattern):
            return True
        # Check if any parent directory matches
        for parent in Path(path).parents:
            if fnmatch.fnmatch(str(parent), pattern):
                return True
    return False

class TranslationSite(CustomSite):
    """Custom site class that filters out legacy pages from translation."""
    
    def is_template(self, filename):
        """Check if a file should be treated as a template."""
        # First check parent class (binary file check)
        if not super().is_template(filename):
            return False
        
        # Get the base name without extension
        base_name = os.path.splitext(os.path.basename(filename))[0]
        
        # Also check directory name
        dir_name = os.path.basename(os.path.dirname(filename))
        
        # Skip if it's a legacy page
        if base_name in LEGACY_PAGES_TO_SKIP or dir_name in LEGACY_PAGES_TO_SKIP:
            return False
            
        return True

def setup_translations(lang_code):
    """Set up gettext translations for a specific language."""
    locale_dir = Path(__file__).parent / 'locale'
    
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
    elif lang_code == 'ja':
        # Japanese uses 'jp' directory
        outpath = 'jp'
        os.makedirs(outpath, exist_ok=True)
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
    # For non-English languages, filter out legacy pages
    if lang_code != 'en':
        # Create custom site that filters legacy pages
        class FilteredTranslationSite(CustomSite):
            def is_template(self, filename):
                """Check if a file should be treated as a template."""
                # First check parent class (binary file check)
                if not super().is_template(filename):
                    return False
                
                # Check if any part of the path contains a legacy page
                path_parts = filename.split(os.sep)
                for part in path_parts:
                    part_without_ext = os.path.splitext(part)[0]
                    if part_without_ext in LEGACY_PAGES_TO_SKIP:
                        print(f"  Skipping legacy page: {filename}")
                        return False
                
                return True
        
        site = FilteredTranslationSite.make_site(
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
    else:
        # For English, use the normal site without filtering
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
    site._env.install_gettext_translations(translation)
    
    # Render the site
    site.render()
    
    # Copy static assets (they don't need translation)
    if lang_code != 'en':
        gitignore_patterns = load_gitignore_patterns()
        static_dirs = ['assets', 'styles', 'js', 'images', 'fonts']
        
        for static_dir in static_dirs:
            src_dir = Path(static_dir)
            if src_dir.exists():
                # Check if this directory should be ignored for this language
                lang_specific_path = f"{outpath}/{static_dir}"
                if is_ignored_by_gitignore(lang_specific_path, gitignore_patterns):
                    print(f"  Skipping {static_dir} (matched .gitignore pattern)")
                    continue
                
                dest_dir = Path(outpath) / static_dir
                if dest_dir.exists():
                    shutil.rmtree(dest_dir)
                shutil.copytree(src_dir, dest_dir)
                print(f"  Copied {static_dir} → {dest_dir}")
    
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