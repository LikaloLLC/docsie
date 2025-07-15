# How to Translate the Docsie Site

This guide explains how to translate the Docsie static site into multiple languages using the built-in translation system that leverages Claude AI for automated translations.

## Prerequisites

1. **Claude API Key**: Set the `CLAUDE_API_KEY` environment variable
   ```bash
   export CLAUDE_API_KEY="your-api-key-here"
   ```

2. **Python Dependencies**: Install required packages
   ```bash
   pip install -r requirements_translation.txt
   ```

3. **Virtual Environment** (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

## Quick Start - Translate Everything

To translate the entire site into all configured languages:

```bash
# Full translation workflow - MUST specify what to run
# Option 1: Run extraction and translation
sh build_multilingual.sh --skip-extract=false --skip-translate=false --skip-yaml=false

# Option 2: Just run translation (if strings already extracted)
sh build_multilingual.sh --skip-translate=false --skip-yaml=false

# Option 3: Force retranslation (ignore cache)
sh build_multilingual.sh --skip-translate=false --skip-yaml=false --force

# Quick mode (skip extraction and translation, just compile and generate)
sh build_multilingual.sh --quick
```

**Note**: By default, the script skips extraction and translation to avoid accidental API usage. You must explicitly enable these steps.

## Step-by-Step Translation Process

### 1. Extract Translatable Strings

Extract all translatable strings from templates and Python files:

```bash
# Using translation system
python translation_system.py extract

# Or directly with pybabel
pybabel extract -F babel.cfg -o locale/messages.pot .
```

### 2. Initialize or Update Language Files

For new languages:
```bash
# Initialize a single language
python translation_system.py init --lang es

# Initialize multiple languages
python translation_system.py init --lang es,fr,de

# Initialize all configured languages
python translation_system.py init
```

For existing languages:
```bash
# Update existing PO files with new strings
python translation_system.py update
```

### 3. Translate Missing Strings

Translate using Claude AI (uses caching to avoid re-translating):

```bash
# Translate all languages
python translation_system.py translate

# Translate specific languages
python translation_system.py translate --lang es,fr

# Translate with specific batch size (default: 20)
python translation_system.py translate --batch-size 50
```

### 4. Compile Translations

Compile PO files to binary MO format:

```bash
# Compile all languages
python translation_system.py compile

# Compile specific language
pybabel compile -d locale -l es
```

### 5. Generate Multilingual Site

Generate static pages for all languages:

```bash
python generate_all_languages.py
```

## Managing Specific Components

### Translating the New Pricing Page

The pricing page components use `{% trans %}` tags throughout. After making changes:

1. **Extract new strings**:
   ```bash
   python translation_system.py extract
   ```

2. **Update language files**:
   ```bash
   python translation_system.py update
   ```

3. **Translate new strings only** (cached strings are skipped):
   ```bash
   python translation_system.py translate
   ```

4. **Compile and generate**:
   ```bash
   python translation_system.py compile
   python generate_all_languages.py
   ```

### Key Pricing Page Files with Translations:
- `src/pricing_v2/index.html` - Main pricing page
- `src/new_home/pricing_cards_v2/pricing_cards_v2.html` - Pricing plan cards
- `src/new_home/enterprise_portal_v2/enterprise_portal_v2.html` - Enterprise add-on section
- `src/pricing_v2/generated_comparison_table.html` - Feature comparison table

## Translation Configuration

### Main Configuration File: `translation_config.yaml`

```yaml
# Languages to translate (can be enabled/disabled)
languages:
  es:
    name: Español
    enabled: true
    rtl: false
  # ... more languages

# Translation settings
translation:
  batch_size: 20
  max_workers: 3
  model: claude-sonnet-4-20250514
  temperature: 0.3
```

### Adding a New Language

1. Add to `translation_config.yaml`:
   ```yaml
   languages:
     pt-br:
       name: Português (Brasil)
       enabled: true
       rtl: false
   ```

2. Initialize the language:
   ```bash
   python translation_system.py init --lang pt-br
   ```

3. Follow the translation workflow above

## Caching System

The translation system uses intelligent caching to save time and API costs:

### Cache Locations:
- **String translations**: `.translation_cache/translations.pkl`
- **YAML translations**: `.translation_cache/yaml_translations.json`

### Cache Management:
```bash
# Clear all caches (forces re-translation)
rm -rf .translation_cache/

# Clear specific language cache
# Note: Currently requires manual editing of cache files
```

### How Caching Works:
1. Each string is hashed (source text + target language)
2. Translations are stored with their hash as the key
3. Before translating, the system checks if a cached translation exists
4. Only new or changed strings are sent to Claude API

## Monitoring Translation Progress

During translation, you'll see progress indicators:

```
Translating to Spanish (es)...
Processing batch 1/5...
[████████████████████████████████] 100/100 strings translated
Spanish translation completed in 45.2 seconds
```

## Best Practices

1. **Regular Updates**: Run translations after any content changes
2. **Review Generated Files**: Check a few translated pages for quality
3. **Use Quick Mode**: When only compiling without new translations
4. **Batch Similar Changes**: Group content updates to minimize API calls
5. **Monitor API Usage**: Each batch of 20 strings = 1 API call

## Troubleshooting

### Common Issues:

1. **Missing API Key**:
   ```
   Error: CLAUDE_API_KEY environment variable not set
   ```
   Solution: Set the environment variable

2. **Import Errors**:
   ```
   ModuleNotFoundError: No module named 'babel'
   ```
   Solution: Install dependencies: `pip install -r requirements_translation.txt`

3. **Permission Errors**:
   ```
   PermissionError: [Errno 13] Permission denied: 'locale/es/LC_MESSAGES'
   ```
   Solution: Check file permissions or run with appropriate privileges

4. **Cache Corruption**:
   ```
   Error loading cache: ...
   ```
   Solution: Delete cache directory: `rm -rf .translation_cache/`

## Advanced Usage

### Translate Specific Strings Only

For targeted updates, you can modify the POT file to include only specific strings before running update:

```bash
# Create a temporary POT with specific strings
grep -A2 -B2 "Pricing" locale/messages.pot > locale/temp.pot
# Manually edit temp.pot to keep only desired strings
# Then update from this file
```

### Parallel Translation

The system supports concurrent translation of multiple languages:

```bash
# Adjust max workers in translation_config.yaml
translation:
  max_workers: 5  # Increase for more parallel processing
```

### Custom Translation Rules

Modify prompts in `translation_system.py` to adjust translation style:
- Formal vs. informal tone
- Technical terminology handling
- Brand name preservation

## Summary Workflow for Pricing Page Updates

After making changes to pricing page components:

```bash
# 1. Extract new strings
python translation_system.py extract

# 2. Update all language files
python translation_system.py update

# 3. Translate (only new strings due to caching)
python translation_system.py translate

# 4. Compile translations
python translation_system.py compile

# 5. Generate multilingual site
python generate_all_languages.py

# Or use the all-in-one script:
sh build_multilingual.sh
```

The entire process typically takes 5-10 minutes depending on the number of new strings and languages enabled.