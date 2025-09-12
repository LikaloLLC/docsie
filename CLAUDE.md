# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 🚨 CRITICAL INCIDENT - August 22, 2025

### The Problem
On August 22, 2025, we discovered that www.docsie.io was completely deindexed by Google, showing "No information is available for this page" in search results. This led to a complete loss of organic traffic and demo bookings.

### Root Cause
The `<title>` and `<meta name="description">` tags were appearing on line 321+ of the HTML instead of within the first 50 lines. This was caused by large include files (`_hreflang.html` and `_structured_data.html`) being placed BEFORE the critical SEO tags in the base templates.

### Impact
- **All pages using `_base.html`, `_base_v2.html`, `_base_v3.html` were affected**
- Main homepage (all versions) - completely deindexed
- All 15+ translated homepages - completely deindexed  
- Zero organic traffic and demo bookings
- Google showing non-www domain (https://docsie.io) instead of canonical www

### The Fix (Implemented August 22, 2025)
1. Reordered base templates to place title/description on lines 13-14
2. Moved includes (_hreflang.html, _structured_data.html) AFTER critical SEO tags
3. Created `site_config.yaml` to control v2/v3 version selection
4. Fixed malformed `name=description` (missing quotes) in all base templates

### Files Modified
- `src/_base.html` - Title/description moved to lines 13-14
- `src/_base_v2.html` - Title/description moved to lines 13-14  
- `src/_base_v3.html` - Title/description moved to lines 13-14
- `site_config.yaml` - New config file for version control
- `main.py` - Updated to use site_config.yaml

### Recovery Actions Required
1. Deploy immediately
2. Request re-indexing in Google Search Console
3. Submit to Bing and Yandex webmaster tools
4. Monitor recovery over 7-14 days

### Prevention
- ALWAYS ensure title and meta description appear within first 50 lines of HTML
- Test HTML output after template changes
- Monitor Google Search Console for indexing issues

## 🚨 CRITICAL DISCOVERY - September 6, 2025: Multilingual Cannibalization

### The Problem
BlogVi's translated articles are cannibalizing English content in search results. Spanish, French, and other language versions are ranking for English search queries, causing catastrophic CTR for English content.

### Root Causes
1. **Missing canonical tags** - Translations don't have canonical tags pointing to English originals
2. **No hreflang implementation** - Google cannot understand language relationships between articles
3. **Wrong language attributes** - All translations have `<html lang="en">` instead of proper language codes
4. **Independent indexing** - Each translation treated as separate, competing content

### Current Impact
- **English blog performance**: Only 61 clicks from 278 articles (0.154% CTR)
- **Foreign language dominance**: 4-5x better CTR, but stealing English queries
- **Traffic stagnation**: ~1K visits/week (30-50% below pre-incident baseline)
- **Example**: Spanish "Las 10 herramientas" ranking for English query "top 10 tools used by product managers"

### Required Fixes
1. **Add canonical tags** to all translations:
   ```html
   <link rel="canonical" href="https://www.docsie.io/blog/articles/[english-slug]/">
   ```
2. **Implement hreflang tags** on all articles:
   ```html
   <link rel="alternate" hreflang="en" href="https://www.docsie.io/blog/articles/[slug]/">
   <link rel="alternate" hreflang="es" href="https://www.docsie.io/blog/es/articles/[slug]/">
   <link rel="alternate" hreflang="fr" href="https://www.docsie.io/blog/fr/articles/[slug]/">
   ```
3. **Fix language attributes**: `<html lang="es">`, `<html lang="fr">`, etc.
4. **Consider temporary no-index** for low-quality translations

### Expected Recovery
- **Immediate**: Stop cannibalization, English content reclaims its queries
- **2-4 weeks**: Google recrawls and understands language structure
- **Long-term**: Each language reinforces domain authority instead of competing

## Project Overview

This is the static website repository for Docsie.io, a documentation platform. The site is built using Python with staticjinja (a static site generator based on Jinja2 templates) and hosted on GitHub Pages.

## Architecture

- **Static Site Generator**: Custom staticjinja implementation with Jinja2 templates
- **Template Engine**: Jinja2 with markdown support and internationalization
- **Content Sources**: Templates in `src/` directory, blog content fetched from RSS feeds
- **Output**: Static HTML files generated to root directory
- **Internationalization**: Multi-language support with Babel (de, es, fr, jp, ko, pt languages)
- **Blog System**: Uses BlogVI for blog generation with YAML configuration
- **Configuration**: `site_config.yaml` controls build behavior and version selection

## Key Directories

- `src/`: Source templates and content
- `blogvi/`: Blog configuration and templates
- `staticjinja/`: Custom staticjinja implementation
- `assets/`: Static assets (images, CSS, JS)
- `locale/`: Translation files
- `scss/`: SCSS source files for styling

## Site Configuration (site_config.yaml)

The site build process is controlled by `site_config.yaml`, which was created during the August 2025 incident to provide better control over site versions:

```yaml
# Version Control
homepage_version: "v2"  # Options: "v1", "v2", "v3"
pricing_version: "v2"    # Options: "v1", "v2"

# Canonical URL Configuration
canonical_domain: "https://www.docsie.io"  # ALWAYS use www for SEO

# Build Settings
verbose_build: true
enable_v3_preview: false  # Set to true to test v3 in development

# Feature Flags
enable_multilingual: true
enable_blog: true
```

**Important Notes:**
- The configuration determines which template versions are built
- `homepage_version: "v2"` maps `src/index_v2.html` → `index.html`
- `pricing_version: "v2"` maps `src/pricing_v2/index.html` → `pricing/index.html`
- v3 files are preserved for future deployment but not currently active
- This system prevents accidental deployment of work-in-progress versions

## Development Commands

### Setup
```bash
# Setup virtual environment and install dependencies
pip install -r requirements.txt
```

### Build and Development
```bash
# Build the site (generates static files)
python main.py

# Alternative build using staticjinja CLI
sh compile.sh

# Start development server
sh start.sh  # Runs on port 8081

# Watch for changes and auto-rebuild
sh auto_compile.sh
```

### Site Generation
```bash
# Generate sitemap
python generate_site_map.py https://www.docsie.io

# Generate supplementary solution pages
python supplementary_site_generator.py

# Generate missing images with DALL-E 3 (requires OPENAI_API_KEY)
python utils/image_generator.py                    # Standard quality
python utils/image_generator.py --quality hd       # HD quality (costs more)
python utils/image_generator.py --style natural    # Natural style
python utils/image_generator.py --override         # Regenerate all images
```

## Content Management

The site pulls content from multiple sources:
- Blog posts from RSS feed: `https://www.docsie.io/blog/rss.xml`
- YouTube videos from channel feed
- Static templates in `src/` directory
- Multilingual content in language-specific directories

## Template System

- Uses Jinja2 with custom extensions for markdown and i18n
- Templates include partials for common elements (`_header.html`, `_footer.html`, etc.)
- Supports dynamic content injection from external feeds
- Custom binary file filtering to exclude non-template files

## Deployment

The site is deployed to GitHub Pages. The build process generates static HTML files that are served directly.

## Babel Commands (Internationalization)

```bash
# Initialize new language
pybabel init -d locale -l <language_code> -i locale/messages.pot

# Compile translations
pybabel compile -d locale -l <language_code>
```

## BlogVi System (勝利 - "victory" in Japanese)

### Overview
BlogVi is a Python-based static blog generator that creates SEO-optimized blogs from CSV data sources. It's located in `.external/BlogVi/` and generates content into the main site's `/blog/` directory.

### Architecture
- **Static Site Generator**: Uses Jinja2 templates
- **Data Source**: CSV files (typically Google Sheets) with article metadata
- **Output**: Static HTML with client-side search (Fuse.js)
- **Translation**: Claude API with batch processing and caching
- **Design System**: V2 theme with Tailwind CSS and custom design tokens

### IMPORTANT: Template System
BlogVi has two sets of templates:
1. **Source templates**: Located in `.external/BlogVi/src/blog_vi/templates/` (DO NOT EDIT)
2. **Working templates**: Located in `/blog/templates/` (EDIT THESE)

The blog generation uses the **working templates** in `/blog/templates/`, NOT the source templates in the BlogVi package. Always edit the templates in the blog directory.

### Running BlogVi

#### From Blog Directory
```bash
cd /Users/philippetrounev/PycharmProjects/docsie-site/blog
python -m blog_vi .
# With force refresh (clears all caches)
python -m blog_vi . --force
```

#### Using Helper Scripts
```bash
# From BlogVi directory
sh regen_blog.sh          # Local testing
sh regen_blog_prod.sh     # Production generation

# With Python script
python /path/to/.external/BlogVi/run_blog_gen.py . [--force]
```

### Configuration (settings.yaml)

#### Single CSV Source (backward compatible)
```yaml
blog_post_location_url: "https://docs.google.com/spreadsheets/d/e/SHEET_ID/pub?output=csv"
```

#### Multiple CSV Sources
```yaml
blog_post_location_urls:
  - "https://docs.google.com/spreadsheets/d/e/SHEET_ID_1/pub?output=csv"
  - "https://docs.google.com/spreadsheets/d/e/SHEET_ID_2/pub?output=csv"
  - "https://raw.githubusercontent.com/user/repo/main/posts.csv"
```

### CSV Format Requirements
Required columns:
- **Title**: Article title
- **Timestamp**: MM/DD/YYYY HH:MM:SS format
- **Modified Timestamp**: (optional) Same format
- **Status**: 1 = published, other = draft
- **Slug**: URL-friendly identifier
- **Categories**: Comma-separated list
- **Author Name**, **Author email**, **Author Avatar Image URL**
- **About the Author**, **linked.in github urls**
- **Header Image**: Main article image
- **Excerpt/Short Summary**: Article description
- **Markdown**: Content (text or URL to .md file)
- **Is Legacy**: (optional) For redirect handling
- **Redirect Slug**: (optional) For URL redirects

### Key Features

#### SEO Implementation
- **Meta Tags**: Open Graph, Twitter Cards, canonical URLs
- **Structured Data**: JSON-LD for WebSite, BlogPosting, BreadcrumbList, Product
- **Breadcrumbs**: Automatic navigation generation
- **RSS Feed**: Auto-generated at `/blog/rss.xml`
- **Clean URLs**: All article URLs end with trailing slash
- **robots.txt directives**: max-image-preview, max-snippet settings

#### Article Processing
1. **Caching System**: Tracks changes using MD5 hashes of content
2. **Markdown Extensions**: Tables, TOC with permalinks, image handling
3. **Reading Time**: Automatic calculation based on word count
4. **Category Pages**: Auto-generated with AI descriptions (Claude API)
5. **Navigation**: Previous/Next article links

#### Design System (V2 Theme)
- **CSS Variables**: `--docsie-primary`, `--docsie-primary-dark`
- **Tailwind CSS**: Via CDN with custom utilities
- **Components**: Cards, breadcrumbs, TOC, category pills
- **Responsive**: Mobile-first design
- **Typography**: Custom styles in `typography.min.css`

### Template Structure
```
templates/
├── blog.html          # Main blog/category page
├── article.html       # Individual article page
├── card.html         # Article card component
├── lead_card.html    # Featured article card
├── header.html       # Site header
├── footer.html       # Site footer
├── favicon.html      # Favicon includes
└── assets/
    ├── css/
    │   ├── design-system.css
    │   └── typography.min.css
    └── js/
        ├── search.js      # Client-side search
        └── reading-time.min.js
```

### Output Structure
```
blog/
├── index.html              # Main blog page
├── rss.xml                 # RSS feed
├── data.json              # Search data
├── articles/
│   └── [slug]/
│       └── index.html     # Article page
├── [category-slug]/       # Category pages
│   └── index.html
└── [language]/            # Translated versions
    └── (same structure)
```

### Caching and Performance

#### Article Cache
- Location: `articles/[slug]/cache.json`
- Tracks: title, markdown, summary, categories, is_legacy
- Use `--force` flag to clear all caches

#### Category Descriptions
- Location: `.category_descriptions_cache/`
- AI-generated descriptions cached to reduce API calls

#### Translation Cache
- Location: `.translation_cache/`
- Stores translated content to avoid re-translation

### CLI Options
```bash
# Basic usage
blogvi [directory]

# Force refresh (clear all caches)
blogvi [directory] --force
blogvi [directory] -f

# Environment variables
BLOGVI_DIRECTORY=/path/to/blog blogvi
```

### Recent Improvements
1. **Trailing Slash Fix**: All article URLs now properly end with `/`
2. **Force Refresh**: Added `--force` flag to regenerate all content
3. **Multiple CSV Support**: Can now pull from multiple Google Sheets
4. **Breadcrumb Navigation**: Proper breadcrumb implementation
5. **V2 Design Integration**: Modern design system with Tailwind

### Known Limitations
- No sitemap.xml generation (see TODO.md)
- No robots.txt management
- Static aggregate ratings in Product schema
- No image optimization
- No AMP support
- No Core Web Vitals optimization features

### Development Notes
- Tracker system only monitors content changes, not template changes
- Use `--force` when updating templates to ensure all articles regenerate
- Category descriptions use Claude API and may take time on first generation
- Templates support both old and new theme versions for migration
- **Working templates are in `/blog/templates/`, NOT in `.external/BlogVi/src/blog_vi/templates/`**
- Previous/Next article links are generated in `landing.py` and require trailing slashes

### Recent Design Updates (Medium-style)
1. **Article Layout**: Narrow content area (max-w-3xl) for optimal readability
2. **TOC Behavior**: Shows initially, hides after 100px scroll for distraction-free reading
3. **Header Auto-hide**: Hides when scrolling down, reappears when scrolling up
4. **Floating CTA**: 
   - Appears after 30% scroll progress
   - Has minimize/expand functionality with close button
   - Minimizes to floating "Book Demo" button
5. **Typography**: 
   - Georgia serif font for article body (21px, line-height 2)
   - Sans-serif for headings with tighter letter spacing
   - Enhanced spacing for Medium-like reading experience

### Common Issues & Solutions
- **Missing trailing slashes**: Edit `landing.py` lines 186 & 191 to add trailing slashes
- **TOC not scrolling**: Remove height restrictions, use sticky container
- **CTA overlapping**: Use single sticky container for both TOC and CTA
- **Template changes not reflecting**: Always use `--force` flag when regenerating
- **Double slash URLs**: Use `.rstrip('/')` when concatenating paths to prevent `/blog//category/` issues
- **Logo not displaying**: Changed from inline SVG to `<img>` tag with CSS filter for coloring
- **Multiple head tags in articles**: Created `HTMLEscapeExtension` to escape HTML tags in markdown content outside of code blocks

### SEO Improvements Implemented
1. **Social Share Buttons**: Converted from `<a>` tags to `<button>` elements with JavaScript handlers
   - Prevents search engines from crawling social share links
   - No 302 redirects to external domains
   - Uses data attributes instead of href

2. **External Link Handling**: Created custom Markdown extension (`NoFollowExtension`)
   - Automatically adds `rel="nofollow noopener"` to all external links
   - Preserves internal links as dofollow
   - Respects manually set rel attributes for partner sites
   - Located in `.external/BlogVi/src/blog_vi/core/utils.py`

3. **URL Structure**: Fixed double slash issues that cause duplicate content
   - Category URLs: `/blog//category/` → `/blog/category/`
   - RSS feed: `/blog//rss.xml` → `/blog/rss.xml`
   - Use `.rstrip('/')` before concatenating paths

### Navigation & Header Updates
- **Dynamic Navigation**: Header now uses `settings.link_menu` instead of hardcoded links
- **Logo Path**: Using `/assets/docsie_logo_square_svg.svg` with CSS filter for brand color
- **Blog Link Removed**: Eliminated redundant "Blog" link from navigation (already shown in logo area)

### LinkedIn Sharing Limitation
LinkedIn's sharing API doesn't support pre-filling text - it only accepts URL parameter and pulls content from Open Graph meta tags. This is different from Twitter which supports both URL and text parameters.

## Project TODO Files and Their Relationships

### 1. Main Site TODO.md
**Location**: `/Users/philippetrounev/PycharmProjects/docsie-site/TODO.md`
**Purpose**: Site-wide SEO and technical issues
**Key Focus Areas**:
- 1,354 404 errors across the site
- Hreflang configuration issues (59% of pages)
- Canonical tag conflicts
- Sitemap issues
- Navigation and structure problems
- Crawl budget optimization

### 2. BlogVi TODO.md
**Location**: `/Users/philippetrounev/PycharmProjects/docsie-site/.external/BlogVi/TODO.md`
**Purpose**: Blog-specific features and enhancements
**Key Focus Areas**:
- AI feature implementation (FAQ, TL;DR, glossary - COMPLETED)
- Term pages implementation (Phase 1 priority)
- Image optimization (CRITICAL - not implemented)
- CTR optimization features
- GSC integration for performance tracking
- Platform-wide issues (CDN, portals, sites)

### 3. GSC Reports TODO.md
**Location**: `/Users/philippetrounev/PycharmProjects/docsie-site/gsc_reports/TODO.md`
**Purpose**: Google Search Console findings and action items
**Key Focus Areas**:
- Catastrophic CTR problem (0.18% vs expected 0.5-1.0%)
- Zero-click pages analysis
- Monitoring schedule for improvements
- Performance metrics and tracking

### Relationships Between TODOs:
1. **GSC Reports → BlogVi**: GSC findings drive BlogVi feature priorities (e.g., CTR issues led to title/meta description features)
2. **BlogVi → Main Site**: Blog improvements affect overall site SEO (e.g., crawl budget, content quality)
3. **Main Site → BlogVi**: Site-wide issues like 404s and hreflang affect blog performance

### Key Scripts and Tools:
- **GSC Integration**: `/Users/philippetrounev/PycharmProjects/docsie-site/.external/BlogVi/src/blog_vi/core/gsc_integration.py`
- **Title Baseline Capture**: `/Users/philippetrounev/PycharmProjects/docsie-site/gsc_reports/capture_title_baseline.py`
- **Title Generator**: `/Users/philippetrounev/PycharmProjects/docsie-site/.external/BlogVi/src/blog_vi/core/title_generator.py`
- **Meta Description Generator**: `/Users/philippetrounev/PycharmProjects/docsie-site/.external/BlogVi/src/blog_vi/core/meta_description.py`

### Current Project Status (July 2025):
1. **Completed**: Dynamic meta descriptions, title optimization, AI features (FAQ, TL;DR, glossary), Term pages Phase 1
2. **Monitoring**: CTR improvements from title/meta changes (2-4 week observation period)
3. **Recent Achievement**: Term pages generator implemented (July 29, 2025)
   - TermPageGenerator creates 400-500 word articles with Mermaid.js diagrams
   - Generates documentation use cases and best practices
   - Multi-threaded batch processing with 365-day caching
   - Ready to generate 100+ new SEO pages from glossary terms
4. **Critical Issues**: Image optimization missing, 1,354 404 errors, hreflang problems