# Component System TODO

## Phase 1: Component Testing & Documentation ✅

### Test Page Creation
- [x] Create comprehensive test YAML (`tacit-knowledge-capture.yaml`)
- [x] Include all V2 components
- [x] Include specialized components
- [x] Document YAML structure for each component

### Documentation
- [x] Create CLAUDE.md with component documentation
- [x] Document generation path
- [x] Document YAML structure for each component
- [x] Add troubleshooting section
- [x] Add best practices

### Next Steps: Component Validation
- [ ] Generate test page (`python supplementary_site_generator.py`)
- [ ] Visual inspection of all components
- [ ] Functional testing (CTAs, animations, responsive)
- [ ] Cross-browser testing

---

## Phase 2: Component Validation (Current Phase)

### Visual Testing
- [ ] **hero_v2**
  - [ ] Badge displays correctly
  - [ ] Title gradient renders
  - [ ] Image loads and scales properly
  - [ ] Primary CTA works
  - [ ] Secondary CTA works
  - [ ] Trust indicators display
  - [ ] Responsive on mobile

- [ ] **features_v2**
  - [ ] 3-column grid on desktop
  - [ ] Icons display correctly
  - [ ] Hover effects work (shadow, translate)
  - [ ] Optional link arrows work
  - [ ] Background patterns visible
  - [ ] Responsive grid on mobile/tablet

- [ ] **faq_v2**
  - [ ] Category headers render
  - [ ] Q&A format displays correctly
  - [ ] Colors (blue Q, green A) correct
  - [ ] Category badges work
  - [ ] 2-column grid on desktop
  - [ ] Bottom CTA renders

- [ ] **testimonials_v2**
  - [ ] Marquee scrolls smoothly
  - [ ] Pause on hover works
  - [ ] Avatars display (or initials)
  - [ ] Star ratings render
  - [ ] Gradient overlays at edges
  - [ ] Cards don't have gaps

- [ ] **modern_stats_v2**
  - [ ] Counters animate on scroll
  - [ ] Numbers reach target values
  - [ ] Suffix displays correctly
  - [ ] Icons render properly
  - [ ] Intersection Observer triggers
  - [ ] Hover scale effect works

- [ ] **comparison_v2**
  - [ ] 2-column layout works
  - [ ] Red X icons on traditional side
  - [ ] Green checkmarks on modern side
  - [ ] "Recommended" badge displays
  - [ ] Gradient backgrounds render
  - [ ] Responsive stacking on mobile

- [ ] **cta_section_v2**
  - [ ] Badge displays
  - [ ] Title gradient renders
  - [ ] Primary button works
  - [ ] Secondary button works
  - [ ] Trust indicators display
  - [ ] Note text shows
  - [ ] Calendly integration (if applicable)

- [ ] **carousel_v2**
  - [ ] Images display
  - [ ] Captions render
  - [ ] Navigation works (if applicable)
  - [ ] Responsive on mobile

- [ ] **benefits_v2**
  - [ ] Icons display (FontAwesome)
  - [ ] Grid layout correct
  - [ ] Hover effects work
  - [ ] Badge displays
  - [ ] Responsive grid

- [ ] **gallery_v2**
  - [ ] Images load
  - [ ] Captions display
  - [ ] Grid layout works
  - [ ] Lightbox (if implemented)
  - [ ] Responsive grid

- [ ] **feature_grid_v2**
  - [ ] Grid layout correct
  - [ ] Icons display
  - [ ] Cards render properly
  - [ ] Responsive grid

- [ ] **feature_steps_v2**
  - [ ] Step numbers display
  - [ ] Icons render
  - [ ] Vertical flow correct
  - [ ] Responsive layout

- [ ] **related_auto**
  - [ ] URL lookup works
  - [ ] Fallback data works
  - [ ] Links are correct
  - [ ] Images display

### Functional Testing
- [ ] All CTAs link to correct URLs
- [ ] Calendly popup triggers when `url: "#"`
- [ ] External links open correctly
- [ ] FontAwesome icons load (check CDN)
- [ ] Images load (check paths)
- [ ] Animations trigger on scroll
- [ ] Hover states work on all interactive elements

### Cross-Browser Testing
- [ ] Chrome (desktop)
- [ ] Firefox (desktop)
- [ ] Safari (macOS)
- [ ] Safari (iOS)
- [ ] Chrome (Android)
- [ ] Edge

### Performance Testing
- [ ] Page load time < 3 seconds
- [ ] Images optimized
- [ ] CSS minified
- [ ] No console errors
- [ ] No 404s in network tab
- [ ] Lighthouse score > 90

---

## Phase 3: Component Fixes & Improvements

### Issues Found
Document any issues discovered during testing:

**Format:**
```
Component: [component_name]
Issue: [description]
Priority: [High/Medium/Low]
Fix: [solution or status]
```

