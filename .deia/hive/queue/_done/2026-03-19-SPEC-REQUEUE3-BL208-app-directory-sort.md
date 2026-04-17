# BL-208 (RE-QUEUE 3): App directory — sort working EGGs above stubs

## Background — Why Re-Queued
Previous re-queue (attempt 2) was dispatched but fix cycle failed due to _active/ path reference bug (now fixed). Original issue: AppsHome.tsx has category grouping (core/tools/fun) but does NOT sort working EGGs above stub/unbuilt EGGs within those groups.

## Objective
Sort EGGs so working/built items appear above unbuilt/stub items. Add a visual "Coming Soon" section or badge for stub EGGs.

## Current State
- `AppsHome.tsx` groups EGGs into sections: core, tools, fun (via SECTION_ORDER)
- EGG metadata includes `_stub: true/false` field in frontmatter
- No sort-by-status logic exists — stubs and working EGGs are mixed

## What Needs to Happen
1. Within each section, sort: working EGGs first, then stubs
2. Add visual indicator for stub EGGs (badge, opacity, or "Coming Soon" label)
3. Optionally: separate "Coming Soon" subsection below working items

## Files to Read First
- `browser/src/primitives/apps-home/AppsHome.tsx` (current grouping logic)
- `browser/src/primitives/apps-home/AppCard.tsx` (card rendering)
- `browser/src/services/egg-registry/eggRegistryService.ts` (where _stub field comes from)
- `eggs/canvas.egg.md` (_stub: false example)
- Any egg with `_stub: true` for reference

## Files to Modify
- `browser/src/primitives/apps-home/AppsHome.tsx` — add sort-by-status within sections

## Deliverables
- [ ] Within each section, working EGGs sort above stub EGGs
- [ ] Stub EGGs have visual indicator (badge/opacity/label)
- [ ] Tests for sort order (working before stubs)
- [ ] No regressions in apps-home tests

## Smoke Test
- [ ] `cd browser && npx vitest run --reporter=verbose src/primitives/apps-home/`
- [ ] `cd browser && npx vitest run`

## Constraints
- No file over 500 lines
- CSS: var(--sd-*) only
- No stubs (ironic)
- MUST modify AppsHome.tsx sort logic

## Model Assignment
sonnet

## Priority
P0
