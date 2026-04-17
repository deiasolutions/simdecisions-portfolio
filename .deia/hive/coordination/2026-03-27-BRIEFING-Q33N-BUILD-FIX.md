# BRIEFING: Fix Vercel Production Build — Commit Missing Bee Source Files

**From:** Q33NR
**To:** Q33N
**Date:** 2026-03-27
**Priority:** P0 — Production is broken

## Situation

The Vercel production build is failing. The bee auto-commit script (`auto_commit.py`) committed only `monitor-state.json` changes for Chrome ADR Wave B/C/D specs — NOT the actual source files the bees created. The missing files have been restored from git stash to the working tree and the build passes locally.

## What Happened

1. Chrome ADR Waves A-F dispatched 36 bee specs
2. Auto-commit script committed state changes but missed untracked source files
3. `index.ts` imports components that don't exist in git (MenuBarPrimitive, TopBar, StatusBar, etc.)
4. Vercel deploy fails: `Could not resolve "../primitives/menu-bar/MenuBarPrimitive"`

## Current State

- **Branch:** `dev` (also merged to `main` — both broken)
- **Build:** Passes locally after stash restore
- **Files restored from stash but NOT committed:**

### Missing Primitives (restored)
- `browser/src/primitives/menu-bar/` (MenuBarPrimitive.tsx, .css, tests)
- `browser/src/primitives/top-bar/` (TopBar.tsx, .css, index.ts, tests)
- `browser/src/primitives/status-bar/` (StatusBar.tsx, .css, tests)
- `browser/src/primitives/command-palette/` (CommandPalette.tsx, .css, fuzzyMatch.ts, tests)
- `browser/src/primitives/bottom-nav/` (BottomNav.tsx, .css, tests)
- `browser/src/primitives/toolbar/` (FloatingToolbar, DockedToolbar, ToolbarManager, useDrag, types, tests)

### Missing Adapters/Services (restored)
- `browser/src/apps/bottomNavAdapter.tsx`
- `browser/src/apps/toolbarAdapter.tsx`
- `browser/src/services/icons/iconResolver.ts`
- `browser/src/services/hivenodeUrl.ts`
- `browser/src/services/settings/settingsSync.ts`
- `browser/src/primitives/auth/SetupWizard.tsx`, `.css`, `setupDetector.ts`
- `browser/src/infrastructure/relay_bus/rtdEmitter.ts`

### Missing Shell Components (restored)
- `browser/src/shell/components/BottomSheet.tsx`
- `browser/src/shell/components/GestureLayer.tsx`
- `browser/src/shell/components/SlideoverPanel.tsx`
- `browser/src/shell/__tests__/reducer.dirty.test.ts`
- `browser/src/eggs/__tests__/eggToolbar.test.ts`
- `browser/src/apps/sim/services/layout/align.ts`

### Missing Backend (restored)
- `hivenode/preferences/` (store.py, __init__.py)
- `hivenode/routes/preferences.py`
- `hivenode/sync/outbox.py`
- `hodeia_auth/dependencies.py`, `routes/mfa_setup.py`, `routes/profile.py`, `routes/recovery_email.py`
- `tests/` for all the above
- `_tools/stop.py`
- `docs/specs/ADR-SC-CHROME-001-v2.md`, `ADR-SC-CHROME-001-v3.md`

## Your Mission

1. **Verify build passes** — run `npm run build` in `browser/`
2. **Run browser tests** — `npx vitest run` in `browser/`
3. **Run backend tests** — `python -m pytest tests/ -x -q`
4. **Commit all restored files** on dev branch
   - Commit message: `fix: commit missing bee source files (auto-commit bug)`
5. **Merge dev to main**
6. **Push both branches**
7. **Verify Vercel deploy succeeds** — check `npx vercel ls`
8. **Add chat.shiftcenter.com domain** — `npx vercel domains add chat.shiftcenter.com`
9. **Report back** with deploy status

## Q88N Authorization

Git commit, merge, and push are **PRE-APPROVED** for this mission. Build fix is urgent.

## Files to Read First

- `browser/src/apps/index.ts` (the file with all the imports that were breaking)
- `vercel.json` (rewrite rules including chat.shiftcenter.com)
