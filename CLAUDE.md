# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is the static website repository for Docsie.io, a documentation platform. The site is built using Python with staticjinja (a static site generator based on Jinja2 templates) and hosted on GitHub Pages.

## Architecture

- **Static Site Generator**: Custom staticjinja implementation with Jinja2 templates
- **Template Engine**: Jinja2 with markdown support and internationalization
- **Content Sources**: Templates in `src/` directory, blog content fetched from RSS feeds
- **Output**: Static HTML files generated to root directory
- **Internationalization**: Multi-language support with Babel (de, es, fr, jp, ko, pt languages)
- **Blog System**: Uses BlogVI for blog generation with YAML configuration

## Key Directories

- `src/`: Source templates and content
- `blogvi/`: Blog configuration and templates
- `staticjinja/`: Custom staticjinja implementation
- `assets/`: Static assets (images, CSS, JS)
- `locale/`: Translation files
- `scss/`: SCSS source files for styling

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

## Main Site vs BlogVi Comparison

### Main Site (Docsie.io)
- **Theming**: Uses a modern V2 design system with:
  - Design tokens in `/styles/design-system.css` and `/styles/design-tokens.css`
  - Component-based CSS architecture in `/styles/components/`
  - Support for both V1 and V2 templates (`_base.html` and `_base_v2.html`)
  - Tailwind-compatible utilities
  - Dark mode support
  - Responsive design with mobile-first approach

- **Translation System**:
  - Sophisticated multi-language support (30+ languages)
  - Uses `translation_system.py` with Claude API integration
  - Babel-based string extraction and compilation
  - YAML translation for content files
  - Caching system for translations
  - Batch translation support
  - Build script: `sh build_multilingual.sh`

### BlogVi System
- **Current State**:
  - Standalone blog generator in `.external/BlogVi/`
  - Uses basic Tailwind CSS from CDN
  - Simple template structure without design system integration
  - Separate translation system using Claude API with batch support
  - Generates content into `/blog/` directory of main site

- **Design Gaps**:
  - Not using main site's design system
  - Different header/footer implementations
  - Inconsistent styling and branding
  - Missing V2 design elements
  - No dark mode support

## Design Alignment Strategy

### Short-term Improvements
1. **Import Main Site Design System**:
   - Copy design tokens and utilities to BlogVi
   - Update BlogVi templates to use main site CSS classes
   - Align color schemes, typography, and spacing

2. **Template Synchronization**:
   - Adapt BlogVi's header.html and footer.html to match main site's `_header_v2.html` and `_footer_v2.html`
   - Use consistent navigation structure
   - Apply same responsive breakpoints

3. **Translation Integration**:
   - Align language codes between systems
   - Share translation cache if possible
   - Use consistent translation settings

### Long-term Architecture Recommendations
1. **Unified Build System**:
   - Integrate BlogVi generation into main build pipeline
   - Share Jinja2 environment and filters
   - Use single translation system for both

2. **Component Library**:
   - Extract reusable components (cards, buttons, forms)
   - Create shared template includes
   - Maintain single source of truth for UI elements

3. **Design System Extension**:
   - Add blog-specific components to design system
   - Create article typography styles
   - Define category and tag styling

## Implementation Notes

- BlogVi currently runs as a separate system but generates into main site's `/blog/` directory
- Both systems use Claude API for translations but with different implementations
- Main site has more mature theming with V2 design system
- Blog needs to adopt main site's design patterns for consistency