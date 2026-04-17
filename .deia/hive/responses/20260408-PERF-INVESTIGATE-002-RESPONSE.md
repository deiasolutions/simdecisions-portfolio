# TASK-PERF-INVESTIGATE-002: Deep Trace of Browser Performance Issue on Set Load -- COMPLETE

**Status:** COMPLETE
**Model:** Sonnet 4.5
**Date:** 2026-04-08
**Role:** Q33N (Queen — research only)

---

## Executive Summary

After a full trace of the `?set=code` load path and systematic search for recurring work patterns, I found **NO CONFIRMED CAUSE** of continuous CPU usage that would make the browser unresponsive.

The previous investigation's assumption about ResizeObservers was **unverified speculation**. This investigation traced the actual execution paths and found:

- ResizeObservers are used correctly with guards and cleanup
- setInterval timers are all gated, throttled, or conditional
- No render cascades or circular event loops detected
- Load sequence is linear with no recurring work during idle state

**The problem is likely NOT in the code patterns examined.** The issue may be:
1. A runtime-only problem (profiler needed)
2. Browser extension interference
3. A specific primitive not in the trace (Monaco editor bundle loading)
4. Memory leak from session state accumulation (not detectable from code alone)

---

## Full Load Trace (Step by Step)

### Phase 0: Module Load (before React render)
**File:** `browser/src/main.tsx`

1. **registerApps()** — Synchronous registration of 38 app adapters
   - No side effects, just function registration
   - Runs once, stores references in APP_REGISTRY map

2. **Import CSS** — `shell-themes.css`, `cloud-theme.css`
   - Synchronous CSS parsing
   - No recurring work

3. **Service Worker registration** (hodeia.app only)
   - Async, fire-and-forget
   - Not relevant to shiftcenter.com

**Result:** No recurring work. Runs once and stops.

---

### Phase 1: App Component Mount
**File:** `browser/src/App.tsx`

1. **extractTokenFromUrl()** — Module-level function (runs once before React)
   - Parses JWT from URL query/hash
   - Stores in authStore
   - Cleans URL via `history.replaceState`
   - **Async call:** `claimDeviceData()` (fire-and-forget, not awaited)

2. **applyBranding()** — Module-level function (runs once)
   - Sets favicon and title based on hostname
   - No listeners, no recurring work

3. **resolveCurrentEgg()** — Synchronous
   - Reads window.location, returns 'code'
   - No side effects

4. **Render check:** Is it a standalone page?
   - `STANDALONE_EGGS['code']` → undefined
   - Not standalone, continues to `<ShellApp />`

**Result:** No recurring work. All synchronous or fire-and-forget.

---

### Phase 2: useEggInit Hook (ShellApp mount)
**File:** `browser/src/shell/useEggInit.ts`

**useEffect runs once (empty deps []):**

1. **resolveCurrentEgg()** → 'code'
2. **loadEggFromMarkdown('/code.set.md')** — Async fetch
   - Parses YAML front-matter
   - Parses layout JSON block
   - Returns EggIR object
3. **Auth gate check:**
   - localhost → bypass
   - Not localhost + auth required → try `tryRefreshToken()`
   - If fails → show AuthGate (early return, no shell render)
4. **eggToShellState(eggIR.layout)** — Synchronous tree transformation
   - Converts EGG layout JSON to ShellState tree
   - Pure function, no side effects
5. **wireEgg(eggIR)** — Async, registers commands/permissions
   - Registers away config (if present)
   - Registers command shortcuts
   - **No polling, no intervals started here**
6. **runStartup(eggIR.startupConfig)** — Async, fire-and-forget
   - Loads default documents (e.g., welcome.md)
   - Async fetch, not blocking render

**Result:** useEffect runs once, does NOT re-run. No recurring work.

---

### Phase 3: Shell Component Mount
**File:** `browser/src/shell/components/Shell.tsx`

**useEffect hooks (analyzed for recurring work):**

1. **Line 62-73: shell.settings command registration**
   - Runs once, registers command
   - Returns cleanup (unregister)
   - No recurring work

2. **Line 76-103: Temp file recovery prompt**
   - Runs once on mount
   - Reads localStorage to check for temp files
   - Shows dialog if found
   - No recurring work

