# Repository Guidelines

## Project Structure & Module Organization
Core site templates live in `src/`; top-level pages sit in folders while reusable includes remain `_*.html` so the build keeps `<title>` and meta tags within the first 50 lines. Static assets belong in `assets/` and `static/` (edit SCSS in `static/scss/style.scss`). Multilingual resources live in `locale/` alongside `translation_config.yaml` and `site_config.yaml`. Blog output and caches reside in `blog/`, while Search Console tooling and reports sit in `gsc_reports/`.

## Site & Blog Build Pipelines
Install dependencies with `pip install -r requirements.txt`. Run `python main.py` to re-render English pages and `sh start.sh` to preview on `http://localhost:8081`. Use `python translate_and_build.py --quick` for rapid multilingual builds or `./build_multilingual.sh --quick` before releases to include YAML extraction and supplementary pages. Blog updates run through `python .external/BlogVi/run_blog_gen.py blog --force --all-ai`; follow with `blog/translate_all_languages.sh` (or `translate_remaining_languages.sh`) when refreshing cached translations.

## Coding Style & Naming Conventions
Adhere to PEP 8 with four-space indentation, `snake_case` helpers, pathlib, and f-strings. Keep scripts idempotent; heavy lifting belongs in modules. Jinja templates extend the appropriate `_base*.html`, use `{% trans %}` blocks, and source hreflang/canonical markup from shared partials. Static assets follow kebab-case filenames; prefix new includes with `_` so `CustomSite` treats them as partials.

## Testing & Verification
Validate changes manually. After site edits, run `python main.py` or the quick multilingual workflow and confirm generated HTML keeps SEO tags near the top, adds no 404s, and respects `site_config.yaml`. For BlogVi work, inspect `blogvi.log`, confirm `.translation_cache/<lang>/` gained expected JSON files, and spot-check regenerated `blog/articles/*/index.html`. When touching analytics, execute `python test_gsc_integration.py` and record any Search Console follow-up.

## Commit & Pull Request Guidelines
Use imperative, single-line summaries (`Fix hreflang map for glossary ru`). Bodies stay under 72 characters per line and list regenerated commands (`python main.py`, `translate_and_build.py --quick`, BlogVi scripts). PRs must call out affected locales, rebuilt directories, SEO verification steps, and any follow-up TODO items. Attach screenshots for layout or design shifts.

## SEO, Localization & Analytics Checks
Preserve canonical tags, hreflang matrices, and `<html lang>` accuracy—reuse `_hreflang.html` helpers and keep translations in sync with `site_config.yaml`. BlogVi translations already add canonical/hreflang metadata; if you filter languages, ensure the full list still renders. Monitor critical TODOs: prevent 404 regressions, keep image optimization on the roadmap, and address zero-click pages highlighted in `gsc_reports/TODO.md`. Before merging, skim newly rendered pages for structured data issues, confirm glossary/comparison modules still emit schema, and note any Search Console resubmission required.
