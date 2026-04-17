---
id: REFACTOR-032
priority: P0
model: sonnet
role: bee
depends_on:
  - REFACTOR-031
---
# SPEC-REFACTOR-032: Wire EGG Loading — Stage Loads Set, Set Loads Primitives

## Priority
P0

## Model Assignment
sonnet

## Depends On
- REFACTOR-031

## Intent
Ensure the full Stage → Set → Primitive loading pipeline works end to end. The shell reads a .set.md config, resolves each primitive reference to a React component, and renders the layout. This is the core architectural pattern that must be operational.

## Files to Read First
- `browser/src/services/shell/eggResolver.ts` — current resolution logic
- `browser/src/shell/components/ShellNodeRenderer.tsx` — how primitives render
- `browser/src/shell/` — shell infrastructure
- `eggs/*.set.md` — configs to load
- `.deia/hive/refactor/changes-031.json` — what changed in previous spec

## Acceptance Criteria
- [ ] EGG resolver can parse any .set.md and return a structured config
- [ ] Shell can take that config and render the correct primitives in the correct layout
- [ ] At least 3 different .set.md products load and render without errors:
  - `home.set.md`
  - `workdesk.set.md`
  - One other (kanban, editor, or efemera)
- [ ] Missing primitive references produce a clear error, not a crash
- [ ] File created: `.deia/hive/refactor/changes-032.json`

## Constraints
- You are in EXECUTE mode. Make the changes. Do NOT enter plan mode.
- Commit changes to `refactor/auto-2026-04-07` branch