3. **Line 142-153: Viewport resize listener (chromeMode='auto' ONLY)**
   - **Guard:** `if (state.chromeMode !== 'auto') return;`
   - Adds resize listener to recalculate chromeMode
   - **For 'code' set:** chromeMode is NOT 'auto' (defaults to 'auto' but may be set by EGG)
   - **Effect:** Listener MAY be added, but only dispatches on resize events (user-initiated)
   - **NOT continuous:** Only fires when user resizes window

4. **Line 156-164: Chrome mode transition detector**
   - Runs on resolvedChromeMode change
   - Dispatches once when mode changes
   - NOT continuous

5. **Line 200-239: Auto-undock slideovers on small viewport**
   - Adds resize listener
   - Scans tree for docked slideovers, undocks if viewport < minDockWidth
   - **NOT continuous:** Only fires on user resize events

6. **Line 242-254: Bus subscription for pane:dirty-changed**
   - Subscribes to bus messages
   - Only fires when panes emit dirty-changed events
   - NOT continuous

7. **Line 256-273: beforeunload handler (dirty flag)**
   - Only adds listener when layoutDirty or contentDirtyPanes is true
   - NOT continuous

**Result:** No continuous work. All listeners are event-driven (resize, bus messages). None poll.

---

### Phase 4: ShellNodeRenderer — Pane Mount Cascade
**File:** `browser/src/shell/components/ShellNodeRenderer.tsx`

For EACH AppNode in the tree (sidebar, editor, terminal, top-bar, menu-bar, status-bar):

**ResizeObserver #1 (lines 119-136):**
- **Guard:** `if (node.type !== 'app' || !(node as AppNode).sizeStates || !ref.current) return;`
- **Only runs if:** Node has sizeStates config (rare)
- **Callback:** Reads height, computes size state, dispatches if changed
- **Termination:** Has early exit — `if (newState !== appNode.currentSizeState)` prevents infinite loop
- **Cleanup:** `observer.disconnect()` on unmount
- **Verdict:** SAFE. Guarded, has termination condition, cleans up.

**ResizeObserver #2 (lines 139-165):**
- **Guard:** `if (node.type !== 'app' || !ref.current || typeof ResizeObserver === 'undefined') return;`
- **Runs for:** ALL app nodes (sidebar, editor, terminal, chrome bars)
- **Callback:** Reads bounding rect, dispatches `UPDATE_LAYOUT_DIMENSIONS`
- **Dispatch:** On EVERY resize callback
- **Termination:** None — always dispatches
- **Cleanup:** `observer.disconnect()` on unmount

**SUSPICIOUS BUT UNVERIFIED:**
- This ResizeObserver fires on every layout change for every app node
- If dispatch causes re-render → layout change → observer fires → dispatch → loop
- **Cannot verify from code alone** — need to check if `UPDATE_LAYOUT_DIMENSIONS` dispatch causes re-layout
- **Likely safe because:** Dispatch updates Redux state (dimensions map), which doesn't trigger CSS recalc unless a component reads it and changes layout

**useEffect: Bus subscription for drag events (lines 91-116):**
- Subscribes to '*' (all bus messages)
- Filters for DRAG_START / DRAG_END
- Only updates local state (isDragActive, canAccept)
- NOT continuous

**Result:** ResizeObservers are present but guarded and cleaned up. Second observer is potentially problematic IF `UPDATE_LAYOUT_DIMENSIONS` causes re-layout, but cannot confirm from code.

---

### Phase 5: Primitives Loaded by Code Set
**From:** `eggs/code.set.md`

**Panes created:**
1. **top-bar** (chrome, appType: top-bar)
2. **menu-bar** (chrome, appType: menu-bar)
3. **sidebar** (appType: sidebar)
   - Embeds: **file-explorer** (TreeBrowserAdapter)
4. **text** (appType: text) — Monaco editor
5. **terminal** (appType: terminal) — Fr@nk terminal
6. **status-bar** (chrome, appType: status-bar)

**TreeBrowser (sidebar → file-explorer):**
**File:** `browser/src/primitives/tree-browser/TreeBrowser.tsx`

- **ResizeObserver (lines 37-47):**
  - **Guard:** `if (manualCollapsed !== undefined) return;` — Manual override takes precedence
  - **Guard:** `if (typeof ResizeObserver === 'undefined' || !containerRef.current) return;`
  - **Callback:** `setAutoCollapsed(entry.contentRect.width < collapseThreshold);`
  - **Only updates state if width crosses threshold**
  - **Cleanup:** `observer.disconnect()`
  - **Verdict:** SAFE. Guarded, threshold-based update, cleans up.

