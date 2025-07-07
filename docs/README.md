# Docsie Website Design System Documentation

## Overview

This documentation covers the Docsie website's design system, focusing on the new home page V2 implementation and supplementary pages architecture. The system uses a hybrid approach combining Jinja templating with modern CSS frameworks to deliver a unified, scalable design system.

## Architecture Stack

### Core Technologies
- **Jinja Templates**: Server-side templating engine for dynamic content
- **FrankenUI v2**: Modern UI framework with enhanced components
- **Tailwind CSS**: Utility-first CSS framework for styling
- **CSS Variables**: Global design tokens for consistency
- **Responsive Design**: Mobile-first approach with breakpoint-based layouts

### File Structure
```
src/
├── new_home/           # Home page components
│   ├── banner_v2/      # Hero section V2
│   ├── about_v2/       # About/Why Choose section V2
│   ├── ai_v2/          # AI features section V2
│   ├── security_v2/    # Security features section V2
│   ├── industries_v2/  # Industries showcase V2
│   ├── reviews_v2/     # Customer testimonials V2
│   └── ...             # Other V1 components
├── supplementary/      # Supplementary page components
└── shared/            # Shared components and utilities
```

## Design System Philosophy

### V2 Design Principles
1. **Mobile-First Responsive**: All components designed for mobile devices first
2. **Accessibility-First**: WCAG 2.1 AA compliance with proper semantic HTML
3. **Performance-Optimized**: Lightweight components with efficient CSS
4. **Animation-Enhanced**: Subtle animations to improve user experience
5. **Consistency**: Unified design tokens and component patterns

### Color System
- **Primary Colors**: Blue gradient system (`from-blue-600 to-blue-800`)
- **Secondary Colors**: Complementary gradients for accents
- **Dark Theme**: Consistent dark backgrounds with proper contrast ratios
- **Semantic Colors**: Success, warning, error, and info color variants

### Typography Scale
- **Headings**: Responsive typography with `text-4xl` to `text-6xl` for hero sections
- **Body Text**: Consistent text sizes with proper line heights
- **Font Weights**: Strategic use of font weights for hierarchy

## Component Architecture

### V2 Component Structure
Each V2 component follows this standard structure:

```html
<!-- Component Container -->
<section class="relative overflow-hidden bg-gradient-to-br from-slate-900 to-slate-800">
  <!-- Content Wrapper -->
  <div class="container mx-auto px-4 py-16 sm:px-6 lg:px-8">
    <!-- Content Grid -->
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
      <!-- Content goes here -->
    </div>
  </div>
</section>
```

### Key Component Features

#### 1. Banner V2 (`src/new_home/banner_v2/banner_v2.html`)
- **Purpose**: Hero section with dynamic messaging
- **Features**:
  - Rotating animated text ("customers love", "teams trust", "users need")
  - Gradient backgrounds with subtle animations
  - CTA buttons with hover effects
  - G2 reviews integration
  - Mobile-optimized layout

#### 2. About V2 (`src/new_home/about_v2/about_v2.html`)
- **Purpose**: "Why Choose Docsie" value proposition
- **Features**:
  - Animated statistics counters
  - Award badges display
  - Trust indicators
  - Performance metrics showcase

#### 3. AI V2 (`src/new_home/ai_v2/ai_v2.html`)
- **Purpose**: AI capabilities showcase
- **Features**:
  - Interactive tabs (desktop) / dropdown (mobile)
  - 4 AI features: Knowledge Base Chatbot, Video to Documentation, AI Technical Writer, Custom Content Prompts
  - Dark theme with gradient backgrounds
  - Responsive component switching

#### 4. Security V2 (`src/new_home/security_v2/security_v2.html`)
- **Purpose**: Security features and compliance
- **Features**:
  - 3-column grid layout
  - Enterprise security standards (SSL/TLS, GDPR, SOC 2)
  - 99.9% uptime guarantee
  - Trust badges and certifications

#### 5. Industries V2 (`src/new_home/industries_v2/industries_v2.html`)
- **Purpose**: Industry-specific solutions showcase
- **Features**:
  - 6 industry cards with hover effects
  - Colorful gradient backgrounds
  - Industry-specific feature highlights
  - Bottom CTA section

#### 6. Reviews V2 (`src/new_home/reviews_v2/reviews_v2.html`)
- **Purpose**: Customer testimonials and social proof
- **Features**:
  - 3-column testimonial grid
  - Star ratings display
  - Customer avatars
  - Staggered animations

## Supplementary Pages System

### Page Structure
Supplementary pages follow a consistent YAML-driven structure:

```yaml
# Page metadata
title: "Page Title"
description: "Page description"
layout: "supplementary"

# Content sections
sections:
  - type: "hero"
    data: { ... }
  - type: "features"
    data: { ... }
  - type: "testimonials"
    data: { ... }
```

### Benefits of YAML-Driven Architecture
1. **Content Management**: Easy content updates without HTML editing
2. **Consistency**: Enforced structure across all supplementary pages
3. **Scalability**: Easy to add new page types and sections
4. **Maintainability**: Centralized component logic with distributed content

## Implementation Guidelines

### Creating New V2 Components

