# Homepage V2 Redesign - Implementation Guide

**Status**: In Progress
**Last Updated**: November 23, 2025
**Primary File**: `/Users/philippetrounev/PycharmProjects/docsie-site/src/index_v2.html`

---

## Overview

This document tracks the complete redesign of the Docsie homepage (V2) with a **warm design system** featuring brown/orange gradients, modern Bento Grid layouts, and streamlined messaging that better represents what Docsie actually does.

---

## Design System Foundation

### Color Palette (Warm Theme)

**Primary Colors:**
- `--v2-orange: #FF6738` - Primary action color
- `--v2-orange-light: #FEA85E` - Lighter orange for gradients
- `--v2-brown: #3C2218` - Dark brown for headlines
- `--v2-brown-light: #6F5A52` - Lighter brown for body text

**Semantic Colors:**
- `--docsie-v2-brown: #3C2218` (headline text)
- `--docsie-v2-brown-light: #6F5A52` (body text)

**Gradient:**
```css
.warm-gradient {
  background: linear-gradient(180deg,
    #FFF7EC 0%,     /* Warm cream */
    #FFE5C5 100%    /* Warm peach */
  );
}
```

**Background Pattern:**
```css
.banner-grid {
  background-image:
    linear-gradient(rgba(178, 73, 52, 0.05) 1px, transparent 1px),
    linear-gradient(90deg, rgba(178, 73, 52, 0.05) 1px, transparent 1px);
  background-size: 20px 20px;
}
```

**Floating Blobs:**
```css
.blob-orange {
  background: rgba(255, 103, 56, 0.1);
  /* Positioned top-left: -top-40 -left-40 */
}

.blob-brown {
  background: rgba(178, 73, 52, 0.1);
  /* Positioned bottom-right: -bottom-40 -right-40 */
}
```

### Typography System

**Location**: `styles/design-system.css`

**Heading Classes:**
- `.heading-xl` - Large section headings (4rem desktop, responsive)
- `.heading-lg` - Subsection headings (2.5rem desktop)
- `.heading-md` - Card headings (1.875rem)
- `.heading-sm` - Small headings (1.5rem)

**Body Classes:**
- `.body-lg` - Large body text (1.25rem, line-height 1.5)
- `.body-base` - Standard body text (1rem, line-height 1.6)
- `.eyebrow` - Small uppercase labels (0.875rem, tracking-wide)

