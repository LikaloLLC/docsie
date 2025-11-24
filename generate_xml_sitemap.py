#!/usr/bin/env python3
"""
Generate XML sitemap for English-only content (post-November 2025 multilingual deprecation)
"""
import os
import sys
from collections import OrderedDict
from pathlib import Path
from urllib.parse import urljoin
from datetime import datetime
import subprocess

def get_tracked_files():
    """Get list of files tracked by git"""
    try:
        result = subprocess.run(['git', 'ls-files'],
                              capture_output=True,
                              text=True,
                              check=True)
        return set(result.stdout.strip().split('\n'))
    except subprocess.CalledProcessError:
        print("⚠️  Could not get git tracked files, including all files")
        return None

def write_xml_sitemap(urls, site_url):
    """Write XML sitemap with proper formatting (English-only)"""
    xml_lines = ['<?xml version="1.0" encoding="UTF-8"?>']
    xml_lines.append('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">')

    # Add URLs
    for url_data in sorted(urls, key=lambda x: x['url']):
        xml_lines.append('  <url>')
        xml_lines.append(f'    <loc>{url_data["url"]}</loc>')
        xml_lines.append(f'    <lastmod>{datetime.now().strftime("%Y-%m-%d")}</lastmod>')
        xml_lines.append('    <changefreq>weekly</changefreq>')
        xml_lines.append(f'    <priority>{url_data["priority"]}</priority>')
        xml_lines.append('  </url>')

    xml_lines.append('</urlset>')
    return '\n'.join(xml_lines)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python generate_xml_sitemap.py <site_url>")
        sys.exit(1)
        
    site_url = sys.argv[1].rstrip('/')
    cwd = os.getcwd()
    
    # Get git tracked files
    tracked_files = get_tracked_files()
    
    # Skip internal directories and build artifacts
    skip_flows = ['src', '.blog', '.git', '.idea', '__pycache__', 'venv', '.venv', 
                  'node_modules', 'staticjinja', 'blogvi', 'utils', 'locale', 
                  '.yaml_batch_status', '.yaml_translation_cache', 'backups',
                  'scss', 'assets', 'content', 'eml', 'ui', 'static', 'scripts',
                  'styles', 'modern-home']  # Removed pricing_v2 from skip list
    
    # Skip untranslated/old pages
    skip_pages = ['validation_page', '2020_websummit', 'collision_2020', 'collision_2021',
                  'codepen', 'carbon', 'affiliate-program', 'docsie_manager', 
                  'docsie_publishing', 'docsie_product', 'docsie_vocally',
                  'docsie-free-consultation', 'discovery_call', 'feedback_preview_demo',
                  'gather_feedback', 'incident', 'manager', 'markdown_editor', 'pilot',
                  'press', 'release_notes', 'publish_documentation', 'self-writing-documentation',
                  'see-it-in-action', 'software_documentation', 'collaboration_software',
                  'careers', 'cookies', 'investors', 'resources', 'terms', 'support',
                  'privacy', 'about', 'features', 'documentation', 'try_docsie']
    
    # Collect all URLs grouped by base path
    url_groups = {}
    excluded_count = 0
    
    # Walk through all directories
    for root, dirs, files in os.walk(cwd):
        # Skip hidden directories and specified directories
        dirs[:] = [d for d in dirs if not d.startswith('.') and d not in skip_flows]
        
        if 'index.html' in files:
            rel_path = os.path.relpath(root, cwd)
            
            # Skip root-level index.html
            if rel_path == '.':
                rel_path = ''
                
            # Check if this path contains any skip_pages
            path_parts = rel_path.split(os.sep) if rel_path else []
            if any(skip_page in path_parts for skip_page in skip_pages):
                excluded_count += 1
                continue
                
            # Check if index.html is tracked by git
            index_path = os.path.join(rel_path, 'index.html') if rel_path else 'index.html'
            if tracked_files and index_path not in tracked_files:
                excluded_count += 1
                continue
                
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
    if excluded_count > 0:
        print(f"ℹ️  Excluded {excluded_count} untracked files from sitemap")