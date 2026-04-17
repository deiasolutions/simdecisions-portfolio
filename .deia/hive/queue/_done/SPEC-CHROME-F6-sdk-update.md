# CHROME-F6: SDK-APP-BUILDER v0.3.0 Update

## Objective
Update the SDK-APP-BUILDER documentation to v0.3.0 covering: new ui block, layout primitives (top-bar, menu-bar, status-bar, bottom-nav, tab-bar, toolbar, command-palette), toolbar fenced block, slideover meta, multi-child ratio syntax, pane lifecycle events, dirty tracking, and design mode.

## Build Type
**Documentation** — Write SDK-APP-BUILDER v0.3.0 documentation. Plus validation tests for JSON examples in the doc.

## Problem Analysis
The EGG SDK documentation must be updated to reflect all changes from this ADR. EGG authors need to know the new layout composition model, how to declare chrome primitives, the ratio syntax, slideover configuration, toolbar blocks, lifecycle events, and design mode. The old ui block flags (hide*, devOverride) must be documented as removed with migration guidance.

## Files to Read First
- docs/specs/ADR-SC-CHROME-001-v3.md
- browser/src/eggs/types.ts

## Files to Modify
- docs/specs/SDK-APP-BUILDER-v0.3.0.md — NEW documentation

## Deliverables
- [ ] Complete SDK v0.3.0 documentation
- [ ] New ui block format (chromeMode, commandPalette, akk)
- [ ] Chrome primitive reference (all 7 appTypes with config schemas)
- [ ] Multi-child ratio syntax reference (px + fr units, sugar → IR)
- [ ] Slideover meta fields reference
- [ ] Toolbar fenced block reference
- [ ] Pane lifecycle events reference
- [ ] Dirty tracking API (pane:dirty-changed)
- [ ] Design mode behavior
- [ ] Migration guide from v0.2.0 (removed flags, new composition model)

## Acceptance Criteria
- [ ] SDK document covers all ADR sections
- [ ] Migration guide clearly maps old flags to new composition patterns
- [ ] All JSON examples valid and consistent with implementation
- [ ] Reference layouts from ADR Sections 17-18 included

## Test Requirements
- [ ] Tests written FIRST (TDD) — before implementation
- [ ] Test file: browser/src/eggs/__tests__/sdkExamples.test.ts
- [ ] Test: each JSON example from SDK doc parses without error
- [ ] Test: each example inflates to valid EggIR
- [ ] Test: reference layout from Section 17 produces correct shell tree
- [ ] All tests pass
- [ ] Minimum 3 tests

## Smoke Test
- [ ] cd browser && npx vitest run src/eggs/__tests__/sdkExamples — tests pass

## Constraints
- Documentation only (plus validation tests for examples)
- No file over 500 lines — split into sections if needed

## Depends On
- SPEC-CHROME-F1 (legacy chrome deleted)
- SPEC-CHROME-F2 (legacy flags removed)
- SPEC-CHROME-F5 (all EGGs retrofitted)

## Model Assignment
haiku

## Priority
P3
