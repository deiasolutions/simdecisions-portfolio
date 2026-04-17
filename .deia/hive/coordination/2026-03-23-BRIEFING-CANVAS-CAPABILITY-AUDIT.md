# BRIEFING: Canvas Capability Audit — Old Platform vs New ShiftCenter

**Date:** 2026-03-23
**From:** Q33NR
**To:** Q33N
**Priority:** HIGH — Q88N wants this NOW

## Objective

Produce a definitive, side-by-side capability comparison of the OLD canvas system (platform repo) vs the NEW flow-designer/sim system (shiftcenter repo). "I don't know" is not acceptable for any capability question. Every feature must be verified by reading actual source code.

## What Q88N Needs

A single consolidated report answering:
1. What modes did the old canvas have? (design, simulate, playback, tabletop, compare — or different?)
2. What modes does the new flow-designer have? Which ones actually work end-to-end?
3. Full node type comparison (old 17 vs new 4-6 — name every type)
4. What features exist in old but NOT in new? (regressions)
5. What features exist in new but NOT in old? (genuinely new)
6. Is 35,625 lines justified vs the old 4,927? What accounts for the 7.2x expansion?
7. Which new components are wired end-to-end vs. UI shells with no backend?

## Repos

- **Old platform:** `C:\Users\davee\OneDrive\Documents\GitHub\platform`
  - Canvas likely in: `src/efemera/components/canvas/` or `simdecisions-2/src/`
  - DES engine likely in: `src/efemera/des/`
  - Look for: mode switching, node types, simulation integration, properties panels

- **New shiftcenter:** `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter`
  - Flow designer: `browser/src/apps/sim/components/flow-designer/`
  - Sim adapter: `browser/src/apps/simAdapter.tsx`
  - EGGs: `eggs/canvas.egg.md`, `eggs/canvas2.egg.md`, `eggs/sim.egg.md`
  - DES routes: `hivenode/routes/des_routes.py`

## Dispatch Plan

Write 3 task files:
- **BEE-CA1:** Audit OLD platform canvas — every mode, every node type, every feature, line counts per subsystem. Read the actual source files, don't guess.
- **BEE-CA2:** Audit NEW shiftcenter flow-designer — every mode, every node type, every component. For each: is it wired to a backend or just UI? Line counts per subsystem.
- **BEE-CA3:** Write the consolidated comparison report. Reads BEE-CA1 and BEE-CA2 response files, produces the final side-by-side table.

BEE-CA1 and BEE-CA2 run in parallel. BEE-CA3 runs after both complete.

## Model Assignment

All three bees: **sonnet** (research depth needed)

## Constraints

- READ ONLY. No code changes. No file modifications.
- Every claim must cite a specific file path and line range.
- No "likely" or "probably" — verify or state "NOT FOUND after searching X, Y, Z."
- Response files go to `.deia/hive/responses/`
