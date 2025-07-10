# Docsie Translation System

A comprehensive translation system for the Docsie documentation platform using Anthropic's Claude API for high-quality translations.

## Features

- **Configuration-driven**: All settings managed via `translation_config.yaml`
- **AI-powered translations**: Uses Anthropic Claude for natural, context-aware translations
- **RTL language support**: Built-in support for right-to-left languages (Arabic, Hebrew, etc.)
- **Multi-language UI**: Dynamic language picker with proper routing
- **Batch processing**: Efficient translation with configurable batch sizes
- **Standard tools**: Uses industry-standard Babel for gettext workflow

## Quick Start

### 1. Setup
```bash
# Run the setup script
./setup_translations.sh

# Or manually:
pip install -r requirements_translation.txt
python translation_system.py extract
python translation_system.py init
```

### 2. Configure Languages
Edit `translation_config.yaml` to enable/disable languages:

```yaml
languages:
  es:
    name: "Español"
    enabled: true
    rtl: false
  fr:
    name: "Français"
    enabled: true
    rtl: false
  ar:
    name: "العربية"
    enabled: true
    rtl: true
```

### 3. Translate
```bash
# Add your API key to .env file
echo "ANTHROPIC_API_KEY='your-api-key-here'" >> .env

# Translate all enabled languages
python translation_system.py translate

# Or specific languages
python translation_system.py translate es fr de
```

### 4. Compile and Deploy
```bash
# Compile translations
python translation_system.py compile

# Build the site
python main.py
```

## Configuration

### `translation_config.yaml`

The main configuration file controls all aspects of the translation system:

#### Project Settings
```yaml
project:
  name: "Docsie Documentation Platform"
  source_language: "en"
  source_dir: "src/"
  locale_dir: "locale/"
```

#### Language Configuration
```yaml
languages:
  es:
    name: "Español"
    enabled: true
    rtl: false
  ar:
    name: "العربية"
    enabled: true
    rtl: true
```

#### Translation API Settings
```yaml
anthropic:
  model: "claude-sonnet-4-20250514"
  temperature: 0.1
  max_tokens: 1000
  batch_size: 20
  delay_between_batches: 1
```

#### Translation Behavior
```yaml
translation:
  skip_existing: true
  terminology:
    "Docsie": "Docsie"  # Don't translate brand names
    "API": "API"
  context: |
    Professional documentation platform interface.
    Maintain formal, business-appropriate tone.
```

#### UI Settings
```yaml
ui:
  language_picker:
    show_flag_icons: false
    show_language_code: true
    position: "footer"
  rtl_support:
    enabled: true
    rtl_stylesheet: "/assets/css/rtl.css"
    auto_detect: true
```

## Commands

### Extract Strings
```bash
python translation_system.py extract
```
Extracts all translatable strings from templates and creates `locale/messages.pot`.

### Initialize Languages
```bash
# Initialize all enabled languages
python translation_system.py init

# Initialize specific languages
python translation_system.py init es fr de
```

### Translate
```bash
# Translate all enabled languages
python translation_system.py translate

# Translate specific languages
python translation_system.py translate es fr

# Custom batch size
python translation_system.py translate es --batch-size 10
```

### Compile
```bash
# Compile all languages
python translation_system.py compile

# Compile specific languages
python translation_system.py compile es fr
```

### Complete Setup
```bash
# Setup all enabled languages
python translation_system.py setup --all-enabled

# Setup specific languages
python translation_system.py setup es fr de
```

### List Languages
```bash
python translation_system.py list-languages
```

## RTL Language Support

The system includes comprehensive RTL support:

### Automatic Detection
- Detects RTL languages from config
- Adds `dir="rtl"` to HTML automatically
- Loads RTL-specific CSS

### CSS Adjustments
The `rtl.css` file includes:
- Margin/padding flips
- Text alignment adjustments
- Component-specific RTL layouts
- Gradient and animation reversals

### Supported RTL Languages
- Arabic (ar)
- Hebrew (he)
- Persian/Farsi (fa)
- Urdu (ur)

## Template Usage

### Adding Translation Strings
Use the `{% trans %}` tag in templates:

```html
<h1>{% trans %}Welcome to Docsie{% endtrans %}</h1>
<p>{% trans %}Create amazing documentation{% endtrans %}</p>
```

### Variables in Translations
```html
<p>{% trans name=user.name %}Hello {{ name }}!{% endtrans %}</p>
```

### Pluralization
```html
{% trans count=items|length %}
  {%- if count == 1 -%}
    1 item
  {%- else -%}
    {{ count }} items
  {%- endif -%}
{% endtrans %}
```

## Language Picker

The system automatically generates a language picker component:

### Features
- Dropdown with all enabled languages
- Shows native language names
- Proper URL routing
- Mobile-friendly design
- Integrates with footer/header

### JSON Data
Generated at `/assets/languages.json`:
```json
{
  "default_language": "en",
  "languages": {
    "en": {
      "name": "English",
      "code": "en",
      "enabled": true,
      "rtl": false,
      "url": "/"
    },
    "es": {
      "name": "Español",
      "code": "es",
      "enabled": true,
      "rtl": false,
      "url": "/es/"
    }
  }
}
```

## File Structure

```
project/
├── translation_config.yaml     # Main configuration
├── translation_system.py       # Translation CLI tool
├── requirements_translation.txt # Python dependencies
├── setup_translations.sh       # Setup script
├── locale/                     # Translation files
│   ├── messages.pot           # Template file
│   ├── es/LC_MESSAGES/        # Spanish translations
│   │   ├── messages.po        # Editable translation file
│   │   └── messages.mo        # Compiled binary file
│   └── fr/LC_MESSAGES/        # French translations
├── src/                       # Template sources
│   ├── assets/
│   │   ├── css/rtl.css       # RTL stylesheet
│   │   └── languages.json    # Language picker data
│   └── _footer_v2.html       # Footer with language picker
└── babel.cfg                 # Babel configuration
```

## Best Practices

### 1. Translation Keys
- Use descriptive, context-aware strings
- Keep strings concise but meaningful
- Avoid concatenation

### 2. Configuration Management
- Review enabled languages regularly
- Update terminology as needed
- Test RTL layouts for RTL languages

### 3. Quality Assurance
- Review AI translations for accuracy
- Test language picker functionality
- Validate RTL layout on all pages

### 4. Performance
- Use appropriate batch sizes for API calls
- Compile translations after updates
- Cache language picker data

## Troubleshooting

### Common Issues

1. **API Rate Limits**
   - Increase `delay_between_batches` in config
   - Reduce `batch_size`

2. **Missing Translations**
   - Check if strings use `{% trans %}` tags
   - Run `extract` to update `.pot` file
   - Verify language is enabled in config

3. **RTL Layout Issues**
   - Ensure `rtl.css` is loaded
   - Check component-specific RTL rules
   - Test with actual RTL content

4. **Language Picker Not Working**
   - Verify `languages.json` exists
   - Check JavaScript console for errors
   - Ensure footer includes picker HTML

### Debug Mode
```bash
# Enable verbose output
python translation_system.py --verbose translate es

# Check specific language status
python translation_system.py list-languages
```

## Contributing

When adding new languages:

1. Update `translation_config.yaml`
2. Add language to enabled list
3. Include RTL flag if applicable
4. Test with sample content
5. Add any language-specific CSS rules

## License

This translation system is part of the Docsie platform and follows the same license terms.