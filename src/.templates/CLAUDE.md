# Component System Documentation

## Overview

The supplementary page system uses modular components defined in `/src/.templates/components/`. Each component is a self-contained directory with its own HTML template and CSS file.

## Generation Path

### 1. Source Files
```
/src/.data/[category]/[page-name].yaml  → YAML data definitions
/src/.templates/components/[name]/      → Component templates
```

### 2. Generation Process
```bash
# Generate all supplementary pages (uses v2 by default)
python supplementary_site_generator.py

# Force specific UI version
python supplementary_site_generator.py --v2
python supplementary_site_generator.py --v3

# Or use main.py which generates everything
python main.py
```

### 3. Output Location
```
/solutions/[category]/[page-id]/index.html
/solutions/[page-id]/index.html          # if no category
```

### 4. Template Resolution
The system looks for versioned components first, then falls back:
- Request `hero` with `ui_version: v2` → tries `hero_v2` → falls back to `hero`
- Component path: `.templates/components/hero_v2/hero_v2.html`

## Available V2 Components

### 1. **hero_v2** - Modern Hero Section
**Location:** `/src/.templates/components/hero_v2/hero_v2.html`

**Features:**
- Animated gradient background
- Badge support with icon
- Two-column layout (text + image)
- Primary and secondary CTA buttons
- Trust indicators (star ratings)
- Responsive animations

**YAML Structure:**
```yaml
hero_v2:
  badge: "New Feature"                    # Optional badge text
  title: "Main Headline"                  # Required
  description: "Subtitle or description"  # Required
  image: "/assets/path/to/image.jpg"     # Hero image
  cta:
    text: "Primary Action"
    url: "/destination/"                  # Use "#" for Calendly popup
  secondary_cta:                          # Optional
    text: "Secondary Action"
    url: "/other-destination/"
```

**Key Features:**
- Calendly integration when `url: "#"` or `url: ""`
- Image optimization with `optimized_image` filter
- Staggered animations (0.5s to 1.7s delays)
- Gradient text effects on title

---

### 2. **features_v2** - Feature Grid
**Location:** `/src/.templates/components/features_v2/features_v2.html`

**Features:**
- 3-column responsive grid
- Icon support with gradient backgrounds
- Hover effects with shadow and translation
- Optional CTA at bottom
- Background patterns and floating elements

**YAML Structure:**
```yaml
features_v2:
  badge: "Core Features"                  # Optional
  title: "Section Title"
  description: "Section description"
  features_list:
    - icon: "document"                    # Built-in icon types
      title: "Feature Name"
      description: "Feature description"
      link:                               # Optional
        text: "Learn More"
        url: "/destination/"
  cta:                                    # Optional bottom CTA
    text: "View All Features"
    url: "/features/"
```

**Built-in Icons:**
- `document` - Document icon
- `users` - Team/users icon
- `search` - Search icon
- `chart` - Bar chart icon
- `lightning` - Lightning bolt
- `shield` - Security shield
- Default: Checkmark

---

### 3. **faq_v2** - FAQ Section
**Location:** `/src/.templates/components/faq_v2/faq_v2.html`

**Features:**
- 2-column category grid
- Q&A format with color-coded labels
- Category headers with gradients
- Optional badge per category
- Bottom CTA

**YAML Structure:**
```yaml
faq_v2:
  badge: "Common Questions"
  title: "FAQ Title"
  description: "FAQ description"
  faq_categories:
    - title: "Category Name"
      icon: "fas fa-rocket"               # FontAwesome class
      badge: "Most Popular"               # Optional
      questions:
        - question: "Question text?"
          answer: "Answer text with details."
  cta:                                    # Optional
    text: "Contact Us"
    url: "/contact/"
    pretext: "Still have questions?"
```

**Styling:**
- Q: Blue label, bold text
- A: Green label, regular weight
- Category headers have gradient backgrounds

---

