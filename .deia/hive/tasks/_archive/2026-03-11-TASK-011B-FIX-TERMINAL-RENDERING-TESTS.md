# TASK-011B: Fix 41 Failing Terminal Rendering Tests

## Objective

Fix the 41 failing tests in `browser/src/primitives/terminal/__tests__/`. These are rendering test failures caused by wrong component props, wrong format expectations, and non-existent function calls. 49 tests already pass — do NOT modify passing tests.

## Context

TASK-011A wrote all 10 test files (90 tests), but 41 fail across 6 files. The tests were written against incorrect component signatures. This is a test fix task — do NOT modify any source files. Only fix test files.

## Files to Read First

Read these source files to understand the actual component APIs:

- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\terminal\TerminalOutput.tsx` (194 lines)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\terminal\TerminalResponsePane.tsx` (52 lines)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\terminal\TerminalStatusBar.tsx` (101 lines)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\terminal\TerminalApp.tsx` (~160 lines)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\terminal\irRouting.ts` (85 lines)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\terminal\types.ts` (83 lines)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\terminal\useTerminal.ts` (~356 lines)

Then read the failing test files:

- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\terminal\__tests__\TerminalOutput.test.tsx`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\terminal\__tests__\TerminalResponsePane.test.tsx`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\terminal\__tests__\TerminalStatusBar.test.tsx`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\terminal\__tests__\TerminalStatusBar.currencies.test.tsx`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\terminal\__tests__\TerminalApp.paneNav.test.tsx`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\terminal\__tests__\irRouting.test.ts`

## Exact Failure Diagnosis (per file)

### 1. TerminalResponsePane.test.tsx (0/8 failing) — WRONG COMPONENT API

The tests use completely wrong props:
```typescript
// WRONG (what tests do):
<TerminalResponsePane response="text" onClose={fn} />

// RIGHT (actual component):
<TerminalResponsePane
  entries={TerminalEntry[]}
  loading={boolean}
  position={'top'|'bottom'|'left'|'right'|'hidden'}
  defaultState={'collapsed'|'expanded'|'hidden'}
  bus={MessageBus|null}
  nodeId={string|null}
  onOpenInDesigner={(ir) => void}
  onCopy={(text) => void}
  onDownload={(ir) => void}
/>
```

**Fix:** Rewrite all 8 tests to use actual props. Test position variants (top/bottom/left/right/hidden), test `returns null when position=hidden`, test `returns null when defaultState=hidden`, test entries passing to TerminalOutput child.

### 2. TerminalStatusBar.test.tsx (0/8 failing) — MISSING REQUIRED PROP + FORMAT MISMATCH

Problems:
1. Missing required `model` prop — tests only pass `ledger`
2. Format expectations wrong:
   - Tests expect `5000ms` — actual renders `clock: 5.0s` (uses `toFixed(1)` on seconds)
   - Tests expect `$0.25` — actual renders `cost: $0.2500` (uses `toFixed(4)`)
   - Tests expect `10.5g` — actual renders `carbon: 10.5000g` (uses `toFixed(4)`)
3. Tests expect "messages" text — component doesn't render message count

**Fix:** Add `model="test-model"` to every render call. Update all format matchers to match actual output format (seconds not ms, 4 decimal places for cost/carbon). Remove message count assertions.

### 3. TerminalStatusBar.currencies.test.tsx (0/5 failing) — SAME AS ABOVE

Same missing `model` prop and format mismatch issues.

**Fix:** Same as TerminalStatusBar.test.tsx — add model prop, fix format expectations.

### 4. TerminalApp.paneNav.test.tsx (0/7 failing) — WRONG PROP NAME + WRONG EVENTS

Problems:
1. Tests pass `paneState={{ nickname: 'test-pane' }}` — actual prop is `nodeId?: string`
2. Tests expect `route-ir` event — actual is `terminal:open-in-designer`
3. Tests expect `onNavigate` for designer — actual uses `window.open('/design/new', '_blank')`

**Fix:** Replace `paneState={{ nickname: 'test-pane' }}` with `nodeId="test-pane"`. Replace `paneState={null}` with omitting nodeId (standalone). Fix event name assertions. Fix navigation assertions to match actual behavior.

### 5. irRouting.test.ts (3/5 failing) — FUNCTIONS DON'T EXIST

Tests call `routeIRToPane()` and `shouldRouteIR()` — these functions do NOT exist in irRouting.ts.

Actual exports:
```typescript
export function openInDesigner(ir: any, ctx: IRRoutingContext): void
export function copyToClipboard(text: string, ctx: IRRoutingContext): void
export function downloadIR(ir: any): void
```

**Fix:** Rewrite the 3 failing tests to test actual exported functions (openInDesigner, copyToClipboard, downloadIR) with correct signatures and behaviors.

### 6. TerminalOutput.test.tsx (0/10 failing) — MOCK/RENDER ISSUES

Read the actual component carefully. Check:
- Mock setup for frank service (extractJsonBlocks, isValidIR, formatMetrics)
- DOM class selectors (.terminal-line, .terminal-banner, .terminal-response, .terminal-ir-block)
- Component prop interface (entries, loading, onOpenInDesigner, onCopy, onDownload)
- The formatMetrics mock must return the exact format the component renders

**Fix:** Align mocks with actual frank service signatures. Ensure render calls use correct props. Match DOM selectors to actual CSS classes.

## Constraints

- TypeScript strict mode
- vitest + @testing-library/react
- Do NOT modify any source files — only fix test files
- Do NOT break the 49 already-passing tests
- Mock external dependencies (frank service, relay_bus)
- All files under 500 lines

## Deliverables

- [ ] Fix `TerminalOutput.test.tsx` — 10 tests passing
- [ ] Fix `TerminalResponsePane.test.tsx` — 8 tests passing
- [ ] Fix `TerminalStatusBar.test.tsx` — 8 tests passing
- [ ] Fix `TerminalStatusBar.currencies.test.tsx` — 5 tests passing
- [ ] Fix `TerminalApp.paneNav.test.tsx` — 7 tests passing
- [ ] Fix `irRouting.test.ts` — 5 tests passing (2 already pass + 3 fixes)

### Verification

- [ ] All 90 tests pass (49 existing + 41 fixed)
- [ ] No source files modified
- [ ] vitest runs clean with zero failures

## Response Requirements -- MANDATORY

When you finish your work, write a response file:
  `.deia/hive/responses/YYYYMMDD-TASK-011B-RESPONSE.md`

The response MUST contain these 8 sections:
1. **Header** -- task ID, title, status (COMPLETE/FAILED), model, date
2. **Files Modified** -- every file created/modified/deleted, full paths
3. **What Was Done** -- bullet list of concrete changes
4. **Test Results** -- test files run, pass/fail counts
5. **Build Verification** -- vitest output summary
6. **Acceptance Criteria** -- copy deliverables above, mark [x] or [ ]
7. **Clock / Cost / Carbon** -- all three, never omit any
8. **Issues / Follow-ups** -- edge cases, dependencies, recommended next tasks

DO NOT skip any section. A response without all 8 sections is incomplete.