### Known Issues to Address
- [ ] **modern_stats_v2**: Stats are hardcoded, not using YAML data
  - Priority: Medium
  - Fix: Modify template to use `section.stats` array

- [ ] **Custom components**: Need documentation
  - Components like `ai_capabilities`, `conversion_features` are custom
  - Priority: Low
  - Action: Document that these need custom template sections

### Improvements to Consider
- [ ] Add loading states for images
- [ ] Add error states for missing data
- [ ] Improve accessibility (ARIA labels)
- [ ] Add dark mode support
- [ ] Optimize animation performance
- [ ] Add lazy loading for images
- [ ] Add schema markup for components

---

## Phase 4: Component Library Expansion

### New Components to Create
Based on TODO.md insights and demo analysis:

- [ ] **migration_checklist_v2** - Step-by-step migration guide component
- [ ] **pricing_comparison_v2** - Pricing table comparison
- [ ] **integration_grid_v2** - Third-party integration showcase
- [ ] **roi_calculator_v2** - Interactive ROI calculator
- [ ] **use_case_tabs_v2** - Tabbed use case display
- [ ] **timeline_v2** - Implementation timeline
- [ ] **certification_badges_v2** - Security/compliance badges
- [ ] **video_embed_v2** - Optimized video embedding

### Components That Need V2 Versions
- [ ] **pilot_inclusions_v2** (currently only v1)
- [ ] **pilot_process_v2** (currently only v1)
- [ ] **qualification_criteria_v2** (currently only v1)

---

## Phase 5: SEO Optimization

### Component SEO Enhancements
- [ ] Add schema markup to testimonials_v2
- [ ] Add FAQ schema to faq_v2
- [ ] Optimize image alt tags
- [ ] Add proper heading hierarchy
- [ ] Ensure semantic HTML throughout
- [ ] Add breadcrumb schema

### Page-Level SEO
- [ ] Verify title tags (within first 50 lines)
- [ ] Verify meta descriptions (within first 50 lines)
- [ ] Add hreflang tags for multi-language
- [ ] Add canonical tags
- [ ] Test with Google Rich Results Test
- [ ] Submit to Search Console

---

## Phase 6: Migration Pages Implementation

Based on demo analysis (62% of demos mention migration):

### High Priority Migration Pages
- [ ] **/solutions/migrate-from-zendesk/**
- [ ] **/solutions/migrate-from-madcap-flare/**
- [ ] **/solutions/migrate-from-notion/**
- [ ] **/solutions/migrate-from-word/**
- [ ] **/solutions/migrate-from-confluence/**
- [ ] **/solutions/documentation-migration-services/**

### Component Requirements for Migration Pages
- [ ] **migration_checklist_v2** - For step-by-step guides
- [ ] **comparison_v2** - Already exists ✅
- [ ] **testimonials_v2** - Already exists ✅
- [ ] **timeline_v2** - New component needed
- [ ] **cta_section_v2** - Already exists ✅

---

## Phase 7: Testing Infrastructure

### Automated Testing
- [ ] Set up visual regression testing (Percy, Chromatic)
- [ ] Add link checker to CI/CD
- [ ] Add YAML validation
- [ ] Add HTML validation
- [ ] Add accessibility testing (axe)
- [ ] Add performance budgets

### Manual Testing Checklist
- [ ] Create browser testing matrix
- [ ] Document device testing requirements
- [ ] Create screenshot comparison process
- [ ] Document QA sign-off process

---

## Quick Reference: Generation Commands

```bash
# Generate all supplementary pages (v2 default)
python supplementary_site_generator.py

# Generate entire site (includes supplementary pages)
python main.py

# Test specific version
python supplementary_site_generator.py --v2
python supplementary_site_generator.py --v3

# Start dev server (port 8081)
sh start.sh

# Watch and auto-compile
sh auto_compile.sh
```

---

## Test Page URL

After generation, test page will be available at:
```
/solutions/ai/tacit-knowledge-capture/
```

Or locally:
```
http://localhost:8081/solutions/ai/tacit-knowledge-capture/
```

---

## Notes

- All V2 components use Tailwind CSS
- Components are self-contained (HTML + CSS in same directory)
- Generator copies CSS to `/styles/components/` during build
- Base template (`_base_v2.html`) loads component CSS files
- Custom components need custom template sections in `supplementary_page_v2.html`

---

## Questions to Answer

- [ ] Do all FontAwesome icons need to be predefined, or can we use any class?
- [ ] Is image optimization filter working correctly?
- [ ] Are there rate limits on Calendly popups?
- [ ] Should we add loading states for async content?
- [ ] What's the fallback if a component fails to render?
- [ ] Do we need component versioning beyond v2?
- [ ] Should we support custom CSS injection per page?
- [ ] What's the policy on external dependencies (fonts, icons)?

---

*Created: [Current Date]*
*Last Updated: [Current Date]*
*Next Review: After Phase 2 completion*
