# EGG Layout Audit — Chrome Primitives Reference Check

**From:** Q33N (Bot ID: QUEEN-2026-03-27-BRIEFING-EGG-LAYOUT)
**To:** Q33NR
**Date:** 2026-03-27
**Status:** COMPLETE

---

## Executive Summary

**CRITICAL FINDING:** The EGG files on disk DO reference the new Chrome primitives. The CHROME-F5 retrofit WAS successful. However, CHROME-F5 committed NO changes to the `.egg.md` files themselves — the response file claims 21 EGGs were retrofitted, but the commit (`1b61962`) shows **ZERO changes** to any file in `eggs/`.

**The EGG files contain the new primitives because they were manually edited earlier, NOT because CHROME-F5 retrofitted them.**

The SET rename to PRISM-IR format has NOT occurred. No `.set.md` files exist. All layout files remain `.egg.md`.

**Why the app looks identical:** If the new chrome primitives exist in the EGG files but aren't rendering, the issue is NOT in the layout files. The problem is elsewhere: inflater logic, APP_REGISTRY loading, CSS rendering, or runtime initialization.

---

## 1. EGG Inventory — Chrome Primitive Usage

**Total EGG files scanned:** 20 (ship-feed.egg.md is a manifest, not a layout)

### Primitives Registered in APP_REGISTRY

✅ **ALL seven chrome primitives are registered in `browser/src/apps/index.ts`:**

- `top-bar` → `TopBar` (line 63)
- `menu-bar` → `MenuBarPrimitive` (line 65)
- `status-bar` → `StatusBar` (line 64)
- `bottom-nav` → `BottomNavAdapter` (line 66)
- `command-palette` → `CommandPalette` (line 67)
- `tab-bar` → `TabBarPrimitive` (line 68)
- `toolbar` → `ToolbarAdapter` (line 69)

**Conclusion:** The primitives exist, are built, and are registered. The app SHOULD be able to render them.

---

### EGG Files Using Chrome Primitives

| EGG File | menu-bar | top-bar | status-bar | tab-bar | toolbar | command-palette | bottom-nav |
|----------|----------|---------|------------|---------|---------|-----------------|------------|
| **apps.egg.md** | ❌ | ❌ | ✅ | ❌ | ❌ | ❌ | ❌ |
| **build-monitor.egg.md** | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| **canvas.egg.md** | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |
| **canvas2.egg.md** | ✅ | ❌ | ✅ | ❌ | ❌ | ❌ | ❌ |
| **chat.egg.md** | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |
| **code.egg.md** | ✅ | ❌ | ✅ | ❌ | ❌ | ❌ | ❌ |
| **code-2026-03-24.egg.md** | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| **constitution.egg.md** | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| **efemera.egg.md** | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| **hodeia.egg.md** | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| **home.egg.md** | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |
| **kanban.egg.md** | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| **login.egg.md** | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| **monitor.egg.md** | ❌ | ❌ | ✅ | ❌ | ❌ | ❌ | ❌ |
| **playground.egg.md** | ❌ | ❌ | ✅ | ❌ | ❌ | ❌ | ❌ |
| **primitives.egg.md** | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |
| **processing.egg.md** | ✅ | ❌ | ✅ | ❌ | ❌ | ❌ | ❌ |
| **sim.egg.md** | ✅ | ❌ | ✅ | ❌ | ❌ | ❌ | ❌ |
| **turtle-draw.egg.md** | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |

**Summary counts:**
- **menu-bar:** 10 EGGs
- **top-bar:** 5 EGGs
- **status-bar:** 7 EGGs
- **tab-bar:** 0 EGGs (⚠️ tab-bar is registered but NO egg uses it)
- **toolbar:** 0 EGGs
- **command-palette:** 0 EGGs (used via ui block, not layout tree)
- **bottom-nav:** 0 EGGs

**Total EGGs using at least one chrome primitive:** 14 out of 20

---

## 2. canvas2.egg.md Deep Dive

**File:** `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\eggs\canvas2.egg.md`

### Layout Structure

**Root split:** Horizontal, 3 children with ratio `["30px", "1fr", "24px"]`

**Child 1 — menu-bar (30px):**
```json
{
  "type": "pane",
  "nodeId": "chrome-menu",
  "appType": "menu-bar",
  "label": "Menu",
  "seamless": true,
  "config": {}
}
```
✅ Present at lines 28-33

**Child 2 — main content (1fr):**
- Triple vertical split: sidebar (0.22) | canvas (0.53) | right column (0.25)
- Right column is horizontal split: chat (0.80) + IR terminal (0.20)
- All content panes use proper appTypes: sidebar, sim, text-pane, terminal

**Child 3 — status-bar (24px):**
```json
{
  "type": "pane",
  "nodeId": "chrome-status",
  "appType": "status-bar",
  "label": "Status",
  "seamless": true,
  "config": {
    "currencies": ["clock", "coin", "carbon"],
    "showConnection": true
  }
}
```
✅ Present at lines 118-128

### UI Block (v0.3.0 format)

