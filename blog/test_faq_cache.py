#!/usr/bin/env python3
"""Test FAQ cache for specific article."""

from pathlib import Path

# Check different cache locations
cache_locations = [
    Path('.faq_cache'),
    Path('./.faq_cache'),
    Path('../.faq_cache'),
]

for loc in cache_locations:
    if loc.exists():
        print(f"Found FAQ cache at: {loc}")
        # Look for the specific article
        automated_caches = list(loc.glob('*automated*'))
        print(f"Found {len(automated_caches)} cache files matching 'automated':")
        for f in automated_caches:
            print(f"  - {f.name}")
    else:
        print(f"No cache at: {loc}")

# Check working directory
print(f"\nCurrent working directory: {Path.cwd()}")

# List all directories starting with dot
dot_dirs = [d for d in Path('.').iterdir() if d.is_dir() and d.name.startswith('.')]
print(f"\nFound {len(dot_dirs)} dot directories:")
for d in sorted(dot_dirs):
    print(f"  - {d.name}")