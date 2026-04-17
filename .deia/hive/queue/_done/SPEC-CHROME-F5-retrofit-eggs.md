# CHROME-F5: Retrofit All Existing EGGs

## Objective
Retrofit all 21 existing .egg.md files to the new layout-composition format. Replace hide* flags with actual chrome primitives in the layout tree. Replace single-float ratios with array ratios where multi-child splits are needed. Add chrome primitives (top-bar, status-bar) to EGGs that need them.

## Build Type
**Retrofit** — Edit all 21 existing .egg.md files to new format. Replace hide* flags with layout composition. Replace single-float ratios with array ratios where needed. Add chrome primitives to layout trees. No new code — editing existing EGG config files.

## Problem Analysis
18 of 21 EGGs use old single-float ratios and boolean hide* flags. The ADR requires a clean break: no inflater shim for old format. All EGGs must be manually retrofitted. Chrome visibility is now determined by whether the layout tree includes the corresponding primitive — not by boolean flags.

Key EGGs to retrofit:
- apps.egg.md: hideMenuBar, hideStatusBar, hideTabBar, hideActivityBar
- constitution.egg.md: hideMenuBar, hideStatusBar, hideTabBar, hideActivityBar
- hodeia.egg.md: hideMenuBar, hideStatusBar, hideTabBar, hideActivityBar
- sim.egg.md: devOverride: false
- code.egg.md: devOverride: false
- All EGGs with masterTitleBar: replace with top-bar primitive in layout

## Files to Read First
- eggs/apps.egg.md
- eggs/chat.egg.md
- eggs/code.egg.md
- eggs/canvas.egg.md
- eggs/canvas2.egg.md
- eggs/efemera.egg.md
- eggs/sim.egg.md
- eggs/constitution.egg.md
- eggs/hodeia.egg.md
- docs/specs/ADR-SC-CHROME-001-v3.md

## Files to Modify
- eggs/apps.egg.md
- eggs/chat.egg.md
- eggs/chat-full.egg.md
- eggs/code.egg.md
- eggs/canvas.egg.md
- eggs/canvas2.egg.md
- eggs/constitution.egg.md
- eggs/efemera.egg.md
- eggs/hodeia.egg.md
- eggs/home.egg.md
- eggs/kanban.egg.md
- eggs/login.egg.md
- eggs/monitor.egg.md
- eggs/playground.egg.md
- eggs/primitives.egg.md
- eggs/processing.egg.md
- eggs/sim.egg.md
- eggs/turtle-draw.egg.md
- eggs/build-monitor.egg.md

## Deliverables
- [ ] All EGGs use new ui block format (chromeMode, commandPalette, akk only)
- [ ] All hide* flags removed, replaced by layout composition
- [ ] All devOverride flags removed
- [ ] EGGs that had chrome (menu bar, status bar) include corresponding primitives in layout tree
- [ ] EGGs that hid chrome simply don't include the primitive
- [ ] Array ratios used for multi-child splits where chrome primitives added
- [ ] masterTitleBar replaced with top-bar primitive in layout

## Acceptance Criteria
- [ ] Every .egg.md passes the new inflater validation (no old flags)
- [ ] All EGGs produce correct layout when loaded
- [ ] No EGG uses devOverride, hideMenuBar, hideStatusBar, hideTabBar, or hideActivityBar
- [ ] Existing EGG tests updated to match new format
- [ ] Visual layout equivalent to previous version

## Test Requirements
- [ ] Tests written FIRST (TDD) — before implementation
- [ ] Test file: browser/src/eggs/__tests__/eggRetrofit.test.ts
- [ ] Test: each retrofitted EGG passes inflater validation
- [ ] Test: chat.egg.md produces correct 3-pane layout with top-bar
- [ ] Test: canvas2.egg.md produces correct layout with chrome primitives
- [ ] Test: code.egg.md produces correct layout without devOverride
- [ ] Test: apps.egg.md produces correct layout without hide* flags
- [ ] Test: no EGG contains devOverride or hide* flags (lint test)
- [ ] All tests pass
- [ ] Minimum 8 tests

## Smoke Test
- [ ] cd browser && npx vitest run src/eggs — all EGG tests pass
- [ ] cd browser && npx vitest run — full suite passes

## Constraints
- No file over 500 lines
- No stubs
- Each EGG must produce equivalent visual layout to its previous version
- Clean break — no backward compatibility shim

## Depends On
- SPEC-CHROME-A1 (multi-child splits for chrome panes in layout)
- SPEC-CHROME-B1 (top-bar registered)
- SPEC-CHROME-B2 (menu-bar registered)
- SPEC-CHROME-B3 (status-bar registered)
- SPEC-CHROME-B4 (tab-bar registered)
- SPEC-CHROME-B5 (bottom-nav registered)
- SPEC-CHROME-C3 (docked toolbar appType available for layout composition)

## Model Assignment
sonnet

## Priority
P2
