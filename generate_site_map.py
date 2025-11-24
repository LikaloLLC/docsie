import os
import sys
from collections import OrderedDict
from pathlib import Path
from urllib.parse import urljoin

cwd = os.getcwd()


if __name__ == '__main__':
    site_path = sys.argv[1]
    flows = [val for sublist in [[os.path.join(os.path.relpath(dir_, cwd), file) for file in files]
                                 for dir_, _, files in os.walk(cwd)] for val in sublist]

    # Skip internal directories and build artifacts
    skip_flows = ['src', '.blog', '.git', '.idea', '__pycache__', 'venv', '.venv',
                  'node_modules', 'staticjinja', 'blogvi', 'utils', 'locale',
                  '.yaml_batch_status', '.yaml_translation_cache', 'backups', '.external']

    # Language directories to EXCLUDE (we only want English content)
    # These have 301 redirects but should NOT be in sitemap
    language_dirs = ['ar', 'da', 'de', 'es', 'fr', 'he', 'it', 'ja', 'jp', 'ko', 'nl', 'no', 'pt', 'ru', 'sv', 'zh',
                     'ja_JP', 'zh_CN', 'ko_KR', 'hu', 'pl', 'tr']  # Locale formats and blog languages

    # Generate sitemap for English pages only (root level)
    site_map = []
    for flow in flows:
        if 'index.html' in flow:
            flow_parts = Path(flow).parts
            # Skip if path contains any skip directory or language directory
            if not any(skip in flow_parts for skip in skip_flows + language_dirs):
                # Clean up the URL
                url = urljoin(site_path, flow).replace('index.html', '')
                # Ensure URL ends with / for directories
                if not url.endswith('/'):
                    url += '/'
                site_map.append(url)

    # Remove duplicates while preserving order
    site_map_dict = OrderedDict.fromkeys(site_map)
    
    # Ensure sitemap directory exists
    os.makedirs('sitemap', exist_ok=True)
    
    with open('sitemap/sitemap.txt', 'w') as f:
        for item in site_map_dict.keys():
            f.write("%s\n" % item)