### 4. **testimonials_v2** - Testimonial Marquee
**Location:** `/src/.templates/components/testimonials_v2/testimonials_v2.html`

**Features:**
- Infinite scrolling marquee
- Avatar support (image or initials)
- 5-star rating display
- Hover pause functionality
- Gradient edge overlays

**YAML Structure:**
```yaml
testimonials_v2:
  badge: "Customer Success"
  title: "What Customers Say"
  description: "Trusted by leading companies"
  testimonials:
    - name: "John Doe"
      role: "CEO"                         # Optional
      company: "Acme Corp"                # Optional
      avatar: "/assets/avatar.jpg"        # Optional (uses initials if missing)
      rating: 5                           # 1-5 stars
      text: "Testimonial quote here"
```

**Auto-duplicates:** Cards are automatically duplicated for seamless looping

---

### 5. **modern_stats_v2** - Animated Statistics
**Location:** `/src/.templates/components/modern_stats_v2/modern_stats_v2.html`

**Features:**
- Animated counter on scroll
- 3-column grid
- Gradient icons
- Hover scale effects
- Intersection Observer for triggering

**YAML Structure:**
```yaml
modern_stats_v2:
  title: "By The Numbers"               # Not currently used in template
  stats:                                 # Currently hardcoded to 3 stats
    - number: 60
      suffix: "%"
      label: "Stat Label"
      description: "Stat description"
      icon: "growth"
```

**Note:** Template currently has hardcoded stats. To use custom stats, template needs modification.

---

### 6. **comparison_v2** - Traditional vs Modern
**Location:** `/src/.templates/components/comparison_v2/comparison_v2.html`

**Features:**
- Side-by-side comparison
- Red X icons for traditional
- Green checkmarks for modern
- "Recommended" badge on modern column

**YAML Structure:**
```yaml
comparison_v2:
  title: "Comparison Title"
  description: "Comparison description"
  comparisons_list:
    - traditional:
        title: "Old Way"
        points:
          - "Pain point 1"
          - "Pain point 2"
      modern:
        title: "New Way"
        points:
          - "Benefit 1"
          - "Benefit 2"
```

---

### 7. **cta_section_v2** - Call to Action
**Location:** `/src/.templates/components/cta_section_v2/cta_section_v2.html`

**Features:**
- Centered content
- Badge support
- Primary and secondary buttons
- Trust indicators
- Note text
- Calendly integration

**YAML Structure:**
```yaml
cta_section_v2:
  badge: "Get Started"
  title: "CTA Headline"
  description: "Compelling description"
  primary_button:
    text: "Main Action"
    url: "/signup/"
  secondary_button:
    text: "Secondary Action"
    url: "/demo/"
  note: "No credit card required"        # Optional
  trust_indicators:                      # Optional
    - text: "SOC 2 Certified"
      icon: true
    - text: "GDPR Compliant"
      icon: true
```

**Button Formats:**
- `primary_button` - Green gradient button
- `secondary_button` - White with border
- `cta` (legacy) - Triggers Calendly popup
- `buttons` (array) - For multiple buttons

---

### 8. **carousel_v2** - Image Carousel
**Location:** `/src/.templates/components/carousel_v2/carousel_v2.html`

**YAML Structure:**
```yaml
carousel_v2:
  title: "Carousel Title"
  description: "Carousel description"
  carousel_slides:
    - image: "/assets/image1.jpg"
      alt: "Alt text"
      caption: "Slide caption"
```

---

### 9. **benefits_v2** - Benefits Grid
**Location:** `/src/.templates/components/benefits_v2/benefits_v2.html`

**YAML Structure:**
```yaml
benefits_v2:
  badge: "Key Benefits"
  title: "Why Choose Us"
  description: "Benefits description"
  benefit_list:
    - icon: "fas fa-shield-alt"          # FontAwesome class
      title: "Benefit Name"
      description: "Benefit description"
```

