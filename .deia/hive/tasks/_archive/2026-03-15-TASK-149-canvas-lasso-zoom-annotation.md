# TASK-149: Port Canvas Lasso Selection + Zoom Controls + Annotation Badge

## Objective

Port 3 canvas interaction components from platform/simdecisions-2 to browser/src/apps/sim/components/flow-designer: LassoOverlay (multi-select), ZoomControls (enhanced version), and AnnotationBadge (comment indicator).

## Context

**This is part of the w1 canvas work stream.** Previous specs SPEC-w1-06 (node types) and SPEC-w1-07 (animation) are complete. This task adds user interaction components.

**Current state:**
- ZoomControls.tsx already exists at `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\sim\components\flow-designer\ZoomControls.tsx` (141 lines) — this will be REPLACED with the enhanced version from platform
- LassoOverlay does NOT exist yet — this is NEW
- AnnotationBadge does NOT exist yet — this is NEW
- overlays/ directory exists with 3 files (DistributionTooltip, TimingBadge, VariablePill)

**Integration points:**
- LassoOverlay needs to integrate with FlowCanvas.tsx (already uses ReactFlow)
- ZoomControls is already imported in FlowDesigner.tsx
- AnnotationBadge will be used in node overlays (future integration)

## Files to Read First

**Platform source files (read these first):**
- `C:\Users\davee\OneDrive\Documents\GitHub\platform\simdecisions-2\src\components\canvas\LassoOverlay.tsx` (108 lines)
- `C:\Users\davee\OneDrive\Documents\GitHub\platform\simdecisions-2\src\components\canvas\controls\ZoomControls.tsx` (96 lines)
- `C:\Users\davee\OneDrive\Documents\GitHub\platform\simdecisions-2\src\components\canvas\controls\ZoomControls.css` (54 lines)
- `C:\Users\davee\OneDrive\Documents\GitHub\platform\simdecisions-2\src\components\canvas\AnnotationBadge.tsx` (59 lines)
- `C:\Users\davee\OneDrive\Documents\GitHub\platform\simdecisions-2\src\components\canvas\AnnotationBadge.css` (122 lines)
- `C:\Users\davee\OneDrive\Documents\GitHub\platform\simdecisions-2\src\components\canvas\__tests__\Canvas.lasso.test.tsx` (127 lines — lasso test reference)

**Shiftcenter target files (read these to understand existing structure):**
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\sim\components\flow-designer\FlowCanvas.tsx` (existing ReactFlow wrapper)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\sim\components\flow-designer\ZoomControls.tsx` (current version, to be replaced)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\sim\components\flow-designer\__tests__\FlowToolbar.test.tsx` (test reference)

## Deliverables

**File 1: LassoOverlay.tsx** (NEW)
- [ ] Create `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\sim\components\flow-designer\overlays\LassoOverlay.tsx`
- [ ] Port logic from platform LassoOverlay.tsx
- [ ] Adapt to shiftcenter patterns:
  - Use inline styles with CSS variables (NO external CSS file)
  - Replace platform stores (useSelectionStore, useGraphStore, useUIStore) with appropriate shiftcenter equivalents OR props
  - Ray-casting algorithm preserved exactly
  - SVG overlay with crosshair cursor when active
- [ ] **Max 150 lines** (the platform version is 108 lines, so this should fit easily)

**File 2: ZoomControls.tsx** (REPLACE existing)
- [ ] Replace `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\sim\components\flow-designer\ZoomControls.tsx`
- [ ] Port enhanced version from platform ZoomControls.tsx + ZoomControls.css
- [ ] Add features missing from current version:
  - Auto-layout button (TB/LR with shift-click toggle)
  - Separator lines between control groups
  - Optional: AI assistant toggle button (onToggleAI prop)
  - Optional: Describe process button (onDescribeProcess prop)
- [ ] Convert CSS to inline styles with CSS variables only
- [ ] **Max 200 lines** (current is 142, platform TSX is 96 + 54 CSS = 150 total)

**File 3: AnnotationBadge.tsx** (NEW)
- [ ] Create `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\sim\components\flow-designer\overlays\AnnotationBadge.tsx`
- [ ] Port logic from platform AnnotationBadge.tsx + AnnotationBadge.css
- [ ] Convert CSS to inline styles with CSS variables only
- [ ] Replace emojis (🔴, ⚠️, 📝) with lucide-react icons (CircleDot, AlertTriangle, FileText)
- [ ] Tooltip on hover with fade-in animation
- [ ] **Max 150 lines** (platform is 59 TSX + 122 CSS = 181 total, but removing CSS file saves space)

**File 4: LassoOverlay.test.tsx** (NEW)
- [ ] Create `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\sim\components\flow-designer\__tests__\LassoOverlay.test.tsx`
- [ ] **Minimum 6 tests** (refer to platform Canvas.lasso.test.tsx for test scenarios):
  1. Renders SVG overlay when active prop is true
  2. Does not render when active prop is false
  3. Applies crosshair cursor when active
  4. Creates path on mouse drag (mousedown → mousemove → mouseup)
  5. Ray-casting algorithm: point inside polygon returns true
  6. Ray-casting algorithm: point outside polygon returns false
- [ ] Use vitest + @testing-library/react
- [ ] Mock ReactFlow hooks if needed (useReactFlow)

**File 5: ZoomControls.test.tsx** (NEW)
- [ ] Create `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\sim\components\flow-designer\__tests__\ZoomControls.test.tsx`
- [ ] **Minimum 7 tests**:
  1. Renders all 4 base buttons (zoom in, zoom out, fit, layout)
  2. Displays zoom percentage correctly
  3. Calls onZoomIn when + button clicked
  4. Calls onZoomOut when − button clicked
  5. Calls onFitView when ⊡ button clicked
  6. Auto-layout button calls applyLayout with 'TB' on normal click
  7. Optional buttons (AI, describe) render only when props provided
- [ ] Use vitest + @testing-library/react

**File 6: AnnotationBadge.test.tsx** (NEW)
- [ ] Create `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\sim\components\flow-designer\overlays\__tests__\AnnotationBadge.test.tsx`
- [ ] **Minimum 6 tests**:
  1. Renders badge with correct icon for each type (pain_point, exception, note)
  2. Truncates content longer than 30 characters
  3. Shows tooltip on hover
  4. Hides tooltip on mouse leave
  5. Tooltip displays full content
  6. Tooltip shows nodeId when provided

## Test Requirements

- [ ] **TDD: Write tests FIRST, then implementation**
- [ ] All tests pass with 0 failures
- [ ] Total: **19 tests minimum** (6 LassoOverlay + 7 ZoomControls + 6 AnnotationBadge)
- [ ] Edge cases covered:
  - LassoOverlay: left-click only (ignore right-click), empty path handling
  - ZoomControls: optional props (onToggleAI, onDescribeProcess) only render when provided
  - AnnotationBadge: tooltip animation, content truncation, missing nodeId
- [ ] Run smoke test: `cd browser && npx vitest run src/apps/sim/components/flow-designer/`
- [ ] **No new test failures** — existing flow-designer tests must still pass

## Constraints

**Hard Rules (from BOOT.md):**
- [ ] **No file over 500 lines** (hard limit: 1,000)
- [ ] **CSS: var(--sd-*) only** — NO hardcoded colors, NO hex, NO rgb(), NO named colors
- [ ] **No stubs** — every function fully implemented
- [ ] **TDD** — tests first, then implementation
- [ ] **All file paths absolute** in response file

**Specific constraints for this task:**
- [ ] LassoOverlay: preserve ray-casting algorithm exactly (point-in-polygon logic)
- [ ] ZoomControls: replace existing file — maintain backward compatibility with current props
- [ ] AnnotationBadge: replace emojis with lucide-react icons
- [ ] NO external CSS files — all styles inline with CSS variables
- [ ] NO platform dependencies — replace stores with props or local state

**CSS Variable Reference (from existing code):**
```css
/* Colors */
--sd-purple, --sd-purple-dimmest, --sd-text-primary, --sd-text-secondary, --sd-text-muted, --sd-text-dim
--sd-border, --sd-glass-bg, --sd-glass-blur, --sd-shadow-md
--sd-error, --sd-error-light, --sd-error-dark
--sd-warning, --sd-warning-light, --sd-warning-dark
--sd-info, --sd-info-light, --sd-info-dark

