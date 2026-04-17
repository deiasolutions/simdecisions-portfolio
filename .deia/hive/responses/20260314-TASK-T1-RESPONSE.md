---
features_delivered:
  - APPS-HOME-EGG-001: apps-home.egg.md EGG definition
features_modified: []
features_broken: []
test_summary:
  total: 0
  passed: 0
  failed: 0
---

# TASK-T1: Create apps-home.egg.md -- COMPLETE

**Status:** COMPLETE
**Model:** Sonnet
**Date:** 2026-03-14

## Files Modified

**Created:**
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\eggs\apps-home.egg.md` (60 lines)

## What Was Done

- Created `apps-home.egg.md` EGG file with schema_version 3
- Added complete frontmatter with all required fields (egg, version, schema_version, displayName, description, author, defaultRoute, license, _stub)
- Created layout block with single pane using `"type": "pane"` (not "app")
- Configured apps-home appType with sections config (core, productivity, platform) and showSearch enabled
- Added UI block with minimal chrome (hideMenuBar: true, hideTabBar: true, hideActivityBar: true, hideStatusBar: false)
- Added tabs block with single tab definition
- Added permissions block with localStorage access and allowed network domains
- Added settings block with defaultView: grid
- Verified file is 60 lines (under 100-line limit)
- No external asset references (only localhost and hivenode.railway.app domains)
- No stub sections, no TODO comments

## Test Results

No tests required for this task. This is a pure EGG definition file (YAML frontmatter + markdown + JSON blocks). The file is served statically by Vite's publicDir config and parsed at runtime by the shell's `useEggInit` hook.

Testing will occur at integration level when the apps-home appType component consumes this EGG file.

## Build Verification

**Vite build:** Not run. This is a static EGG definition file served from `../eggs/` publicDir. No build step required.

**Vitest:** Not run. No testable code in this deliverable.

The file will be validated at runtime by:
1. `useEggInit.ts` hook parsing the EGG file
2. `eggToShell.ts` transforming layout to shell state
3. Apps-home appType component reading the config

## Acceptance Criteria

- [x] Valid `.egg.md` with correct frontmatter (all required fields, schema_version 3)
- [x] Layout block uses `"type": "pane"` and is valid JSON
- [x] UI block matches minimal chrome pattern (hideMenuBar: true, hideTabBar: true, hideActivityBar: true)
- [x] No external asset references (only localhost and hivenode.railway.app allowed domains)
- [x] File is under 100 lines (60 lines total)

All acceptance criteria met.

## Clock / Cost / Carbon

**Clock:** 2 minutes (file creation + verification)
**Cost:** ~$0.02 (2 Read, 2 Write, 1 Bash command)
**Carbon:** Negligible (< 0.1g CO2e)

## Issues / Follow-ups

**None.** File is complete and ready for integration.

**Dependencies:**
- Task T2 must create the `apps-home` appType component in `browser/src/apps/home/` to render this EGG
- Task T3 must update dispatch routing to recognize `/apps` route

**Edge cases handled:**
- Used `"type": "pane"` as specified (not `"type": "app"`)
- Followed exact permission structure from spec (localStorage: true, sessionStorage: false)
- Matched UI chrome settings from spec precisely

**Recommended next tasks:**
- T2 (apps-home component)
- T3 (dispatch routing)
- Integration test to verify EGG parsing and rendering