---

### 10. **gallery_v2** - Image Gallery
**Location:** `/src/.templates/components/gallery_v2/gallery_v2.html`

**YAML Structure:**
```yaml
gallery_v2:
  title: "Gallery Title"
  description: "Gallery description"
  images:
    - src: "/assets/image1.jpg"
      alt: "Alt text"
      caption: "Image caption"
```

---

### 11. **feature_grid_v2** - Feature Grid Layout
**Location:** `/src/.templates/components/feature_grid_v2/feature_grid_v2.html`

**YAML Structure:**
```yaml
feature_grid_v2:
  title: "Advanced Features"
  description: "Feature grid description"
  features:
    - icon: "fas fa-video"               # FontAwesome class
      title: "Feature Name"
      description: "Feature description"
```

---

### 12. **feature_steps_v2** - Step-by-Step Process
**Location:** `/src/.templates/components/feature_steps_v2/feature_steps_v2.html`

**YAML Structure:**
```yaml
feature_steps_v2:
  title: "How It Works"
  description: "Process description"
  steps:
    - number: 1
      title: "Step Title"
      description: "Step description"
      icon: "fas fa-search"              # FontAwesome class
```

---

### 13. **stats_v2** - Statistics Display
**Location:** `/src/.templates/components/stats_v2/stats_v2.html`

**Note:** Similar to modern_stats_v2 but with different styling.

---

### 14. **related_auto** - Related Solutions
**Location:** `/src/.templates/components/related_auto/related_auto.html`

**Features:**
- Automatically fetches page data by URL
- Uses hero image from target page automatically
- Uses target page title and description
- Falls back to manual data only if URL lookup fails

**YAML Structure (Recommended - minimal):**
```yaml
related_auto:
  title: "Related Solutions"
  solutions:
    - url: "/solutions/documentation-from-video/"
    - url: "/solutions/knowledge-base/"
    - url: "/solutions/ai-technical-writer/"
```

**YAML Structure (With fallback data):**
```yaml
related_auto:
  title: "Related Solutions"
  solutions:
    - url: "/solutions/knowledge-base/"
      title: "Fallback Title"            # Only used if URL lookup fails
      description: "Fallback desc"       # Only used if URL lookup fails
      image: "/assets/fallback.jpg"      # Only used if URL lookup fails or page has no hero
```

**Best Practice:**
- Don't specify `title`, `description`, or `image` unless the target page doesn't exist yet
- Let the component auto-fetch from the actual solution pages for consistency
- The hero image will automatically match what users see on the solution page

---

## Specialized Components

### 15. **knowledge_graph_hero_v2** - Special Hero with Graph
**Location:** `/src/.templates/components/knowledge_graph_hero_v2/`

For knowledge-focused pages with visual graph elements.

---

### 16. **safari_v2** - Browser Mockup
**Location:** `/src/.templates/components/safari_v2/`

For showing product screenshots in Safari browser frame.

---

### 17. **interactive_3d** - 3D Elements
**Location:** `/src/.templates/components/interactive_3d/`

For pages needing 3D interactive elements (experimental).

---

## V1 Components (Legacy)

These components work but lack modern styling:
- `hero` - Basic hero
- `features` - Basic features grid
- `carousel` - Basic carousel
- `stats` - Basic statistics
- `comparison` - Basic comparison
- `benefits` - Basic benefits
- `reviews` - Customer reviews
- `related` - Related links
- `cta_section` - Basic CTA
- `gallery` - Basic gallery

---

## Component Testing Checklist

### Visual Checks
- [ ] Responsive behavior (mobile, tablet, desktop)
- [ ] Animations trigger correctly
- [ ] Hover states work
- [ ] Images load and display properly
- [ ] Gradients render correctly

### Functional Checks
- [ ] CTAs link to correct destinations
- [ ] Calendly popup triggers when appropriate
- [ ] Icons display correctly (FontAwesome loaded)
- [ ] Text content displays without overflow
- [ ] Component renders with minimal data
- [ ] Component renders with maximum data

