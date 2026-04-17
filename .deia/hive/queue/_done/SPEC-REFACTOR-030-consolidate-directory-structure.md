---
id: REFACTOR-030
priority: P0
model: sonnet
role: bee
depends_on:
  - REFACTOR-023
---
# SPEC-REFACTOR-030: Consolidate Directory Structure per Stage/Set Pattern

## Priority
P0

## Model Assignment
sonnet

## Depends On
- REFACTOR-023

## Intent
Reorganize directory structure so the Stage/Set pattern is clean. Every primitive lives in `browser/src/primitives/`, every service in `services/`, every shell component in `shell/`. Remove orphan directories, consolidate scattered modules.

## Files to Read First
- `.deia/hive/refactor/FEATURE-MANIFEST.json` — what exists
- `.deia/hive/refactor/VALIDATION-BASELINE.json` — what works (don't break it)
- `browser/src/` — current structure
- `docs/specs/SPEC-EGG-FORMAT-v0.3.1.md` — target architecture

## Acceptance Criteria
- [ ] All primitives in `browser/src/primitives/` — no stray primitive-like components elsewhere
- [ ] All shell infrastructure in `browser/src/shell/`
- [ ] All services in `browser/src/services/`
- [ ] No orphan directories (empty dirs, dirs with only index files)
- [ ] All imports updated to reflect any moves
- [ ] TypeScript compiles: `npx tsc --noEmit` passes
- [ ] File created: `.deia/hive/refactor/changes-030.json` — list of every file moved/renamed

## Constraints
- You are in EXECUTE mode. Make the changes. Do NOT enter plan mode.
- PRESERVE ALL FUNCTIONALITY — if unsure about a move, don't move it
- Update all imports after any file relocation
- Commit changes to `refactor/auto-2026-04-07` branch
- No file over 500 lines
