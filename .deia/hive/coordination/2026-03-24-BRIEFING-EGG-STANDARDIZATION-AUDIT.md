# BRIEFING: EGG Standardization Audit

**From:** Q33NR
**To:** Q33N
**Date:** 2026-03-24
**Priority:** P1

---

## Objective

Audit every EGG file in `eggs/` to determine what our "standard" app configuration is, identify bespoke deviations, and produce a report that will let us enforce consistency going forward.

## What To Do

### 1. Catalog Every EGG

Read every `*.egg.md` file in `eggs/`. For each one, extract:
- **Name** and purpose
- **Layout structure** (pane tree shape: splits, ratios, nesting)
- **Pane types used** (terminal, text-pane, tree-browser, canvas, chat, properties, etc.)
- **Adapter configs** per pane (which adapter, what settings)
- **Bus events** referenced (routeTarget, bus subscriptions, renderMode, etc.)
- **Special/unique features** that differ from other EGGs

### 2. Identify the Standard Pattern

From the catalog, determine:
- What is the **common baseline** layout most EGGs share? (e.g., sidebar + main area + terminal/chat split)
- What pane configs appear in **every** or **nearly every** EGG?
- What are the **standard adapter assignments** (e.g., tree-browser always uses filesystemAdapter in the sidebar)?
- What **bus wiring** is standard vs bespoke?

### 3. Flag Bespoke Deviations

For each EGG, list what it does differently from the standard pattern:
- Extra panes not in the standard layout
- Custom adapters
- Unusual ratios or split directions
- Unique bus events or routeTargets
- Missing standard panes (e.g., no terminal, no chat)

### 4. Check the Shell/Applet Infrastructure

Read these files to understand how EGGs are loaded and rendered:
- `browser/src/shell/` — how Shell consumes EGG layouts
- `browser/src/infrastructure/egg/` or wherever `eggLayoutToShellTree` lives
- `browser/src/apps/` — the adapter files (simAdapter, treeBrowserAdapter, sidebarAdapter, etc.)
- `vite.config.ts` — the `serveEggs()` plugin

Determine:
- Is there a "base EGG template" or shared layout fragment?
- If we change a standard pane config (e.g., update terminal defaults), how many EGGs would need manual updating?
- Could we extract shared config into a reusable fragment or template?

### 5. Produce the Report

Write a report to `.deia/hive/responses/20260324-EGG-STANDARDIZATION-AUDIT-RESPONSE.md` with:

1. **EGG Catalog Table** — every EGG with its layout structure, pane count, adapters
2. **Standard Pattern Definition** — the baseline config most EGGs share
3. **Deviation Matrix** — which EGGs deviate from standard and how
4. **Fragility Assessment** — if we change X in the standard, which EGGs break?
5. **Recommendations** — how to make EGGs inherit from a shared base so updates propagate automatically

## Files to Read First

- `eggs/*.egg.md` (all of them)
- `browser/src/shell/` (Shell.tsx or similar)
- `browser/src/infrastructure/egg/` (EGG parser/loader)
- `browser/src/apps/*.tsx` (adapter files)
- `vite.config.ts` (serveEggs plugin)

## Constraints

- This is a RESEARCH task. Do NOT modify any files.
- Do NOT write code.
- Do NOT dispatch bees.
- Write the report and return to Q33NR.