### Cross-browser Checks
- [ ] Chrome/Edge (Chromium)
- [ ] Firefox
- [ ] Safari (macOS/iOS)

---

## Common Issues & Solutions

### Issue: Component not rendering
**Solution:** Check that component name matches directory name and template file name exactly.

### Issue: Icons not showing
**Solution:** Verify FontAwesome CDN is loaded in base template. Use full class names like `fas fa-icon-name`.

### Issue: Images not displaying
**Solution:** Ensure image paths are absolute from root (`/assets/...` not `assets/...`).

### Issue: Calendly popup not working
**Solution:** Ensure Cal.com script is loaded in base template. Use `url: "#"` or `url: ""` in CTA.

### Issue: Animations not triggering
**Solution:** Check that Tailwind CSS is loaded. Verify animation styles are in component's style block.

### Issue: Custom component data not displaying
**Solution:** Custom components (like `ai_capabilities`, `conversion_features`) need custom template sections. They won't auto-render like standard components.

---

## Creating New Components

### 1. Create Component Directory
```bash
mkdir src/.templates/components/my_component_v2
```

### 2. Create Template File
```bash
touch src/.templates/components/my_component_v2/my_component_v2.html
```

### 3. Create Style File
```bash
touch src/.templates/components/my_component_v2/style.css
```

### 4. Template Structure
```html
{% if section %}
<section class="my-component-v2 py-16">
  <div class="container mx-auto px-4">
    <h2>{{ section.title }}</h2>
    <p>{{ section.description }}</p>
    <!-- Component content -->
  </div>
</section>
{% endif %}
```

### 5. Register in supplementary_page.html
The component should be automatically available. Use in YAML:
```yaml
components:
  my_component_v2:
    title: "Component Title"
    # ... other properties
```

---

## File Generation Flow

```
1. YAML files in /src/.data/[category]/
   ↓
2. supplementary_site_generator.py reads YAML
   ↓
3. Loads supplementary_page_v2.html template
   ↓
4. For each component in YAML:
   - Looks for [component_name]_v2 template first
   - Falls back to [component_name] if v2 not found
   ↓
5. Renders complete page
   ↓
6. Outputs to /solutions/[category]/[id]/index.html
```

---

## Best Practices

1. **Always use v2 components** for new pages
2. **Test with minimal and maximal data** to ensure robustness
3. **Use semantic HTML** in component templates
4. **Keep styles scoped** to component class names
5. **Make components responsive** by default
6. **Use Tailwind utilities** for consistency
7. **Add fallbacks** for optional fields
8. **Document required vs optional** fields in YAML
9. **Test Calendly integration** if using CTAs
10. **Optimize images** before adding to assets

---

## URL Structure

Generated pages follow this pattern:
- Category page: `/solutions/[category]/[page-id]/`
- Top-level page: `/solutions/[page-id]/`
- Canonical URLs must include trailing slash

**Examples:**
- `/solutions/ai/tacit-knowledge-capture/`
- `/solutions/knowledge-base/`

---

## Debugging Tips

1. **Check console output** during generation for component load messages
2. **Verify YAML syntax** with a YAML validator
3. **Test incrementally** - add one component at a time
4. **Use browser DevTools** to inspect rendered HTML
5. **Check network tab** for failed asset loads
6. **Validate links** don't return 404s
7. **Review git diff** after regeneration to see what changed

---

## Integration with Main Site

Supplementary pages inherit:
- Header from `_header.html`
- Footer from `_footer.html`
- Base styles from `_base_v2.html`
- Favicon includes from `_favicon.html`
- Hreflang from `_hreflang.html`
- Structured data from `_structured_data.html`

Component-specific styles are injected via:
```html
<link rel="stylesheet" href="/styles/components/[component].css">
```
