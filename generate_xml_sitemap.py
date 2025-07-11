#!/usr/bin/env python3
"""
Generate XML sitemap with hreflang annotations for multilingual SEO
"""
import os
import sys
from collections import OrderedDict
from pathlib import Path
from urllib.parse import urljoin
from datetime import datetime

# Language mapping (same as in hreflang template)
LANGUAGE_CODES = ['de', 'es', 'fr', 'jp', 'ko', 'pt', 'ar', 'bn', 'cs', 'da', 
                  'el', 'fi', 'he', 'hi', 'hu', 'id', 'is', 'it', 'ja', 'nl', 
                  'no', 'pl', 'ro', 'ru', 'sv', 'tr', 'uk', 'zh']

# Map directory to language code
DIR_TO_LANG = {
    'jp': 'ja',  # Japanese uses jp directory but ja language code
}

def get_language_from_path(path):
    """Extract language code from path"""
    parts = Path(path).parts
    if parts and parts[0] in LANGUAGE_CODES:
        # Map directory to language code if needed
        return DIR_TO_LANG.get(parts[0], parts[0])
    return 'en'  # Default to English

def get_base_path(path):
    """Get base path without language prefix"""
    parts = list(Path(path).parts)
    if parts and parts[0] in LANGUAGE_CODES:
        return '/'.join(parts[1:])
    return path

def write_xml_sitemap(url_groups, site_url):
    """Write XML sitemap with proper formatting"""
    xml_lines = ['<?xml version="1.0" encoding="UTF-8"?>']
    xml_lines.append('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">')
    
    # Add URLs with hreflang annotations
    for base_path, lang_urls in sorted(url_groups.items()):
        # Determine priority based on path depth
        if not base_path:
            priority = "1.0"
        elif base_path.count('/') == 0:
            priority = "0.8"
        else:
            priority = "0.6"
            
        # Add entry for each language version
        for lang, url in lang_urls.items():
            xml_lines.append('  <url>')
            xml_lines.append(f'    <loc>{url}</loc>')
            xml_lines.append(f'    <lastmod>{datetime.now().strftime("%Y-%m-%d")}</lastmod>')
            xml_lines.append('    <changefreq>weekly</changefreq>')
            xml_lines.append(f'    <priority>{priority}</priority>')
            
            # Add hreflang links for all language versions
            for alt_lang, alt_url in lang_urls.items():
                xml_lines.append(f'    <xhtml:link rel="alternate" hreflang="{alt_lang}" href="{alt_url}"/>')
            
            # Add x-default for English
            if 'en' in lang_urls:
                xml_lines.append(f'    <xhtml:link rel="alternate" hreflang="x-default" href="{lang_urls["en"]}"/>')
                
            xml_lines.append('  </url>')
    
    xml_lines.append('</urlset>')
    return '\n'.join(xml_lines)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python generate_xml_sitemap.py <site_url>")
        sys.exit(1)
        
    site_url = sys.argv[1].rstrip('/')
    cwd = os.getcwd()
    
    # Skip internal directories and build artifacts
    skip_flows = ['src', '.blog', '.git', '.idea', '__pycache__', 'venv', '.venv', 
                  'node_modules', 'staticjinja', 'blogvi', 'utils', 'locale', 
                  '.yaml_batch_status', '.yaml_translation_cache', 'backups',
                  'scss', 'assets', 'content', 'eml', 'ui']
    
    # Collect all URLs grouped by base path
    url_groups = {}
    
    # Walk through all directories
    for root, dirs, files in os.walk(cwd):
        # Skip hidden directories and specified directories
        dirs[:] = [d for d in dirs if not d.startswith('.') and d not in skip_flows]
        
        if 'index.html' in files:
            rel_path = os.path.relpath(root, cwd)
            
            # Skip root-level index.html
            if rel_path == '.':
                rel_path = ''
                
            # Get base path and language
            base_path = get_base_path(rel_path)
            lang = get_language_from_path(rel_path)
            
            # Create URL
            if rel_path:
                url = f"{site_url}/{rel_path}/"
            else:
                url = f"{site_url}/"
            
            # Group by base path
            if base_path not in url_groups:
                url_groups[base_path] = {}
            url_groups[base_path][lang] = url
    
    # Write XML sitemap
    xml_content = write_xml_sitemap(url_groups, site_url)
    
    with open('sitemap.xml', 'w', encoding='utf-8') as f:
        f.write(xml_content)
    
    # Also keep the text version for compatibility
    os.makedirs('sitemap', exist_ok=True)
    with open('sitemap/sitemap.txt', 'w') as f:
        for base_path, lang_urls in sorted(url_groups.items()):
            for lang, url in sorted(lang_urls.items()):
                f.write(f"{url}\n")
    
    print(f"✅ Generated XML sitemap with {len(url_groups)} unique pages")
    print(f"✅ Total URLs (all languages): {sum(len(urls) for urls in url_groups.values())}")