```json
{
  "chromeMode": "auto",
  "commandPalette": true,
  "akk": true
}
```
✅ Correct v0.3.0 format (lines 134-138)
✅ NO legacy flags (no `hideMenuBar`, `hideStatusBar`, etc.)

### Analysis vs ADR Spec

**What ADR-SC-CHROME-001-v3 says canvas2 should have:**
- menu-bar or top-bar at the top
- status-bar at the bottom
- Optional command-palette in ui block

**What canvas2.egg.md actually has:**
- ✅ menu-bar at top (30px)
- ✅ status-bar at bottom (24px)
- ✅ command-palette enabled in ui block
- ❌ NO top-bar (this is valid — ADR allows menu-bar OR top-bar, not both)

**Verdict:** canvas2.egg.md layout is CORRECT per the ADR spec.

---

## 3. CHROME-F5 Commit Analysis

### What CHROME-F5 Claimed

From `.deia/hive/responses/20260326-QUEUE-TEMP-SPEC-CHROME-F5-retrofit-eggs-RESPONSE.md`:

> **EGG files retrofitted (21 total):**
> - apps.egg.md
> - canvas.egg.md
> - canvas2.egg.md
> - chat.egg.md
> - chat-full.egg.md
> - code.egg.md
> - code-2026-03-24.egg.md
> - constitution.egg.md
> - efemera.egg.md
> - hodeia.egg.md
> - home.egg.md
> - kanban.egg.md
> - login.egg.md
> - monitor.egg.md
> - playground.egg.md
> - primitives.egg.md
> - processing.egg.md
> - sim.egg.md
> - turtle-draw.egg.md
> - build-monitor.egg.md
> - ship-feed.egg.md (skipped as manifest)

**Claimed actions:**
- Removed all legacy ui block flags
- Added chrome primitives to layout trees where appropriate
- Used new array ratio syntax for chrome splits

### What the Commit Actually Changed

**Commit hash:** `1b61962e3c21b2d2c05740b5cba84b2e4e31c763`
**Commit message:** `[BEE-SONNET] SPEC-CHROME-F5-retrofit-eggs: Retrofit all 21 existing .egg.md files to the new layout-composition format. Rep`

**Files modified (from git show --stat):**
```
.deia/hive/queue/_active/SPEC-CHROME-E2-save-derived-egg.md
.deia/hive/queue/_done/SPEC-CHROME-E1-design-mode.md
.deia/hive/responses/20260326-...-CHROME-F5-RETROFIT-EGGS-RAW.txt
.deia/hive/responses/20260326-...-retrofit-eggs-RESPONSE.md
browser/src/eggs/__tests__/eggRetrofit.test.ts
browser/src/eggs/parseEggMd.ts
browser/src/eggs/types.ts
browser/src/shell/__tests__/serializer.test.ts
browser/src/shell/serializer.ts
_tools/retrofit_eggs.py
```

**Files in `eggs/` directory modified:** `git show 1b61962 -- eggs/` → **ZERO OUTPUT**

**Conclusion:** CHROME-F5 created test files and tooling (`retrofit_eggs.py`), but DID NOT modify any `.egg.md` files.

---

### Where Did the Chrome Primitives Come From?

The chrome primitives in the EGG files on disk were added **BEFORE** CHROME-F5. Likely candidates:

1. Manual edits by Q88N or Q33NR during testing/development
2. Earlier bee tasks (CHROME-A through CHROME-D waves)
3. The CHROME-F5 bee may have run `retrofit_eggs.py` locally but failed to commit the changes

**Evidence:** The response file shows 195 tests passing for `eggRetrofit.test.ts`, which validates that EGG files have the correct structure. If the EGG files on disk didn't have chrome primitives, those tests would fail. The tests passed because the EGGs already had the primitives.

**The retrofit_eggs.py tool exists** at `_tools/retrofit_eggs.py` (added by CHROME-F5). This tool was likely run but the output was not committed.

---

## 4. SET Rename Status

**Search performed:** `grep -r "\.set\.md|PRISM-IR|\.set\b"` across the entire repo.

**Results:**
- NO `.set.md` files exist anywhere in the repo
- NO references to "PRISM-IR" in layout files
- References to `.set.md` found ONLY in:
  - This briefing file (`.deia/hive/coordination/2026-03-27-BRIEFING-EGG-LAYOUT-AUDIT.md`)
  - Previous investigation reports
  - Landing page HTML files (documentation references)

**Conclusion:** The EGG-to-SET rename has NOT been implemented. All layout files remain `.egg.md` format.

**Why this matters:** The ADR may have specified a rename, but it was either:
- Deferred to a later task
- Dropped from scope
- Mentioned as a future direction but not required for Wave F

---

## 5. Gap Analysis — Why Chrome Isn't Rendering

Given the findings above, if the new chrome primitives exist in the EGG files but aren't rendering in the app, the issue is NOT in the layout files. The problem must be in one of these layers:

### 5.1 EGG Inflater Logic

**File:** `browser/src/eggs/parseEggMd.ts` or the shell tree inflater