**Color Classes:**
- `.text-headline-warm` - Brown headlines (#3C2218)
- `.text-body-warm` - Brown body text (#6F5A52)

**Fonts:**
- Sans: `'Inter', system-ui, -apple-system, sans-serif`
- Mono: `'JetBrains Mono', 'Courier New', monospace`

### Border Radius

```css
--warm-radius: 24px;  /* Bento cards, media elements */
```

---

## Critical SEO Fix (August 22, 2025)

### The Incident

On August 22, 2025, www.docsie.io was **completely deindexed by Google** due to `<title>` and `<meta name="description">` tags appearing on line 321+ instead of within the first 50 lines.

### Root Cause

Large include files (`_hreflang.html` and `_structured_data.html`) were placed **BEFORE** critical SEO tags in base templates.

### The Fix

**All base templates updated** (`_base.html`, `_base_v2.html`, `_base_v3.html`):
1. Title/description moved to lines 13-14
2. Includes moved AFTER critical SEO tags
3. Fixed malformed `name=description` (missing quotes)

**Prevention Rule:**
- **ALWAYS** ensure `<title>` and `<meta name="description">` appear within first 50 lines of HTML output

---

## Components Redesigned

### 1. Hero Banner (`new_home/banner_v2/`)

**Files:**
- `banner_v2.html` - Main template
- `banner_v2.css` - Component styles

**Layout:**
- Two-column grid (text left, video right)
- Hero badge with lightning icon: "AI Knowledge Orchestration Platform"
- Main title: "Turn training videos and PDFs into enterprise knowledge base. Automatically."
- Subtitle: "Transform training videos, PDFs, and unstructured content into structured documentation and secure branded client portals."
- Single CTA: "Book Demo" (Cal.com integration)
- G2 rating badge (4.8 stars, 100+ reviews)
- Video demo card on right side

**Customer Logos:**
- Horizontal strip below hero
- 6 logos: Canada, Fellowmind, North Highland, AddSecure, PowerFlex, Becklar
- Mobile: Infinite scroll carousel (3x clone, -33.333% translateX)
- Desktop: Static centered row (max-width: 75%)
- Grayscale with hover color transition

**Key CSS:**
```css
.hero-video-card {
  background: linear-gradient(135deg,
    rgba(255, 247, 236, 0.20) 0%,
    rgba(255, 229, 197, 0.25) 100%
  );
  backdrop-filter: blur(10px);
  border-radius: var(--warm-radius);
  padding: 20px 20px 18px;
}
```

### 2. Process Timeline (`new_home/process_timeline_v2/`)

**File:** `process_timeline_v2.html` (self-contained with CSS + JS)

**Layout:**
- Section header: "See it in action" eyebrow + "How Docsie Works" title
- Step indicator pills (01 Convert, 02 Manage, 03 Deliver)
- Animated progress bar
- Auto-cycling steps (10 seconds per step)

**Grid Layout:**
- Desktop: 52fr / 48fr split (55/45 balance)
- Gap: 8 (reduced from 12)
- Alignment: `items-start` (not center)

**Three Steps:**

#### Step 1: 🟧 CONVERT
**Title:** "Turn scattered content into structured documentation — automatically."

**Description:** "Docsie's AI agent transforms your training videos, PDF manuals, and entire documentation websites into clean, searchable documentation. Start with one video — scale to your entire knowledge base."

**6 Bullets:**
- Extract workflows and step-by-step guides from training videos
- Convert manuals and scanned PDFs with AI vision
- Import complete documentation sites at scale (200K+ URLs tested)
- Refine structure through conversational AI — preview, edit, approve
- Batch-process entire knowledge bases, not individual files
- Use 40+ autonomous tools to create, search, translate, and organize docs

**Badge:** "Powered by Multimodal AI & Computer Vision"

#### Step 2: 🟦 MANAGE
**Title:** "Your documentation system — versioned, collaborative, always current."

**Description:** "Once content is generated, Docsie becomes the control center for everything: structure, versions, variants, translations, and team workflows."

**6 Bullets:**
- Branch, diff, and merge versions — including client-specific variants
- Collaborate in real time with granular roles and permissions
- Translate into 100+ languages with automated AI workflows
- Use reusable templates and structured content blocks
- Enforce consistency with formatting, style, and quality checks
- Track every change with reviews, history, and audit trails

**Badge:** "Built for Version Control & Collaboration at Scale"

#### Step 3: 🟩 DELIVER
**Title:** "Deploy secure, branded client portals — at scale."

**Description:** "Give every client, partner, or region its own isolated documentation portal with custom branding, domains, and access rules."

**8 Bullets:**
- Fully isolated portals with white-label branding and custom domains
- Route users by email domain, SSO attributes, or custom rules
- Support enterprise SSO/SAML (Azure AD, Okta, Google)
- Control access by teams, clients, and deployments
- Authenticate with branded invites, OTP, and magic links
- Track engagement, search, usage, and access history per portal
- White-label UI, emails, login flows, and domain experience
- Scale to thousands of portals from a single workspace

**Badge:** "Multi-Tenant SaaS Infrastructure Built In"

**Typography Tightening:**
- Content max-width: 620px
- Paragraph max-width: 580px
- Bullet list max-width: 600px
- Reduced line-heights: body-lg (1.5), body-base (1.6)
- Reduced spacing: subtitle mb-0.5rem, paragraph mb-1rem
- Bullet spacing: space-y-3 (was space-y-4)

**Media Card:**
- Min-height: 500px (desktop), 420px (tablet)
- Transform: translateY(-20px) to align with first bullet
- Bento-style gradient background matching hero

**JavaScript Autoplay:**
- Duration: 10 seconds per step
- Progress bar animates 0-100% across 3 steps
- Resets to 0% when cycling back to step 1
- Manual clicks pause for 5 seconds then resume
- No hover interruptions (removed mouseenter/mouseleave)

**Key Fixes Applied:**
1. Reduced section header margin: mb-16 → mb-12
2. Reduced pill-to-progress gap: mb-12 → mb-8
3. Tightened grid gap: gap-12 → gap-8
4. Changed alignment: items-center → items-start
5. 52/48 grid split on desktop
6. Scaled up media card height (70-75% of text height)
7. Nudged screenshot up 20px

### 3. Pain Point Bento Grid (`new_home/pain_point_bento/`)

**File:** `pain_point_bento.html`

**Status:** Created, not yet integrated into `index_v2.html`

**Layout:**
- 3-column Bento Grid
- Warm gradients matching design system
- Translucent backgrounds (15-35% opacity)
- Glass morphism effects

**Design Tokens:**
```css
.bento-card {
  background: linear-gradient(135deg,
    rgba(255, 247, 236, 0.30) 0%,
    rgba(255, 229, 197, 0.35) 100%
  );
  backdrop-filter: blur(10px);
  border-radius: var(--warm-radius);
  box-shadow:
    0 0 0 1px rgba(178, 73, 52, 0.10),
    0 4px 12px rgba(255, 103, 56, 0.08);
}
```

---

## File Structure

### Key Directories

```
/Users/philippetrounev/PycharmProjects/docsie-site/
├── src/
│   ├── index_v2.html                    # Main V2 homepage
│   ├── _base_v2.html                    # Base template (SEO-fixed)
│   ├── _footer_v2.html                  # Footer component
│   └── new_home/
│       ├── banner_v2/
│       │   ├── banner_v2.html
│       │   └── banner_v2.css
│       ├── process_timeline_v2/
│       │   └── process_timeline_v2.html # Self-contained
│       ├── pain_point_bento/
│       │   └── pain_point_bento.html    # Not yet integrated
│       ├── about_v2/
│       ├── solution_picker_v2/
│       └── [other components]
├── styles/
│   └── design-system.css                # Global typography & colors
├── site_config.yaml                     # Controls which version builds
└── main.py                              # Build script
```

### Version Control (site_config.yaml)

```yaml
homepage_version: "v2"  # Controls which index.html is built
pricing_version: "v2"
canonical_domain: "https://www.docsie.io"
```

**How it works:**
- `homepage_version: "v2"` → `src/index_v2.html` builds to `index.html`
- V3 files exist but are not active (enable_v3_preview: false)
- Prevents accidental deployment of WIP versions

---

## Design Principles

### 1. Use ONLY Design System Classes

**DO:**
```html
<h2 class="heading-xl text-headline-warm">
<p class="body-lg text-body-warm">
```

**DON'T:**
```html
<h2 class="text-4xl font-bold text-brown-900">  ❌ Custom classes
<p class="mb-4">                                 ❌ Inline spacing
```

### 2. Component-Specific Styles in <style> Tags

**DO:**
```css
/* Component spacing */
.timeline-content h3 {
  margin-bottom: 0.875rem;
}
```

**DON'T:**
```html
<h3 class="heading-lg mb-3">  ❌ Don't use Tailwind margin classes
```

### 3. Build ON TOP of Design System

- Design system = foundation (typography, colors)
- Component CSS = delta (spacing, animations, interactions)
- Never override design system variables

### 4. Warm Gradient Backgrounds

All sections use warm gradient + pattern + blobs:

```html
<section class="warm-gradient relative overflow-hidden">
  <div class="absolute inset-0 opacity-5">
    <div class="absolute inset-0 banner-grid"></div>
  </div>
  <div class="absolute -top-40 -left-40 w-80 h-80 rounded-full blur-3xl blob blob-orange"></div>
  <div class="absolute -bottom-40 -right-40 w-80 h-80 rounded-full blur-3xl blob blob-brown"></div>

  <div class="relative z-10">
    <!-- Content here -->
  </div>
</section>
```

---

## Development Workflow

### Build Commands

```bash
# Build site
python main.py

# Start dev server (port 8081)
sh start.sh

# Auto-rebuild on changes
sh auto_compile.sh
```

### Testing Checklist

1. **SEO Check**: View source → title/description on lines 13-14
2. **Responsive Test**: Mobile (375px), Tablet (768px), Desktop (1440px)
3. **Animation Test**: Process timeline autoplay cycles smoothly
4. **Video Test**: Hero video autoplays muted
5. **Logo Carousel**: Mobile infinite scroll works

---

## Known Issues & TODO

### Completed ✅
- Hero banner with warm design
- Process timeline with auto-cycling
- Fixed SEO meta tag positioning
- Logo strip with mobile carousel
- Typography tightening (7 visual fixes)
- Progress bar auto-rewind
- Removed hover interruptions

### In Progress 🟡
- Pain Point Bento Grid created but not integrated
- Other V2 components need warm design migration

### Blocked/Future 🔴
- V3 homepage exists but not active
- Multilingual variants need hreflang fixes (see main TODO.md)

---

## Copy Guidelines

### Hero Title Pattern
- Line 1: Action verb + what they have
- Line 2: Transform into what they want
- Line 3: Outcome qualifier

**Example:**
```
Turn training videos and PDFs
into enterprise knowledge base.
Automatically.
```

### Process Step Pattern
Each step follows:
1. **Icon + Title** (e.g., 🟧 CONVERT)
2. **Subtitle** - One sentence outcome
3. **Description** - Two sentences on how/why
4. **6-8 Bullets** - Action-oriented, start with verb
5. **Tech Badge** - What powers it

### Messaging Hierarchy
1. **What it does** (outcome first)
2. **How it works** (process second)
3. **Why it matters** (benefits third)
4. **Proof points** (scale, customers, tech)

---

## Critical Rules

### SEO
1. ✅ Title/description MUST be in first 50 lines
2. ✅ Use canonical URLs with www: `https://www.docsie.io`
3. ✅ All pages need proper hreflang (see main TODO.md)

### Design System
1. ✅ Never use custom typography classes
2. ✅ Component spacing in CSS, not inline
3. ✅ Match Bento aesthetic: translucent, minimal shadows
4. ✅ Use warm gradient + blobs consistently

### JavaScript
1. ✅ No hover interruptions on carousels
2. ✅ Progress bars must reset on cycle
3. ✅ Videos autoplay muted with error handling

---

## Next Steps for New Developer

### Immediate Tasks
1. **Integrate Pain Point Bento Grid** into `index_v2.html`
2. **Update About V2** with warm design
3. **Update Solution Picker V2** with warm design
4. **Test full page flow** from hero → process → pain points → CTA

### Medium Priority
1. Review other V2 components for warm design consistency
2. Add animations/transitions to Bento cards
3. Create mobile-optimized layouts for all sections
4. Performance audit (image optimization, lazy loading)

### Low Priority
1. A/B test hero copy variants
2. Add micro-interactions to CTAs
3. Implement scroll-triggered animations
4. Consider V3 activation timeline

---

## Resources

### Design System Reference
- Main file: `styles/design-system.css`
- Color palette: Lines 1-20
- Typography: Lines 30-150
- Utilities: Lines 150+

### Component Examples
- Best reference: `new_home/banner_v2/banner_v2.html`
- Self-contained: `new_home/process_timeline_v2/process_timeline_v2.html`
- Bento pattern: `new_home/pain_point_bento/pain_point_bento.html`

### Related Documentation
- `CLAUDE.md` - Project instructions & SEO incident details
- `TODO.md` - Site-wide issues (1,354 404 errors, hreflang)
- `site_config.yaml` - Version control settings

---

## Contact & Escalation

**Design Questions**: Refer to warm design system in `design-system.css`
**Copy Questions**: Use existing process_timeline_v2 as template
**SEO Issues**: CRITICAL - Review August 2025 incident in CLAUDE.md
**Build Issues**: Check `site_config.yaml` version settings

---

**Last Tested**: November 23, 2025
**Browser Support**: Chrome 120+, Safari 17+, Firefox 121+
**Mobile Tested**: iOS Safari 17, Android Chrome 120
