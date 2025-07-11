#!/usr/bin/env python3
"""
Generate complete translated versions of the site including supplementary pages.
This combines main site generation with supplementary page generation for each language.
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
import shutil

# Import the custom classes and supplementary functions
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from main import CustomSite, render_template_file, is_binary_file
from supplementary_site_generator import (
    load_component_data, load_all_supplementary_pages, 
    render_component_with_version, copy_styles
)

def generate_supplementary_pages_for_locale(site_env, locale_code, output_base, locale_name):
    """Generate supplementary pages for a specific locale using the site's Jinja environment"""
    print(f"  📄 Generating supplementary pages for {locale_code}...")
    
    # Use V2 template
    template = site_env.get_template('.templates/supplementary_page_v2.html')
    
    # Load all page data
    pages_data = load_all_supplementary_pages()
    
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
    
    site_env.globals['get_page_by_url'] = get_page_by_url
    
    # Load component configurations
    components_data = load_component_data()
    
    # Create base output directory
    base_dir = os.path.join(output_base, 'solutions')
    os.makedirs(base_dir, exist_ok=True)
    
    # Generate each page
    generated_count = 0
    for page in pages_data:
        try:
            # Force UI version
            page['ui_version'] = 'v2'
            
            # Create context
            context = {
                'page': page,
                'components': components_data,
                'styles_path': '/styles',
                'get_page_by_url': get_page_by_url,
                'locale': locale_name
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
            print(f"    ⚠️  Error processing page {page.get('id', 'unknown')}: {str(e)}")
    
    print(f"  ✅ Generated {generated_count} supplementary pages")

def copy_styles_once():
    """Copy component styles to output directory (only needs to be done once)"""
    print("\n📁 Copying component styles...")
    
    # Create styles directories
    os.makedirs('styles/components', exist_ok=True)
    os.makedirs('solutions/styles/components', exist_ok=True)
    
    # Copy component styles
    components_dir = 'src/.templates/components'
    if os.path.exists(components_dir):
        for component_name in os.listdir(components_dir):
            component_path = os.path.join(components_dir, component_name)
            if os.path.isdir(component_path):
                style_file = os.path.join(component_path, 'style.css')
                if os.path.exists(style_file):
                    # Copy to both locations
                    shutil.copy2(style_file, f'styles/components/{component_name}.css')
                    shutil.copy2(style_file, f'solutions/styles/components/{component_name}.css')
    
    # Copy main supplementary page style
    if os.path.exists('src/.templates/supplementary_page.css'):
        shutil.copy2('src/.templates/supplementary_page.css', 'styles/supplementary_page.css')
        shutil.copy2('src/.templates/supplementary_page.css', 'solutions/styles/supplementary_page.css')

def generate_language_version(locale_dir, locale_code):
    """Generate complete site for a specific language including supplementary pages"""
    print(f"\n🌐 Generating {locale_code} version...")
    
    # Special handling for locale codes
    if locale_code == 'ja':
        loc_name = '/jp'
        output_path = 'jp'
    else:
        loc_name = '/' + locale_code
        output_path = locale_code
    
    # Setup gettext translations
    try:
        translation = gettext.translation(
            'messages',
            localedir=locale_dir,
            languages=[locale_code]
        )
        _ = translation.gettext
    except FileNotFoundError:
        print(f"  ⚠️  Translation not found for {locale_code}, using English")
        translation = None
        _ = lambda x: x
    
    # Get blog feeds
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
    os.makedirs(output_path, exist_ok=True)
    
    # Create site with locale
    site = CustomSite.make_site(
        searchpath='./src', 
        outpath=output_path,
        env_globals={
            "locale": loc_name,
            "feed": feed[-12:][::-1],
            "videos": feed_videos,
            "_": _,
            "gettext": _,
            "render_component": lambda name, config, **kwargs: render_component_with_version(
                site._env, name, config, 'v2', **kwargs
            )
        },
        locale=locale_code, 
        extensions=['jinja2.ext.i18n', 'jinja_markdown.MarkdownExtension'],
        rules=[
            (".*", render_template_file)
        ]
    )
    
    # Install translations in Jinja environment
    if translation:
        site._env.install_gettext_translations(translation)
    
    # Import language helpers into the environment
    site._env.globals.update({
        'lang': {
            'abs_lang_url': lambda path: f"{loc_name}/{path}".replace('//', '/')
        }
    })
    
    # Render the main site
    print(f"  📝 Generating main pages...")
    site.render(use_reloader=False)
    
    # Generate supplementary pages using the same environment
    generate_supplementary_pages_for_locale(site._env, locale_code, output_path, loc_name)
    
    print(f"✅ Completed {locale_code} generation")

def main():
    """Generate all language versions with supplementary pages"""
    print("🚀 Starting complete multilingual site generation...")
    
    # Get all locale directories
    locale_path = 'locale'
    if not os.path.exists(locale_path):
        print(f"❌ Locale directory '{locale_path}' not found!")
        return
    
    # Copy styles once at the beginning
    copy_styles_once()
    
    # Get all language directories
    languages = []
    for item in os.listdir(locale_path):
        item_path = os.path.join(locale_path, item)
        if os.path.isdir(item_path) and item != '.cache':
            # Check if it has compiled messages
            mo_file = os.path.join(item_path, 'LC_MESSAGES', 'messages.mo')
            if os.path.exists(mo_file):
                languages.append(item)
    
    print(f"\nFound {len(languages)} languages with compiled translations")
    print(f"Languages: {', '.join(sorted(languages))}")
    
    # Always generate English first
    print("\n📝 Generating English (base) version...")
    print("  📝 Generating main pages...")
    os.system('python main.py')
    print("  📄 Generating supplementary pages...")
    os.system('python supplementary_site_generator.py')
    print("✅ Completed English generation")
    
    # Generate other languages
    for locale_code in sorted(languages):
        generate_language_version(locale_path, locale_code)
    
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