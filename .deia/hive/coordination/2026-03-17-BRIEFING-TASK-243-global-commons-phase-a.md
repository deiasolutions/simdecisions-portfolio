# BRIEFING: TASK-243 — Global Commons Phase A

**From:** Q33NR (Queen Regent)
**To:** Q33N (Queen Coordinator)
**Date:** 2026-03-17
**Source Spec:** `docs/specs/WAVE-5-SHIP.md` — Task 5.4
**Priority:** P2
**Model:** Sonnet

---

## Objective

Create the static content foundation for Global Commons at deiasolutions.org. This is Wave 5 (Ship) Task 5.4: "Global Commons Phase A: static content at deiasolutions.org (Federalist Papers, design tokens, ethics.yml defaults)."

**What is Global Commons?**

Global Commons is the public-facing documentation and governance reference for DEIA. It makes the constitutional framework visible and auditable by anyone. Phase A is static content only — no dynamic features, no database, no backend.

---

## Context

### What Exists Now

1. **Ethics configuration:** `.deia/config/ethics-default.yml` (21 lines) — Default ethics template (ADR-014)
2. **Carbon methodology:** `.deia/config/carbon.yml` (44 lines) — Carbon budgets and model energy estimates (ADR-015)
3. **Grace configuration:** `.deia/config/grace.yml` (20 lines) — Grace period configuration for gate dispositions (ADR-014)
4. **Design tokens:** `browser/src/shell/shell-themes.css` (756 lines) — All `--sd-*` CSS variables across 4 themes (default, depth, light, monochrome, high-contrast)

### What Needs to Happen

Create `docs/global-commons/` directory with 5 markdown files:

1. **index.md** — Landing page. What is DEIA? What is Global Commons? Links to all documents.
2. **ethics.md** — Human-readable version of `ethics-default.yml`. Explain each field, what it does, why it exists.
3. **design-tokens.md** — Document all `--sd-*` CSS variables. Include descriptions, default values, and usage patterns.
4. **carbon.md** — Human-readable version of `carbon.yml`. Explain the carbon methodology, model energy estimates, regional intensity, budgets.
5. **governance.md** — How the constitutional framework works: ethics → governance → execution. This is the "Federalist Papers" — the philosophical foundation.

Plus a `README.md` with build/deploy instructions.

---

## Requirements

### Content Quality

- **Factual:** Derived from actual config files and code. Do NOT invent governance rules or philosophical positions. If something is not documented in the code, do not claim it exists.
- **Clear:** Written for strangers. No internal jargon without definition.
- **Complete:** Every field in ethics.yml, carbon.yml, grace.yml should be explained.
- **Useful:** Design tokens should show real examples (which components use which variables).

### File Structure

```
docs/global-commons/
├── README.md          # Build/deploy instructions
├── index.md           # Landing page
├── ethics.md          # Ethics framework
├── carbon.md          # Carbon methodology
├── design-tokens.md   # CSS variable reference
└── governance.md      # Constitutional framework
```

### No Tests Required

This is a documentation-only task. TDD does not apply. No tests needed.

### File Limit

Each markdown file should stay under 500 lines. If `design-tokens.md` would exceed 500 lines (likely, given 756 lines of CSS), split into:
- `design-tokens.md` (overview + default theme)
- `design-tokens-themes.md` (depth, light, monochrome, high-contrast)

---

## Files to Reference

- `.deia/config/ethics-default.yml` — 21 lines
- `.deia/config/carbon.yml` — 44 lines
- `.deia/config/grace.yml` — 20 lines
- `browser/src/shell/shell-themes.css` — 756 lines (CSS variables)
- `docs/specs/WAVE-5-SHIP.md` — Wave 5 task list

---

## Constraints

1. **No code.** This is pure markdown documentation.
2. **No dynamic features.** Static content only. No APIs, no database, no React components.
3. **No fabrication.** If governance rules are not documented in the codebase, do not invent them. Document what exists.
4. **File paths must be absolute** in task files.
5. **Hard Rule 4:** No file over 500 lines. Modularize if needed.

---

## Deliverables

Your task file(s) should specify:

- [ ] Create `docs/global-commons/` directory
- [ ] Write `README.md` with build/deploy instructions
- [ ] Write `index.md` (landing page)
- [ ] Write `ethics.md` (explain ethics-default.yml)
- [ ] Write `carbon.md` (explain carbon.yml + grace.yml)
- [ ] Write `design-tokens.md` (document all CSS variables, split if >500 lines)
- [ ] Write `governance.md` (constitutional framework — the "Federalist Papers")
- [ ] All content derived from actual config files and code
- [ ] All file paths absolute

---

## Success Criteria

After bees complete:

1. `docs/global-commons/` exists with all 6+ files
2. Every field in ethics-default.yml is explained in ethics.md
3. Every field in carbon.yml and grace.yml is explained in carbon.md
4. All CSS variables from shell-themes.css are documented in design-tokens.md (or split files)
5. governance.md explains the constitutional framework (ethics → governance → execution)
6. index.md provides a clear landing page with links
7. README.md provides build/deploy instructions
8. No file exceeds 500 lines

---

## Next Steps

1. Write task file(s) for this work
2. Return to Q33NR for review
3. After Q33NR approval, dispatch bee(s)
4. Review bee response files
5. Report to Q33NR

---

## Notes

- This is **Wave 5 (Ship)** work. The product must be ready for strangers.
- Global Commons is a public-facing artifact. Quality matters.
- This is the foundation for deiasolutions.org — the place where DEIA governance becomes auditable.
- Estimated effort: 2 hours (from WAVE-5-SHIP.md)

---

**Q33N: Please write task file(s) for this work and return for my review before dispatching bees.**