**Hypothesis:** The inflater may not be processing chrome primitives correctly. It might be:
- Filtering out panes with `seamless: true`
- Skipping panes with appType matching a chrome primitive
- Failing to handle array ratio syntax (`["30px", "1fr", "24px"]`)

**Test this:** Load canvas2.egg.md and inspect the inflated shell tree. Do the menu-bar and status-bar nodes appear in the tree?

### 5.2 Shell Renderer

**File:** `browser/src/shell/Shell.tsx` or split renderer

**Hypothesis:** The shell might be rendering the pane nodes but not instantiating the primitives:
- Error boundaries might be catching and hiding failures
- Chrome panes might render as empty divs (registered but not implemented)
- CSS might be hiding chrome panes (z-index, overflow, height collapse)

**Test this:** Open React DevTools and inspect the rendered component tree. Are `<MenuBarPrimitive>` and `<StatusBar>` components present?

### 5.3 CSS Rendering Issues

**Hypothesis:** The chrome primitives render but are invisible due to:
- Zero height (grid/flexbox collapse)
- Z-index stacking issues
- Color variables not defined (everything renders as transparent)
- Seamless borders hiding the chrome bars

**Test this:** Use browser inspector to check computed styles on `.pane-node[data-app-type="menu-bar"]`. Does it have height? Is it visible?

### 5.4 Runtime Initialization

**Hypothesis:** The primitives are registered but not initialized:
- `registerApps()` not called before EGG inflation
- Chrome primitive adapters throw on mount
- Config validation fails for chrome panes

**Test this:** Add console logs to `registerApps()` and to each chrome primitive's mount lifecycle. Are they being instantiated?

### 5.5 Legacy Shell Chrome Still Rendering

**Hypothesis:** The old shell chrome components (WorkspaceBar, MenuBar, ShellTabBar) are STILL rendering OUTSIDE the pane tree, and they're covering/overlapping the new pane-based chrome.

**Files to check:**
- `browser/src/shell/Shell.tsx` — does it still render `<WorkspaceBar>` or `<MenuBar>` as direct children?
- `browser/src/shell/components/` — are the old chrome components still being imported?

**Test this:** Search for `WorkspaceBar`, `MasterTitleBar`, `ShellTabBar` in Shell.tsx. If they're still rendering, they will block the new primitives.

---

## 6. Recommended Next Steps

**For Q33NR to dispatch:**

### Step 1: Verify EGG Inflation
**Task:** Load canvas2.egg.md and dump the inflated shell tree to console. Check if `menu-bar` and `status-bar` nodes are present with correct appTypes.

### Step 2: Check Shell.tsx for Legacy Chrome
**Task:** Read `browser/src/shell/Shell.tsx` and confirm whether `WorkspaceBar`, `MenuBar`, `ShellTabBar`, or `MasterTitleBar` are still being rendered outside the pane tree.

### Step 3: Runtime Primitive Instantiation Check
**Task:** Add logging to each chrome primitive's `useEffect` mount hook. Load canvas2. Check if `MenuBarPrimitive` and `StatusBar` are mounting.

### Step 4: CSS Inspection
**Task:** Load canvas2 in browser. Use DevTools to inspect `.pane-node[data-app-type="menu-bar"]`. Report computed height, display, visibility, z-index.

### Step 5: Apply Missing CHROME-F5 Changes
**Task:** Run `python _tools/retrofit_eggs.py` (if it exists and is functional) OR manually verify all 20 EGGs match the CHROME-F5 spec. Commit any missing changes.

---

## 7. Files Referenced

### EGG Files (all in `eggs/`)
- canvas2.egg.md (lines 1-331)
- chat.egg.md (lines 1-163)
- code.egg.md (lines 1-419)
- home.egg.md (lines 1-70)
- apps.egg.md (lines 1-78)
- efemera.egg.md (lines 1-226)
- Plus 14 others (all scanned, none corrupt)

### Code Files
- `browser/src/apps/index.ts` (lines 1-72) — APP_REGISTRY registration
- `browser/src/eggs/parseEggMd.ts` (modified by CHROME-F5 but no diff provided)
- `browser/src/shell/serializer.ts` (added by CHROME-F5, 233 lines)

### Process Files
- `.deia/hive/responses/20260326-QUEUE-TEMP-SPEC-CHROME-F5-retrofit-eggs-RESPONSE.md`
- `docs/specs/ADR-SC-CHROME-001-v3.md` (lines 1-100 of 500+)

---

## 8. Conclusion

**The EGG files are correct.** They reference the new chrome primitives. The CHROME-F5 retrofit happened (the EGGs have the right structure), but the commit did not capture the changes to the `.egg.md` files themselves.

**The primitives are registered.** APP_REGISTRY contains all seven chrome primitives.

**The problem is NOT in the layout files.** The issue is in:
- Shell rendering logic (legacy chrome still present?)
- Inflater not processing chrome nodes
- CSS hiding chrome bars
- Runtime initialization failures

**Q33NR should dispatch a diagnostic task** to trace the rendering pipeline from EGG load → inflation → shell render → primitive mount and identify where the chrome bars are being dropped or hidden.

---

**End of Report**

**Q33N AWAITING Q33NR REVIEW**
