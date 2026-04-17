# BRIEFING: SimDecisions Applet Wiring

**From:** Q33NR
**To:** Q33N
**Date:** 2026-03-15
**Status:** EXECUTE

---

## Objective

Wire up the existing SimDecisions flow designer into the ShiftCenter shell as a launchable applet. All major components exist (121 frontend files, DES engine, API routes). This spec connects the last-mile pieces.

## Spec Location

Read the full spec: `docs/specs/2026-03-15-0100-SPEC-simdecisions-applet-wiring.md`

It has three phases:
1. **Shell integration** — simAdapter.tsx + sim.egg.md + APP_REGISTRY entry (browser-only)
2. **Engine wiring** — connect SimulationEngine to the 503-stub routes in sim.py
3. **Tests** — adapter mount, EGG resolution, engine lifecycle, unskip blocked tests

## Task Breakdown Guidance

Split into bee-sized tasks by phase:
- **T1:** simAdapter.tsx + sim.egg.md + registerApp (Phase 1, small)
- **T2:** Engine integration in sim.py — wire SimulationEngine to all endpoints (Phase 2, medium)
- **T3:** Tests for all three phases (Phase 3, medium)

Phase 1 must work independently — frontend loads even if backend is down (uses LocalDESEngine fallback).

## Key Files

All listed in the spec under "Key Files to Read First". The adapter pattern to follow is `browser/src/apps/canvasAdapter.tsx` (32 lines). The EGG pattern is `eggs/code.egg.md`.

## Model Assignment

- T1: haiku (small, pattern-following)
- T2: sonnet (engine integration, needs to understand DES engine API)
- T3: sonnet (cross-cutting tests)

## Constraints

- Do NOT rewrite existing sim components — wrap and wire only
- Do NOT modify `engine/des/` core files — only import and call from routes
- No file over 500 lines
- CSS: `var(--sd-*)` only
- No stubs

## After Completion

Write task files to `.deia/hive/tasks/`. Return to Q33NR for review before dispatching bees.
