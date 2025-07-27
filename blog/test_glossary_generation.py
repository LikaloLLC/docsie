#!/usr/bin/env python3
"""Test script to debug glossary generation."""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../.external/BlogVi/src'))

from pathlib import Path
from blog_vi._config import Settings
from blog_vi.core.glossary import GlossaryAggregator
from blog_vi.core.article import Article
import json

# Load settings
settings = Settings.from_file(Path('./settings.yaml'))
print(f"Settings loaded: {settings.blog_name}")

# Check glossary settings
if hasattr(settings, 'glossary_generation'):
    print(f"Glossary generation enabled: {settings.glossary_generation.get('enabled', False)}")
else:
    print("No glossary_generation settings found")

# Mock articles with glossary terms
class MockArticle:
    def __init__(self, slug, title):
        self.slug = slug
        self.title = title
        self.glossary_terms = []

# Load actual glossary terms from cache
cache_dir = Path('.glossary_cache')
articles = []

for cache_file in list(cache_dir.glob('*.json'))[:10]:  # Test with first 10
    with open(cache_file, 'r') as f:
        cache_data = json.load(f)
    
    article = MockArticle(
        slug=cache_file.stem,
        title=f"Article: {cache_file.stem}"
    )
    
    # Convert cached terms to objects
    from blog_vi.core.glossary.extractor import GlossaryTerm
    for term_data in cache_data.get('terms', []):
        term = GlossaryTerm(**term_data)
        article.glossary_terms.append(term)
    
    articles.append(article)
    print(f"Loaded {len(article.glossary_terms)} terms for {article.slug}")

# Try to aggregate
print("\nAttempting glossary aggregation...")
aggregator = GlossaryAggregator(settings)
glossary_index = aggregator.aggregate_terms(articles)

print(f"\nAggregated {len(glossary_index)} unique terms")
if glossary_index:
    # Try to generate page
    print("Generating glossary page...")
    aggregator.generate_glossary_page(glossary_index)
    print("Done!")