**Result:** TreeBrowser ResizeObserver is SAFE.

---

### Phase 6: setInterval Usage Audit

**Files with setInterval (18 total):**

1. **buildMonitorAdapter.tsx (lines 209, 225, 265)**
   - Line 225: Polls `/build/status` every 10s
   - Line 265: Live timer for running tasks (updates every 1s)
   - **Guard:** Only starts if connected to hivenode
   - **Cleanup:** `clearInterval` on unmount
   - **Relevant to 'code' set?** NO — build-monitor is not in code.egg.md
   - **Verdict:** NOT ACTIVE during code set load

2. **autosave.ts (line 35)**
   - Autosave timer, 60-second interval
   - **Guard:** Must call `startAutosave()` to activate
   - **Search:** No call to `startAutosave()` in Shell or useEggInit
   - **Verdict:** NOT ACTIVE by default

3. **awayManager.ts (line 104)**
   - Idle detection, checks every 5 seconds
   - **Guard:** Must call `startIdleTracking()` to activate
   - **Search:** Where is it called?
   - **File:** `browser/src/services/away/awayManager.ts`
   - **Call site:** NOT found in Shell, useEggInit, or App
   - **Likely:** Started by away config from EGG wireEgg()
   - **Verdict:** MAY be active if code.egg.md has away config (line 430-439 shows away block)
   - **Frequency:** 5 seconds
   - **Work:** Checks `Date.now() - lastActivityMs`, updates state if threshold crossed
   - **Cost:** Minimal (one timestamp comparison)

4. **PaneLoader.tsx (line 15)**
   - Spinner animation, 150ms interval
   - **Only renders:** When pane is in loading state
   - **For HOT panes:** Not rendered
   - **Verdict:** NOT ACTIVE after panes load

5. **Other setInterval occurrences (notifications, collaboration, sim-specific)**
   - Not relevant to code.egg.md

**Confirmed Active Intervals:**
- **awayManager idle check:** Every 5 seconds (if started)
- **Cost:** Negligible (timestamp comparison)

**Result:** Minimal active intervals. None polling network or triggering heavy work.

---

## Confirmed Causes

**NONE.**

No code pattern found that provably causes continuous CPU usage during idle state after set load.

---

## Likely Causes

### 1. Away Manager Idle Tracking (Low Probability)
**Evidence:**
- `code.egg.md` has away config (lines 430-439)
- `wireEgg()` likely starts idle tracking
- Interval runs every 5 seconds

**Counter-Evidence:**
- Work is trivial (timestamp comparison)
- No layout changes, no DOM manipulation
- Throttled activity listeners (1-second throttle)

**Likelihood:** 10% — Too lightweight to cause unresponsiveness

---

### 2. ResizeObserver Cascade (Medium Probability)
**Evidence:**
- `ShellNodeRenderer.tsx` lines 139-165: ResizeObserver dispatches `UPDATE_LAYOUT_DIMENSIONS` on every resize
- If dispatch causes re-render → layout change → observer fires → loop

**Counter-Evidence:**
- Dispatch updates Redux state (dimensions map)
- No component in trace reads dimensions and triggers layout change
- Would need Chrome DevTools Performance profile to confirm

**Likelihood:** 30% — Possible but unverified

---

### 3. Monaco Editor Bundle Load (High Probability)
**Evidence:**
- `text` primitive (appType: text) in code.egg.md is a Monaco editor
- Monaco is a large bundle (~5MB minified)
- Monaco initializes workers (syntax highlighting, language services)
- **NOT traced in this investigation** — text primitive implementation not read

**Missing Data:**
- How is Monaco loaded? Dynamic import?
- Does it start background workers?
- Does it poll for file changes?

**Likelihood:** 60% — Monaco is known to be resource-intensive

---

### 4. Browser Extension Interference (Medium Probability)
**Evidence:**
- None in code

**Hypothesis:**
- Ad blockers, React DevTools, or other extensions may inject observers or polling

**Likelihood:** 20% — External to codebase

---

### 5. Session State Accumulation / Memory Leak (Low Probability)
**Evidence:**
- None in code

