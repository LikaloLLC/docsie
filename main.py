from staticjinja import Site
from jinja2 import Environment, FileSystemLoader
import gettext
import sys
from os import listdir 
from os.path import isfile, join
import os 
cwd = os.getcwd() 
import feedparser
from os import listdir 
from os.path import isfile, join 
import dateutil.parser
import arrow
import yaml

def is_binary_file(filepath):
    """
    Determine if a file is a binary file that should be excluded from template processing.
    """
    excluded_extensions = {
        '.png', '.jpg', '.jpeg', '.gif', '.bmp', '.ico', '.svg',
        '.pdf', '.doc', '.docx', '.ppt', '.pptx',
        '.mp4', '.webm', '.ogg', '.mp3', '.wav',
        '.zip', '.tar', '.gz', '.rar',
        '.backup', '.bak', '.tmp', '.swp'  # Add backup files
    }
    _, ext = os.path.splitext(filepath.lower())
    return ext in excluded_extensions

class CustomSite(Site):
    """Custom Site class that filters out binary files from template processing."""
    
    def is_template(self, filename):
        """Check if a file should be treated as a template."""
        if is_binary_file(filename):
            return False
        return super().is_template(filename)

def render_template_file(site, template, **kwargs):
    """
    Custom render function that handles template rendering.
    Automatically detects V2 pages and provides appropriate context.
    Special handling for V2 homepage.
    """
    # Skip rendering index.html if index_v2.html exists (V2 takes precedence)
    if template.name == 'index.html':
        index_v2_path = os.path.join(site.searchpath, 'index_v2.html')
        if os.path.exists(index_v2_path):
            print(f"Skipping {template.name} because index_v2.html exists")
            return True
    
    # Skip rendering pricing/index.html if pricing_v2/index.html exists (V2 takes precedence)
    if template.name == 'pricing/index.html':
        pricing_v2_path = os.path.join(site.searchpath, 'pricing_v2/index.html')
        if os.path.exists(pricing_v2_path):
            print(f"Skipping {template.name} because pricing_v2/index.html exists")
            return True
    
    # Special handling for index_v2.html - render it as index.html
    if template.name == 'index_v2.html':
        outpath = os.path.join(site.outpath, 'index.html')
        print(f"Rendering {template.name} as index.html (V2 homepage)")
    # Special handling for pricing_v2/index.html - render it as pricing/index.html
    elif template.name == 'pricing_v2/index.html':
        outpath = os.path.join(site.outpath, 'pricing/index.html')
        print(f"Rendering {template.name} as pricing/index.html (V2 pricing)")
    else:
        outpath = os.path.join(site.outpath, template.name)
    
    outdir = os.path.dirname(outpath)
    
    if outdir:
        os.makedirs(outdir, exist_ok=True)
    
    # Check if this is a V2 page by examining the template name or reading the file
    is_v2_page = False
    try:
        # Check template name first
        if 'index_v2.html' in template.name or 'v2_demo.html' in template.name or 'pricing_v2' in template.name:
            is_v2_page = True
        else:
            # Read the template file to check for _base_v2.html
            template_path = os.path.join(site.searchpath, template.name)
            if os.path.exists(template_path):
                with open(template_path, 'r', encoding='utf-8') as f:
                    template_content = f.read()
                    if '_base_v2.html' in template_content:
                        is_v2_page = True
    except Exception:
        # If there's any error, default to V1
        is_v2_page = False
    
    # Add V2-specific context if needed
    if is_v2_page:
        kwargs['is_v2'] = True
        kwargs['use_v2_styles'] = True
        
    # Render the template
    rendered = template.render(**kwargs)
    
    # Write the rendered template to file
    with open(outpath, 'w', encoding='utf-8') as f:
        f.write(rendered)
    return True

if __name__ == "__main__":
    # Get the directory where the script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    ###Grabbing blogposts and converting them to
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

    site = CustomSite.make_site(
        searchpath='src/', 
        outpath=script_dir,
        env_globals={"feed":feed[-12:][::-1],"videos":feed_videos},
        extensions=['jinja2.ext.i18n','jinja_markdown.MarkdownExtension'],
        rules=[
            (".*", render_template_file)
        ]
    )
    site.render()