1. **Component File Structure**:
   ```
   src/new_home/component_name_v2/
   ├── component_name_v2.html
   └── (optional) component_name_v2.css
   ```

2. **HTML Structure Standards**:
   - Use semantic HTML5 elements
   - Include proper ARIA attributes
   - Follow mobile-first responsive design
   - Use Tailwind CSS classes consistently

3. **CSS Guidelines**:
   - Use Tailwind utility classes primarily
   - Custom CSS only for complex animations
   - Follow the established color system
   - Maintain consistent spacing scales

### Animation Standards
- **Entrance Animations**: Subtle fade-in and slide-up effects
- **Hover Effects**: Smooth transitions with `transition-all duration-300`
- **Performance**: Use CSS transforms for hardware acceleration
- **Accessibility**: Respect `prefers-reduced-motion` settings

### Responsive Design Breakpoints
- **Mobile**: `< 640px` (default)
- **Tablet**: `sm: 640px+`
- **Desktop**: `lg: 1024px+`
- **Large Desktop**: `xl: 1280px+`

## Integration with Existing System

### V1 to V2 Migration Path
1. **Backward Compatibility**: V1 components remain functional
2. **Progressive Enhancement**: V2 components can be adopted incrementally
3. **Shared Resources**: Common CSS variables and utilities are shared
4. **Testing**: A/B testing capabilities between V1 and V2 versions

### Template Integration
V2 components integrate into pages using Jinja includes:

```html
<!-- index_v2.html -->
{% include "src/new_home/banner_v2/banner_v2.html" %}
{% include "src/new_home/about_v2/about_v2.html" %}
{% include "src/new_home/ai_v2/ai_v2.html" %}
{% include "src/new_home/security_v2/security_v2.html" %}
{% include "src/new_home/industries_v2/industries_v2.html" %}
{% include "src/new_home/reviews_v2/reviews_v2.html" %}
```

## Performance Considerations

### Optimization Strategies
1. **CSS Purging**: Remove unused Tailwind classes in production
2. **Critical CSS**: Inline critical styles for above-the-fold content
3. **Lazy Loading**: Progressive loading of non-critical components
4. **Image Optimization**: Responsive images with proper formats

### Loading Performance
- **First Contentful Paint**: Optimized for < 1.5s
- **Largest Contentful Paint**: Target < 2.5s
- **Cumulative Layout Shift**: Minimize layout shifts during load

## Accessibility Features

### WCAG 2.1 AA Compliance
- **Keyboard Navigation**: Full keyboard accessibility
- **Screen Reader Support**: Proper ARIA labels and roles
- **Color Contrast**: Minimum 4.5:1 contrast ratio
- **Focus Management**: Visible focus indicators
- **Semantic HTML**: Proper heading hierarchy and landmarks

### Testing Tools
- **axe-core**: Automated accessibility testing
- **Screen Readers**: NVDA, JAWS, VoiceOver testing
- **Keyboard Testing**: Tab navigation verification

## Development Workflow

### Local Development
1. **Environment Setup**: Ensure Jinja and CSS processing tools are configured
2. **Component Development**: Create components in isolation
3. **Integration Testing**: Test components in full page context
4. **Cross-Browser Testing**: Verify compatibility across browsers

### Code Quality Standards
- **HTML Validation**: Use W3C HTML validator
- **CSS Linting**: Follow established CSS style guides
- **Component Testing**: Test components in isolation
- **Performance Testing**: Monitor Core Web Vitals

## Future Enhancements

### Planned Improvements
1. **Component Library**: Standardized component documentation
2. **Design Tokens**: Expanded token system for consistency
3. **Animation Library**: Reusable animation components
4. **Testing Framework**: Automated visual regression testing

### Scalability Considerations
- **Component Variants**: Support for multiple component styles
- **Theming System**: Support for multiple brand themes
- **Internationalization**: Multi-language support expansion
- **Performance Monitoring**: Real-time performance tracking

## Maintenance and Support

### Regular Maintenance Tasks
1. **Dependency Updates**: Keep frameworks and tools updated
2. **Performance Audits**: Regular performance monitoring
3. **Accessibility Audits**: Ongoing accessibility compliance
4. **Browser Testing**: Cross-browser compatibility verification

### Documentation Updates
- **Component Changes**: Document any component modifications
- **New Features**: Update documentation for new capabilities
- **Best Practices**: Evolve guidelines based on learnings
- **Migration Guides**: Provide clear upgrade paths

---

## Quick Start Guide

### For Developers
1. **Clone Repository**: Get the latest codebase
2. **Install Dependencies**: Set up development environment
3. **Review Components**: Study existing V2 components
4. **Follow Guidelines**: Use this documentation as reference
5. **Test Thoroughly**: Ensure accessibility and performance

### For Content Managers
1. **YAML Structure**: Learn supplementary page YAML format
2. **Content Guidelines**: Follow established content patterns
3. **Image Guidelines**: Use properly optimized images
4. **Testing**: Preview changes in staging environment

### For Designers
1. **Design System**: Follow established design tokens
2. **Component Patterns**: Use existing component structures
3. **Accessibility**: Design with accessibility in mind
4. **Performance**: Consider performance in design decisions

---

*This documentation is living and should be updated as the system evolves. For questions or suggestions, please contribute to the documentation or reach out to the development team.* 