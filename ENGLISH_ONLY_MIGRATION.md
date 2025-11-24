# English-Only Migration - November 23, 2025

## 🎯 Executive Summary

On November 23, 2025, we made the strategic decision to **abandon the multilingual blog strategy** and **301 redirect all 3,107 non-English blog articles to their English equivalents**. This document serves as the canonical reference for this decision and its implementation.

## 📊 Business Justification

### The Problem
- **3,107 translated articles** across 16 languages
- **High CTR** (4-5x better than English)
- **Zero revenue** - no demo bookings from foreign language traffic

### The Reality
- **Actual buyers**: English-speaking enterprise consultants (SAP, Workday, Salesforce implementers)
- **Revenue data**: Russian article with 41 clicks = $0 revenue vs. English article with 1 click = $9K deal
- **Demo bookings**: 100% from English-speaking traffic

### Strategic Conclusion
Foreign language traffic was **vanity metrics**. English traffic drives **all revenue**.

---

## 🛠️ Implementation Details

### Infrastructure Change
**From**: Cloudflare (failed - Bulk Redirects didn't work on FREE plan)
**To**: AWS Route53 + CloudFront Functions

### CloudFront Function Code
```javascript
function handler(event) {
    var request = event.request;
    var uri = request.uri;

    // 16 languages to redirect
    var languages = [
        'da', 'de', 'es', 'fr', 'hu', 'it', 'ja', 'ko',
        'nl', 'pl', 'pt-br', 'pt-pt', 'ru', 'sv', 'tr', 'zh'
    ];

    // Pattern 1: /blog/{lang}/* → /blog/*
    for (var i = 0; i < languages.length; i++) {
        var lang = languages[i];
        var pattern = '/blog/' + lang + '/';

        if (uri.indexOf(pattern) === 0) {
            var newUri = uri.replace(pattern, '/blog/');
            return {
                statusCode: 301,
                statusDescription: 'Moved Permanently',
                headers: {
                    'location': { value: 'https://www.docsie.io' + newUri },
                    'cache-control': { value: 'max-age=31536000' }
                }
            };
        }
    }

    // Pattern 2: /blog/{lang} → /blog/
    for (var i = 0; i < languages.length; i++) {
        var lang = languages[i];
        if (uri === '/blog/' + lang || uri === '/blog/' + lang + '/') {
            return {
                statusCode: 301,
                statusDescription: 'Moved Permanently',
                headers: {
                    'location': { value: 'https://www.docsie.io/blog/' },
                    'cache-control': { value: 'max-age=31536000' }
                }
            };
        }
    }

    return request;
}
```

### Redirect Pattern
- **From**: `/blog/{lang}/articles/{slug}/` (16 languages × ~190 articles each)
- **To**: `/blog/articles/{slug}/` (English)
- **Status**: 301 Permanent
- **Cache**: 1 year

### Affected URLs
- **3,107 translated blog articles**
- **16 language blog homepages** (`/blog/{lang}/`)
- **~480 category pages** across all languages

---

## 📁 File Structure Changes

### What We KEPT
Translation files remain on GitHub Pages:
```
/blog/da/
/blog/de/
/blog/es/
/blog/fr/
... (all 16 languages)
```

**Why?**
- CloudFront redirects happen at edge (before GitHub Pages)
- No need to delete files (Google will naturally deindex)
- Preserves history if we ever need to reference

### What We CHANGED
1. **Sitemap** - Remove all non-English URLs
2. **Hreflang tags** - Remove all except `hreflang="en"` from English articles
3. **Language attributes** - Ensure `<html lang="en">` on English content

---

## 📈 Expected Impact

### Short-term (Weeks 1-4)
- ❌ **Traffic DROP**: ~40% (lose foreign language clicks)
- ✅ **English CTR UP**: No more cannibalization from translations
- ✅ **Impressions down**: Google stops showing non-English pages in SERPs
- ⏳ **Deindexing begins**: Foreign URLs start disappearing from Google

### Medium-term (Months 2-3)
- ✅ **Authority consolidation**: English articles gain SEO juice from all 16 languages
- ✅ **Better rankings**: Enterprise keywords (SAP, Workday, documentation) rank higher
- ✅ **More qualified demos**: English-speaking enterprise buyers find us
- ✅ **Reduced tech debt**: No more translation quality issues

### Long-term (Months 6+)
- ✅ **Revenue increase**: More demos = more $9K deals
- ✅ **Faster development**: No translation maintenance burden
- ✅ **Cleaner analytics**: All traffic in one language = easier to analyze

---

## ✅ Implementation Checklist

### Phase 1: Infrastructure (Nov 23, 2025)
- [x] Move DNS from Cloudflare to AWS Route53
- [x] Create CloudFront distribution pointing to GitHub Pages
- [x] Deploy CloudFront Function with 16-language redirect logic
- [x] Update Route53 A record to point to CloudFront

### Phase 2: BlogVi Updates (This Week)
- [ ] Update sitemap generation to exclude non-English URLs
  - File: `.external/BlogVi/src/blog_vi/core/landing.py`
  - Change: Only output `/blog/articles/*` URLs (no `/blog/{lang}/*`)
- [ ] Remove hreflang tags from English article template
  - File: `/blog/templates/article.html`
  - Keep only: `<link rel="alternate" hreflang="en" href="..." />`
  - Remove: All other language hreflang tags
- [ ] Ensure `<html lang="en">` on English articles
  - File: `/blog/templates/article.html`
  - Verify: `<html lang="en">` not `<html lang="{{ language }}">`

### Phase 3: Google Search Console (Week 2)
- [ ] Submit updated English-only sitemap
  - URL: `https://www.docsie.io/blog/sitemap.xml`
  - Remove: All `/blog/{lang}/*` URLs
- [ ] Monitor deindexing of foreign URLs
  - Check GSC Coverage report weekly
  - Expect 2-4 weeks for full deindexing

### Phase 4: Monitoring (Ongoing)
- [ ] Week 1-2: Track traffic drop (expect ~40%)
- [ ] Week 3-4: Monitor English CTR improvement
- [ ] Month 2-3: Measure demo booking increase
- [ ] Month 6: Analyze revenue impact

---

## 🔍 Monitoring & Success Metrics

### Week 1-2 (Nov 23 - Dec 7, 2025)
**Track:**
- Total blog traffic (expect drop)
- English article CTR (expect improvement)
- GSC Coverage: "Excluded" count for non-English URLs
- Demo bookings from blog (baseline)

### Week 3-4 (Dec 8 - Dec 21, 2025)
**Track:**
- English content position improvements
- Foreign URL deindexing progress
- Demo booking trend

### Month 2-3 (Jan-Feb 2026)
**Track:**
- English article rankings for enterprise keywords
- Demo booking increase %
- Revenue from blog-sourced demos

### Month 6+ (Apr 2026)
**Decision Point:**
- Delete foreign language files if fully deindexed
- Document final ROI analysis
- Create case study for BlogVi

---

## 🎓 Key Learnings

### What We Learned
1. **CTR ≠ Revenue**: High engagement means nothing without conversions
2. **Know Your Buyer**: B2B SaaS buyers are English-speaking enterprise consultants
3. **Consolidation > Distribution**: Better to dominate one language than spread thin across 17
4. **Technical Debt Kills Velocity**: 3,107 translations crushed development speed
5. **Vanity Metrics Are Dangerous**: Foreign traffic looked good in analytics but generated $0

### What We'd Do Differently
1. **Start with buyer research**: Who actually pays? What language do they speak?
2. **Test before translating**: Translate 1-2 articles per language, measure conversions
3. **Revenue tracking from day 1**: Connect analytics to demo bookings to revenue
4. **Question assumptions**: "More languages = more traffic = more revenue" was FALSE

### Advice for Other BlogVi Users
**Before translating your blog:**
1. Who are your buyers? (Not readers, BUYERS)
2. What language do they transact in?
3. Can you track conversions by language?
4. Is the ROI worth the technical debt?

**For B2B SaaS specifically:**
- Enterprise buyers are often English-speaking
- Technical documentation readers ≠ decision makers
- Focus on content quality in one language over quantity in many

---

## 📝 References

### Documentation Updated
- `/Users/philippetrounev/PycharmProjects/docsie-site/CLAUDE.md`
- `/Users/philippetrounev/PycharmProjects/docsie-site/.external/BlogVi/CLAUDE.md`
- `/Users/philippetrounev/PycharmProjects/docsie-site/TODO.md` (this section added)
- `/Users/philippetrounev/PycharmProjects/docsie-site/.external/BlogVi/TODO.md` (this section added)
- `/Users/philippetrounev/PycharmProjects/docsie-site/gsc_reports/TODO.md` (monitoring section added)

### CloudFront Function
- **Location**: AWS Console → CloudFront → Functions
- **Name**: `docsie-blog-language-redirects`
- **Associated Distribution**: CloudFront distribution for www.docsie.io

### Original Multilingual Setup (Archived)
- Translation cache: `.translation_cache/{language}/{slug}.json` (preserved)
- Translation count: 3,107 articles across 16 languages
- Languages: da, de, es, fr, hu, it, ja, ko, nl, pl, pt-br, pt-pt, ru, sv, tr, zh

---

## 🚀 Future Considerations

### Potential BlogVi Feature
Add `english_only_mode` configuration option:

```yaml
# settings.yaml
english_only_mode: true  # Disables translations, removes hreflang, English-only sitemap
```

**What it would do:**
- Skip translation generation entirely
- Remove all hreflang tags except `en`
- Generate English-only sitemap
- Add warning if translation files detected
- Provide migration guide

### If We Ever Go Multilingual Again
**Requirements before retranslating:**
1. Proof that foreign language buyers exist and convert
2. Demo booking tracking by language
3. Revenue attribution by content language
4. Dedicated translation budget and quality control
5. Clear ROI threshold (e.g., "Must generate 10 demos/month to justify")

---

**Date**: November 23, 2025
**Decision Maker**: Product Team
**Implementation**: AWS CloudFront Functions
**Status**: ✅ Live in Production
**Next Review**: April 2026 (6-month post-mortem)
