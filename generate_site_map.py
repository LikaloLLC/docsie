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

    skip_flows = ['src', '.blog', 'jp', 'ko', 'de', 'es', 'de', 'fr', 'pt']

    site_map = [
        urljoin(site_path, flow).replace('index.html', '') for flow in flows
        if 'index.html' in flow and not any(skip in Path(flow).parts for skip in skip_flows)
    ]
    skip_flows_locale = ['src', '.blog', 'jp', 'ko', 'de', 'es', 'de', 'fr', 'pt', 'blog', 'try_docsie']


    locale_root = Path('locale')
    locale_dirs = [dir_ for dir_ in locale_root.iterdir() if dir_.is_dir()]
    for loc in locale_dirs:
        locale = loc.name if loc.name != 'ja_JP' else 'jp'
        site_map.extend([
            urljoin(urljoin(site_path, locale) + '/', flow).replace('index.html', '') for flow in flows
            if 'index.html' in flow and not any(skip in Path(flow).parts for skip in skip_flows_locale)
        ])

    # Hacky deduplicating of the urls
    site_map_dict = d = OrderedDict.fromkeys(site_map)
    with open('sitemap/sitemap.txt', 'w') as f:
        for item in site_map_dict.keys():
            f.write("%s\n" % item)
