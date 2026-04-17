---
id: REFACTOR-031
priority: P0
model: sonnet
role: bee
depends_on:
  - REFACTOR-030
---
# SPEC-REFACTOR-031: Ensure All Products Are .set.md Configs

## Priority
P0

## Model Assignment
sonnet

## Depends On
- REFACTOR-030

## Intent
Every product/app must be defined by a `.set.md` config in `eggs/`, not by hardcoded React components. Any app that currently bypasses the EGG/Set system (e.g., standalone eggs in STANDALONE_EGGS map in App.tsx) should be converted to proper .set.md configs that load through the standard pipeline.

## Files to Read First
- `eggs/*.set.md` — existing set files
- `browser/src/App.tsx` — STANDALONE_EGGS map, applyBranding, routing
- `browser/src/services/shell/eggResolver.ts` — EGG resolution
- `.deia/hive/refactor/test-results-sets.json` — which sets currently work
- `docs/specs/SPEC-EGG-FORMAT-v0.3.1.md` — format spec

## Acceptance Criteria
- [ ] Every app route in App.tsx backed by a .set.md config
- [ ] STANDALONE_EGGS map reduced or eliminated where possible
- [ ] Each .set.md has valid frontmatter matching EGG schema
- [ ] Each .set.md references only primitives that exist in `browser/src/primitives/`
- [ ] File created: `.deia/hive/refactor/changes-031.json` — changes made

## Constraints
- You are in EXECUTE mode. Make the changes. Do NOT enter plan mode.
- Do NOT remove working standalone apps that can't yet be expressed as set configs — convert what you can, note what you can't
- Commit changes to `refactor/auto-2026-04-07` branch
