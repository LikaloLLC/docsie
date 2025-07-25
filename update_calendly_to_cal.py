#!/usr/bin/env python3
"""
Script to replace all Calendly references with Cal.com in generated HTML files.
This handles supplementary pages and any other generated content.
"""

import os
import re
from pathlib import Path

def replace_calendly_in_file(filepath):
    """Replace Calendly references with Cal.com in a single file."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Track if we made any changes
        original_content = content
        
        # Replace Calendly script URL
        content = content.replace(
            'https://assets.calendly.com/assets/external/widget.css',
            ''  # Remove CSS as Cal.com includes it in their script
        )
        content = content.replace(
            'https://assets.calendly.com/assets/external/widget.js',
            'https://app.cal.com/embed/embed.js'
        )
        
        # Replace Calendly DNS prefetch
        content = content.replace(
            'https://assets.calendly.com',
            'https://app.cal.com'
        )
        
        # Replace Calendly onclick handlers
        # Pattern: onclick="Calendly.initPopupWidget({url: 'https://calendly.com/docsie-io/demo-call'});return false;"
        calendly_onclick_pattern = r'onclick="Calendly\.initPopupWidget\({url:\s*[\'"]https://calendly\.com/docsie-io/demo-call[\'"]\}\);return false;"'
        cal_replacement = 'data-cal-link="docsie/product-discovery" data-cal-namespace="product-discovery" data-cal-config=\'{"layout":"month_view"}\''
        content = re.sub(calendly_onclick_pattern, cal_replacement, content)
        
        # Also handle variation without return false
        calendly_onclick_pattern2 = r'onclick="Calendly\.initPopupWidget\({url:\s*[\'"]https://calendly\.com/docsie-io/demo-call[\'"]\}\)"'
        content = re.sub(calendly_onclick_pattern2, cal_replacement, content)
        
        # Handle AI pilot page with custom calendly URL
        calendly_pilot_pattern = r'onclick="Calendly\.initPopupWidget\({url:\s*[\'"]https://calendly\.com/docsie-io/docsie-io-ai-pilot/[\'"]\}\);?return false;"'
        cal_pilot_replacement = 'data-cal-link="docsie/docsie-io-ai-pilot" data-cal-namespace="product-discovery" data-cal-config=\'{"layout":"month_view"}\''
        content = re.sub(calendly_pilot_pattern, cal_pilot_replacement, content)
        
        # Handle any other calendly URLs
        calendly_generic_pattern = r'onclick="Calendly\.initPopupWidget\({url:\s*[\'"]https://calendly\.com/([^\'"]*)[\'"]\}\);?(?:return false;)?"'
        def replace_generic_calendly(match):
            calendly_path = match.group(1)
            # Extract the last part of the path as the cal.com link
            cal_link = calendly_path.split('/')[-1] if '/' in calendly_path else calendly_path
            return f'data-cal-link="{cal_link}" data-cal-namespace="product-discovery" data-cal-config=\'{{\"layout\":\"month_view\"}}\''
        content = re.sub(calendly_generic_pattern, replace_generic_calendly, content)
        
        # If we made changes, write the file
        if content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        return False
    except Exception as e:
        print(f"Error processing {filepath}: {e}")
        return False

def update_all_html_files(root_dir):
    """Walk through all HTML files and update Calendly references."""
    updated_files = []
    skipped_dirs = {'src', '.git', 'node_modules', '.external', '__pycache__'}
    
    for root, dirs, files in os.walk(root_dir):
        # Skip certain directories
        dirs[:] = [d for d in dirs if d not in skipped_dirs]
        
        for file in files:
            if file.endswith('.html'):
                filepath = os.path.join(root, file)
                if replace_calendly_in_file(filepath):
                    updated_files.append(filepath)
    
    return updated_files

def main():
    """Main function to run the update."""
    print("Starting Calendly to Cal.com migration...")
    
    # Get the root directory (current directory)
    root_dir = os.getcwd()
    
    # Update all HTML files
    updated_files = update_all_html_files(root_dir)
    
    print(f"\nUpdated {len(updated_files)} files:")
    for file in sorted(updated_files)[:20]:  # Show first 20 files
        print(f"  - {file}")
    
    if len(updated_files) > 20:
        print(f"  ... and {len(updated_files) - 20} more files")
    
    print("\nMigration complete!")
    print("\nNote: You may need to rebuild the site to ensure all templates are properly updated.")

if __name__ == "__main__":
    main()