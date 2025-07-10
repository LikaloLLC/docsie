# Enhanced Image Generator Guide

## Overview

The new `image_generator_v2.py` creates startup-specific illustrations with:
- Flat vector isometric style
- Your design system colors (soft blue, lavender, deep indigo)
- Multiple variation themes (collaboration, innovation, growth, automation, connection)
- Ability to target specific images or patterns

## Quick Start

### 1. Regenerate a Specific Image
```bash
python utils/image_generator_v2.py --image "/assets/solutions/api-documentation-hero.jpg"
```

### 2. Regenerate All Hero Images
```bash
python utils/image_generator_v2.py --pattern "*/hero*" --override
```

### 3. Use Specific Style Variation
```bash
# Innovation style for hero images
python utils/image_generator_v2.py --pattern "*/hero*" --style innovation

# Collaboration style with specific variation
python utils/image_generator_v2.py --pattern "*/case*" --style collaboration --variation 2
```

### 4. Generate HD Quality Images
```bash
python utils/image_generator_v2.py --quality hd --image "/assets/solutions/ai-documentation-hero.jpg"
```

## Style Variations

### 🚀 Innovation
- Rocket ships, light bulbs, innovation labs
- Best for: Hero images, AI features, new products

### 🤝 Collaboration  
- Teams working together, remote connections
- Best for: Case studies, support pages, team features

### 📈 Growth
- Charts, plants growing, success paths
- Best for: Business pages, success stories, metrics

### 🤖 Automation
- Friendly robots, AI assistants, smart systems
- Best for: AI features, automation tools, workflows

### 🔗 Connection
- API handshakes, data bridges, integrations
- Best for: API docs, integrations, connectivity

## Preview Styles Without Generating

```bash
# See all style variations
python utils/image_style_preview.py

# Preview prompts for specific image type
python utils/image_style_preview.py --type hero --count 10

# Show startup visual concepts
python utils/image_style_preview.py --concepts
```

## Design System Integration

All generated images use your color palette:
- **Soft Blue**: #CFE8FF (primary backgrounds)
- **Lavender**: #E3D9FF (accent gradients)
- **Deep Indigo**: #2E2E8F (text, details)
- **White**: #FFFFFF (base background)

## Examples

### Generate All Missing Solution Images
```bash
python utils/image_generator_v2.py --pattern "/assets/solutions/*"
```

### Regenerate Specific Page Images with Style
```bash
# API Documentation page with connection theme
python utils/image_generator_v2.py --pattern "*api-documentation*" --style connection --override

# AI Features with automation theme
python utils/image_generator_v2.py --pattern "*ai-*" --style automation --override
```

### Test Single Image Generation
```bash
# Generate one image to test style
python utils/image_generator_v2.py \
  --image "/assets/new_home/solutions/api-documentation-hero.jpg" \
  --style innovation \
  --variation 0 \
  --override
```

## Tips

1. **Start Small**: Test with one image first to see if you like the style
2. **Use Patterns**: Target groups of related images for consistency
3. **Mix Styles**: Different page types can use different style themes
4. **HD Quality**: Use for hero images, standard for smaller images
5. **Preview First**: Use the preview script to see what prompts will be generated

## Troubleshooting

- **Rate Limits**: The script handles OpenAI rate limits automatically
- **Missing Images**: Run without --override first to see what's missing
- **Style Consistency**: Use same style/variation for related pages
- **API Key**: Ensure OPENAI_API_KEY is set in your .env file

## Cost Estimation

- Standard quality: ~$0.04 per image
- HD quality: ~$0.08 per image
- Full site regeneration: ~$2-4 depending on quality

## Next Steps

1. Preview the styles: `python utils/image_style_preview.py`
2. Test on one image to verify you like the style
3. Generate missing images for key pages
4. Consider HD quality for hero images only