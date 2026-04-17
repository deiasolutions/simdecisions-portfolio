# Global Commons — DEIA Public Documentation

**Version:** 1.0.0
**Date:** 2026-03-17
**Status:** Phase A (Static Content)

---

## What is This?

Global Commons is the public-facing documentation and governance reference for DEIA (Distributed, Ethical, Intelligence Architecture). This repository makes DEIA's constitutional framework, ethics configuration, carbon methodology, and design system visible and auditable by anyone.

## Documents

### Foundation
- **[index.md](index.md)** — Landing page: What is DEIA? What is Global Commons?

### Governance Framework
- **[governance.md](governance.md)** — Constitutional framework: ethics → governance → execution
- **[ethics.md](ethics.md)** — Ethics framework: forbidden actions, escalation triggers, grace periods
- **[carbon.md](carbon.md)** — Carbon methodology: model energy estimates, budgets, grace periods

### Design System
- **[design-tokens.md](design-tokens.md)** — CSS design tokens (default theme)
- **[design-tokens-themes.md](design-tokens-themes.md)** — Theme variants (depth, light, monochrome, high-contrast)

## Build & Deploy Instructions

### Static Site Hosting

Global Commons is pure static content — no build step required. Deploy to any static hosting provider.

**Recommended hosts:**
- GitHub Pages
- Netlify
- Vercel
- CloudFlare Pages

### Deploy Steps

1. **Clone or copy** the `docs/global-commons/` directory to your hosting provider.
2. **Set index.md** as the landing page (or create an HTML redirect to it).
3. **No build step required** — all files are plain markdown.

### Future: Markdown Rendering

Phase A is static markdown. Future phases may add:
- Markdown → HTML conversion (using a static site generator)
- Search functionality
- Navigation UI
- Dynamic content (API documentation, live carbon tracking)

For now: these files are meant to be read as markdown in a code editor or rendered via GitHub/GitLab.

## File Paths

All paths in this documentation reference the ShiftCenter repository structure:

```
C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\
  .deia/
    config/
      ethics-default.yml
      carbon.yml
      grace.yml
  browser/
    src/
      shell/
        shell-themes.css
  docs/
    global-commons/
      (this directory)
```

## Contribution Guidelines

Global Commons documents **actual implemented behavior**. Do not add speculative features or future plans.

**When updating:**
1. Changes to `ethics-default.yml` → update `ethics.md`
2. Changes to `carbon.yml` or `grace.yml` → update `carbon.md`
3. Changes to `shell-themes.css` → update `design-tokens.md` and `design-tokens-themes.md`
4. Changes to governance logic → update `governance.md`

**Traceability:** Every statement must be traceable to actual config files or code.

## License

Global Commons content is public domain. Share freely.

## Contact

- **Project:** ShiftCenter (DEIA implementation)
- **Repository:** [github.com/your-org/shiftcenter](https://github.com/your-org/shiftcenter) (update with actual URL)
- **Website:** deiasolutions.org (Phase A: static content only)
