# Docsie Unified CSS Design System

## Overview
This unified design system ensures consistent styling across all pages while preventing CSS conflicts. It uses Tailwind CSS with custom design tokens and scoped component styles.

## Architecture

### 1. Base Layer (`_base.html`)
- Loads core styles: FrankenUI, Tailwind CSS, Font Awesome
- Includes unified design system (`/styles/design-system.css`)
- Configures Tailwind with Docsie brand colors

### 2. Design System (`design-system.css`)
- **CSS Variables**: Brand colors, spacing, shadows
- **Utility Classes**: Extends Tailwind with brand-specific utilities
- **Scoped Components**: Component-specific styles with namespaced classes
- **Button System**: Unified button classes (`docsie-btn-primary`, `docsie-btn-secondary`)

### 3. Page-Specific Styles
- Only load essential page-specific stylesheets
- Avoid global style overrides
- Use scoped classes with prefixes (e.g., `docsie-knowledge-graph`)

## Brand Colors

```css
:root {
  --docsie-primary: #13AF4B;
  --docsie-primary-dark: #0f8f3d;
  --docsie-primary-light: #1bc95a;
}
```

Available as Tailwind classes:
- `bg-docsie-primary`
- `text-docsie-primary`
- `border-docsie-primary`
- `bg-docsie-gradient`

## Component Guidelines

### V2 Components
All V2 components should:
1. Use unified button classes (`docsie-btn-primary`, `docsie-btn-secondary`)
2. Use Tailwind utilities for layout and spacing
3. Reference brand colors via CSS variables or Tailwind classes
4. Scope custom styles with component prefixes

### Example V2 Button Usage
```html
<!-- Primary Button -->
<a href="/signup" class="docsie-btn-primary">
  Get Started
</a>

<!-- Secondary Button -->
<a href="/demo" class="docsie-btn-secondary">
  Learn More
</a>
```

### Custom Components
For complex components requiring custom styles:
1. Use scoped class names (e.g., `.docsie-knowledge-graph`)
2. Define styles in `design-system.css` under component-specific sections
3. Use CSS variables for consistent colors and spacing

## CSS Isolation Strategy

### Page Isolation
- `index_v2.html`: Uses scoped `.docsie-knowledge-graph` class
- Supplementary pages: Inherit base styles only
- No global style conflicts

### Component Isolation
- V2 components use unified system
- V1 components remain unchanged
- Clear separation prevents style bleeding

## Migration Guide

### Converting V1 to V2 Components
1. Replace hardcoded colors with CSS variables or Tailwind classes
2. Use unified button classes
3. Apply scoped class prefixes for custom styles
4. Test in isolation to prevent conflicts

### Adding New Components
1. Use Tailwind utilities first
2. Add custom styles to `design-system.css` with scoped prefixes
3. Follow naming convention: `docsie-{component-name}`
4. Document any new design tokens

## Testing

### Before Deployment
1. Build site: `python main.py`
2. Test index_v2.html in browser
3. Test supplementary pages (e.g., `/solutions/knowledge-base`)
4. Verify no style conflicts between pages

### Browser Testing
- Test responsive design on mobile/desktop
- Verify animations work correctly
- Check color consistency across components

## Benefits

1. **Consistency**: Unified color palette and design tokens
2. **Maintainability**: Single source of truth for styles
3. **Performance**: Reduced CSS redundancy
4. **Scalability**: Easy to add new components
5. **Isolation**: No style conflicts between pages

## Files Modified

- `/styles/design-system.css` - New unified design system
- `/src/_base.html` - Includes design system, adds brand colors to Tailwind
- `/src/index_v2.html` - Uses scoped styles and unified buttons
- `/src/.templates/components/hero_v2/hero_v2.html` - Updated to use unified buttons

## Future Improvements

1. Gradually migrate V1 components to use unified system
2. Create more reusable utility classes
3. Add dark mode support using CSS variables
4. Implement design tokens for animations and transitions