**Hypothesis:**
- Event listeners not cleaned up
- Redux state growing unbounded
- Bus subscriptions accumulating

**Counter-Evidence:**
- All useEffect hooks have cleanup functions
- ResizeObservers call `.disconnect()`
- setInterval calls have clearInterval

**Likelihood:** 10% — Cleanup appears correct

---

## Ruled Out

### 1. ResizeObserver in TreeBrowser
**Why:** Guarded, threshold-based, cleans up. Only fires when width crosses collapseThreshold.

### 2. Autosave Timer
**Why:** NOT started by default. No call to `startAutosave()` found.

### 3. Build Monitor Polling
**Why:** build-monitor primitive NOT in code.egg.md.

### 4. PaneLoader Spinner
**Why:** Only renders during LOADING state, not after panes mount.

### 5. Viewport Resize Listeners (Shell.tsx)
**Why:** Event-driven (user resize), not continuous polling.

---

## What a Chrome DevTools Profile Would Need to Confirm

To identify the actual cause, record a Performance profile during the slowdown and look for:

1. **Long Tasks** (>50ms)
   - If ResizeObserver callbacks show up repeatedly → cascade confirmed
   - If Monaco worker messages dominate → Monaco is the cause

2. **Scripting Flame Graph**
   - Which functions consume the most CPU?
   - Look for `observer.observe`, `dispatch`, `setState` in hot path

3. **Memory Timeline**
   - Is memory growing unbounded? → Memory leak
   - Are Detached DOM nodes accumulating? → Cleanup issue

4. **Network Tab**
   - Is polling happening? (XHR/fetch requests repeating)
   - Is Monaco loading chunks repeatedly?

5. **Rendering Timeline**
   - Are layout/paint cycles repeating rapidly?
   - Which elements trigger reflow?

**Critical Questions:**
- Is CPU usage at 100% for one core?
- Does killing the tab immediately restore performance?
- Does the issue reproduce in Incognito mode (no extensions)?
- Does it reproduce with a minimal set? (e.g., just top-bar + status-bar, no editor/terminal)

---

## Recommended Next Steps

### Immediate Actions:

1. **Run Chrome DevTools Performance Profile**
   - Load shiftcenter.com/?set=code
   - Start recording
   - Wait for slowdown
   - Stop recording
   - Share profile (or screenshot of flame graph)

2. **Test with Minimal Set**
   - Create `minimal.set.md` with only top-bar + status-bar
   - Load `?set=minimal`
   - Does slowdown still occur?

3. **Test in Incognito Mode**
   - Disables extensions
   - If issue goes away → extension interference

4. **Monitor Memory Growth**
   - Open Chrome Task Manager (Shift+Esc)
   - Watch memory for shiftcenter.com tab
   - Is it growing continuously?

### Code Investigations (if DevTools points to specific patterns):

1. **Trace Monaco Editor Load**
   - Read `browser/src/apps/textPaneAdapter.tsx`
   - Check if Monaco starts workers
   - Check if Monaco polls for changes

2. **Audit `UPDATE_LAYOUT_DIMENSIONS` Dispatch Chain**
   - Find all reducers that handle this action
   - Check if any trigger layout changes
   - Instrument with console.log to count dispatches

3. **Add Instrumentation to ResizeObserver Callbacks**
   - Log every observer callback with timestamp
   - Count how many fire per second during idle

---

## Clock / Cost / Carbon

- **Clock:** 42 minutes (file reads, code tracing, grep searches, response writing)
- **Cost:** ~$0.12 (Sonnet 4.5, ~130k tokens)
- **Carbon:** ~0.5g CO2e (estimated)

---

## Issues / Follow-ups

1. **Cannot confirm ResizeObserver cascade without runtime profiling**
   - Code trace shows it COULD loop if dispatch causes re-layout
   - Need Performance profile to verify

2. **Monaco editor not investigated**
   - High-probability suspect
   - Need to trace text primitive implementation

3. **Away manager activation not confirmed**
   - wireEgg() likely starts it, but not verified
   - Low impact even if active

4. **No reproduction steps tested**
   - This is pure static analysis
   - Need live testing with instrumentation

**Recommended follow-up:** Dispatch TASK-PERF-FIX-001 ONLY after DevTools profile confirms root cause.