/* Fonts */
--sd-font-xs, --sd-font-base, --sd-font-md, --sd-font-lg, --sd-font-mono
```

## Heartbeats

**IMPORTANT:** Send heartbeat every 3 minutes while working:
```bash
curl -X POST http://localhost:8420/build/heartbeat \
  -H "Content-Type: application/json" \
  -d '{"task_id":"2026-03-15-1124-SPEC-w1-08-canvas-lasso-zoom","status":"running","model":"haiku","message":"working"}'
```

Do NOT skip heartbeats. The build monitor needs these to track progress.

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260315-TASK-149-RESPONSE.md`

The response MUST contain these 8 sections:
1. **Header** — task ID, title, status (COMPLETE/FAILED), model, date
2. **Files Modified** — every file created/modified/deleted, full absolute paths
3. **What Was Done** — bullet list of concrete changes (not intent)
4. **Test Results** — test files run, pass/fail counts, example: "19 tests, 19 passed, 0 failed"
5. **Build Verification** — smoke test output summary (last 5 lines)
6. **Acceptance Criteria** — copy from this task, mark [x] or [ ] with explanations
7. **Clock / Cost / Carbon** — all three, never omit any (estimate if needed)
8. **Issues / Follow-ups** — edge cases, dependencies, next tasks

DO NOT skip any section.

## Expected Timeline

- Read source files: 5 min
- Write tests (19 tests): 30 min
- Implement LassoOverlay: 20 min
- Implement ZoomControls (replace): 15 min
- Implement AnnotationBadge: 20 min
- Run tests + fix failures: 15 min
- Write response file: 10 min
**Total: ~2 hours (with heartbeats every 3 min)**

## Notes

- This is a PORT, not a rewrite. Copy/adapt existing logic from platform.
- The platform code is proven and tested — preserve the core algorithms.
- If platform dependencies (stores, hooks) don't exist in shiftcenter, replace with props or local state.
- ZoomControls is REPLACING the existing file — ensure backward compatibility with existing usage in FlowDesigner.tsx.
- AnnotationBadge is for future use — it doesn't need to be integrated into nodes yet, just ported and tested.
- If you encounter missing dependencies (like useLayout hook), create a minimal stub OR accept the prop from parent component.

## Success Criteria

- [ ] 3 components ported (LassoOverlay, ZoomControls, AnnotationBadge)
- [ ] 19 tests passing (6 + 7 + 6)
- [ ] No hardcoded colors (all var(--sd-*))
- [ ] No files over 500 lines
- [ ] No stubs
- [ ] Smoke test passes with 0 new failures
- [ ] Response file complete with all 8 sections
