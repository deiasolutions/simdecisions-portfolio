# TASK-147: Port animation component test suite

## Objective
Port comprehensive test suite from platform repo to shiftcenter for 6 animation components + hook. Adapt imports for local structure.

## Context
Animation components were ported on 2026-03-14 but NO TESTS were written. Platform has a complete test suite (228 lines, 17 test cases, 3 skipped due to timing issues). This violates the TDD requirement (Rule #5).

**Source test file:**
`C:\Users\davee\OneDrive\Documents\GitHub\platform\simdecisions-2\src\components\canvas\animation\__tests__\animation.test.tsx` (228 lines)

**Target location:**
`C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\sim\components\flow-designer\animation\__tests__\animation.test.tsx`

**Components under test:**
1. TokenAnimation (115 lines)
2. NodePulse (120 lines)
3. QueueBadge (82 lines)
4. ResourceBar (91 lines)
5. CheckpointFlash (141 lines)
6. SimClock (194 lines)
7. useAnimationFrame hook (44 lines)

## Files to Read First
- `C:\Users\davee\OneDrive\Documents\GitHub\platform\simdecisions-2\src\components\canvas\animation\__tests__\animation.test.tsx`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\sim\components\flow-designer\animation\index.ts` (current exports)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\test\setup.ts` (vitest config)

## Deliverables
- [ ] Create `__tests__` directory in animation folder
- [ ] Port animation.test.tsx (adapt all import paths)
- [ ] Fix import path for useAnimationFrame (platform: `../../../../hooks/`, shiftcenter: `./`)
- [ ] All 17 test cases ported (including 3 skipped tests with skip reason preserved)
- [ ] Tests run and pass (skipped tests not counted as failures)
- [ ] No hardcoded colors in test assertions (use CSS variable names)

## Test Requirements
- [ ] Tests written FIRST (TDD) — ✓ Already exist in platform, just need porting
- [ ] All tests pass (excluding skipped)
- [ ] Edge cases covered:
  - TokenAnimation: isActive true/false, canvas rendering
  - NodePulse: animation timing, opacity states, position tracking
  - QueueBadge: count=0 (hidden), count>999 (shows "999+")
  - ResourceBar: utilization thresholds (>0.8 red, >0.6 orange), percentage display
  - CheckpointFlash: onAnimationComplete callback (skipped in platform due to timing)
  - SimClock: time formatting (ms/seconds/minutes), paused state, speed indicators
  - useAnimationFrame: enable/disable toggle, callback invocation (skipped in platform)
- [ ] Test file under 400 lines (source is 228, should be similar after porting)

## Import Path Adaptations Needed

**Platform imports:**
```typescript
import { useAnimationFrame } from '../../../../hooks/useAnimationFrame';
```

**ShiftCenter imports:**
```typescript
import { useAnimationFrame } from '../useAnimationFrame';
```

All component imports stay as relative from `__tests__/` to parent directory.

## Constraints
- Max 500 lines per file (source is 228, should fit easily)
- CSS: var(--sd-*) only — tests should NOT assert on hex values
- No stubs — every test fully implemented
- TDD: tests exist, just need porting
- Preserve skip reasons for timing-related tests (3 tests marked `.skip`)

## Smoke Test Command
```bash
cd C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser
npx vitest run src/apps/sim/components/flow-designer/animation/
```

Expected: ~14 passing, ~3 skipped, 0 failures

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `.deia/hive/responses/20260315-TASK-147-RESPONSE.md`

The response MUST contain these 8 sections:
1. **Header** — task ID, title, status (COMPLETE/FAILED), model, date
2. **Files Modified** — every file created/modified/deleted, full paths
3. **What Was Done** — bullet list of concrete changes
4. **Test Results** — test files run, pass/fail counts, skip counts
5. **Build Verification** — test/build output summary (last 10 lines)
6. **Acceptance Criteria** — copy from task, mark [x] or [ ]
7. **Clock / Cost / Carbon** — all three, never omit any
8. **Issues / Follow-ups** — edge cases, dependencies, next tasks

DO NOT skip any section.

## Heartbeat Requirement
POST to http://localhost:8420/build/heartbeat every 3 minutes:
```json
{"task_id": "TASK-147", "status": "running", "model": "haiku", "message": "porting tests"}
```
