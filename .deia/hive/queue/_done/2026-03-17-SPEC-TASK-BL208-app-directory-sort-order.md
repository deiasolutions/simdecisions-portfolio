# BL-208: App Directory should show unbuilt items below built items

## Objective
Update the App Directory (AppsHome) to sort EGGs so working/built items appear at the top and unbuilt/stub items appear below in a separate section.

## Context
The App Directory shows all EGGs in a flat list. Users want to see working apps first, with unbuilt/not-yet-working items in a lower "Coming Soon" or "In Development" section.

## Files to Read First
- `browser/src/primitives/apps-home/AppsHome.tsx`
- `browser/src/primitives/apps-home/AppCard.tsx`
- `browser/src/services/egg-registry/eggRegistryService.ts`
- `browser/scripts/copy-eggs.cjs`

## Deliverables
- [ ] Sort EGGs: working items first, then unbuilt/stub items
- [ ] Add visual section divider between "Available" and "Coming Soon"
- [ ] Status badges reflect actual build status (working/stub/broken)
- [ ] Tests for sort order and section grouping

## Acceptance Criteria
- [ ] Working EGGs appear above unbuilt EGGs
- [ ] Section headers or dividers separate the groups
- [ ] Status badges accurate
- [ ] Tests pass

## Smoke Test
- [ ] `cd browser && npx vitest run --reporter=verbose src/primitives/apps-home/`
- [ ] `cd browser && npx vitest run`

## Constraints
- No file over 500 lines
- CSS: var(--sd-*) only
- No stubs

## Model Assignment
haiku

## Priority
P0
