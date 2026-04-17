# TASK-CANVAS-000: Convert Flow-Designer Floating Panels to Shell Panes

## Objective
Refactor ALL floating panels in the flow-designer from custom absolute-positioned divs to proper shell panes — defined in the EGG, managed by the shell, communicating via MessageBus.

## Context
The flow-designer currently renders SimConfigPanel, ProgressPanel, ResultsPreview, PlaybackControls, and SimulationConfig as custom `position: absolute` divs with hardcoded z-indexes. None of them use the shell infrastructure (PaneChrome, MessageBus, layout tree). This violates the architecture — we have a governed pane shell and everything must go through it.

**Current (WRONG):**
- SimConfigPanel: absolute, top:70 left:14, z-index:50 — props/callbacks
- ProgressPanel: absolute, top:70 right:14, z-index:50 — props/callbacks
- ResultsPreview: absolute, bottom:14 right:14, z-index:50 — props/callbacks
- PlaybackMode bottom panel: absolute, bottom:0, z-index:50 — props/callbacks
- SimulationConfig modal: fixed, inset:0, z-index:2000 — props/callbacks

**Target (CORRECT):**
- Each panel becomes a pane adapter (like simAdapter, textPaneAdapter, etc.)
- Panes are defined in canvas.egg.md with proper pane IDs
- Panes communicate via MessageBus events (not props/callbacks)
- Shell manages positioning, chrome, drag/resize
- Mode switching shows/hides the relevant panes via bus events or EGG mode config

## Files to Read First
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\simAdapter.tsx` (existing sim adapter pattern)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\textPaneAdapter.tsx` (adapter pattern reference)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\terminalAdapter.tsx` (adapter pattern reference)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\eggToShell.ts` (how EGG defines panes)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\types.ts` (shell tree types)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\eggs\canvas.egg.md` (current canvas EGG layout)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\sim\components\flow-designer\FlowDesigner.tsx` (lines 1042-1078, current panel rendering)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\sim\components\flow-designer\simulation\SimConfigPanel.tsx`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\sim\components\flow-designer\simulation\ProgressPanel.tsx`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\sim\components\flow-designer\simulation\ResultsPreview.tsx`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\sim\components\flow-designer\modes\PlaybackMode.tsx`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\infrastructure\relay_bus\` (MessageBus types)

## Deliverables

### New Pane Adapters
- [ ] `browser/src/apps/sim/adapters/simConfigPaneAdapter.tsx` — wraps SimConfigPanel as a shell pane
- [ ] `browser/src/apps/sim/adapters/simProgressPaneAdapter.tsx` — wraps ProgressPanel + ResultsPreview
- [ ] `browser/src/apps/sim/adapters/playbackControlsPaneAdapter.tsx` — wraps PlaybackControls as a shell pane

### Register Adapters
- [ ] Register all 3 new adapters in `browser/src/apps/index.ts` (or wherever app types are mapped)
- [ ] New appType strings: `sim-config-panel`, `sim-progress-panel`, `playback-controls`

### Update canvas.egg.md
- [ ] Define pane slots for sim config (left or floating), progress (right or floating), playback controls (bottom or floating)
- [ ] Each mode can specify which panes are visible — use the EGG's mode system or bus events
- [ ] Sim mode: show sim-config-panel (left) + sim-progress-panel (right)
- [ ] Playback mode: show playback-controls (bottom)
- [ ] Design mode: neither (just the canvas + palette + properties)

### Bus Integration
- [ ] `sim:config-updated` — SimConfigPanel publishes config changes via bus instead of props
- [ ] `sim:progress-updated` — SimulateMode publishes progress/metrics via bus instead of props
- [ ] `sim:results-available` — Published when simulation completes, ProgressPanel listens
- [ ] `sim:playback-control` — PlaybackControls publishes play/pause/step/speed via bus
- [ ] FlowDesigner listens to bus events instead of passing props to inline panels

### Remove Custom Positioning
- [ ] Remove absolute-positioned panel rendering from FlowDesigner.tsx (lines 1042-1078)
- [ ] Remove z-index stacking from panel components
- [ ] Remove SlideUpPanel responsive hack (shell handles responsive layout)

### Tests
- [ ] `browser/src/apps/sim/adapters/__tests__/simConfigPaneAdapter.test.tsx`
- [ ] `browser/src/apps/sim/adapters/__tests__/simProgressPaneAdapter.test.tsx`
- [ ] `browser/src/apps/sim/adapters/__tests__/playbackControlsPaneAdapter.test.tsx`
- [ ] Bus integration tests: config published → canvas receives, progress published → panel receives

## Test Requirements
- [ ] Tests written FIRST (TDD)
- [ ] All tests pass
- [ ] 15+ tests across the 3 adapter test files
- [ ] Bus round-trip tests: publish event → adapter receives → renders correctly
- [ ] Edge cases: mode switch hides/shows correct panes, rapid mode switching, no stale state

## Constraints
- No file over 500 lines
- CSS: var(--sd-*) only
- No stubs — every adapter fully functional
- No custom z-index stacking — let the shell handle layering
- No position:absolute/fixed for panel placement — shell manages layout
- Panels can use the "floating pane" look (glassmorphism, backdrop blur) via CSS on the pane content — but the PANE ITSELF is shell-managed
- All communication via MessageBus, not React props/callbacks between unrelated components

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `.deia/hive/responses/20260323-TASK-CANVAS-000-RESPONSE.md`

The response MUST contain these 8 sections:
1. **Header** — task ID, title, status (COMPLETE/FAILED), model, date
2. **Files Modified** — every file created/modified/deleted, full paths
3. **What Was Done** — bullet list of concrete changes
4. **Test Results** — test files run, pass/fail counts
5. **Build Verification** — test/build output summary
6. **Acceptance Criteria** — copy from task, mark [x] or [ ]
7. **Clock / Cost / Carbon** — all three, never omit any
8. **Issues / Follow-ups** — anything that didn't work, edge cases, recommended next tasks

DO NOT skip any section.
