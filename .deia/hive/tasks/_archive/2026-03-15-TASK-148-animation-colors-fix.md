# TASK-148: Fix hardcoded colors in animation components

## Objective
Remove all hardcoded hex colors from 6 animation components by replacing theme.ts imports with CSS variables. This is a CRITICAL VIOLATION of Rule #3.

## Context
All animation components currently import from `src/apps/sim/lib/theme.ts` which contains hardcoded hex colors:
```typescript
export const colors = {
  purple: "#8b5cf6",  // ← VIOLATION
  green: "#22c55e",   // ← VIOLATION
  // ... 20+ more hex colors
}
```

**Rule #3:** NO HARDCODED COLORS. Only CSS variables (`var(--sd-*)`). No hex, no rgb(), no named colors.

The platform versions also had this issue (see NodePulse.tsx line 27: `color = '#a855f7'`). All must be converted to CSS variables.

## Files to Modify
All paths under `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\sim\components\flow-designer\animation\`:

1. **TokenAnimation.tsx** (115 lines)
   - Remove: `import { colors } from '../../../lib/theme';`
   - Find: `color = colors.purple` or hex literals
   - Replace with: `color = 'var(--sd-purple)'`
   - Check canvas gradient code for hex literals

2. **NodePulse.tsx** (120 lines)
   - Remove: `import { colors } from '../../../lib/theme';`
   - Replace: `color = 'var(--sd-purple)'` (default prop)
   - Ensure backgroundColor uses CSS var
   - Check boxShadow for hardcoded colors

3. **QueueBadge.tsx** (82 lines)
   - Remove: `import { colors } from '../../../lib/theme';`
   - Replace all color/backgroundColor with `var(--sd-*)`
   - Check badge background, border, text colors

4. **ResourceBar.tsx** (91 lines)
   - Remove: `import { colors } from '../../../lib/theme';`
   - Replace: `barColor = 'var(--sd-green)'`, `backgroundColor = 'var(--sd-bg-terminal)'`, `textColor = 'var(--sd-text-primary)'`
   - Check dynamic color thresholds (>0.8 red, >0.6 orange)

5. **CheckpointFlash.tsx** (141 lines)
   - Remove: `import { colors } from '../../../lib/theme';`
   - Replace all inline styles using colors.*
   - Check gradient/animation color stops

6. **SimClock.tsx** (194 lines)
   - Remove: `import { colors, fonts } from '../../../lib/theme';`
   - Replace: `fontFamily: 'var(--sd-font-mono)'` (fonts.mono)
   - Replace all color references with CSS vars
   - Check: paused state colors, speed indicators, status dot

## Files to Read First
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\sim\components\flow-designer\animation\TokenAnimation.tsx`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\sim\components\flow-designer\animation\NodePulse.tsx`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\sim\components\flow-designer\animation\QueueBadge.tsx`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\sim\components\flow-designer\animation\ResourceBar.tsx`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\sim\components\flow-designer\animation\CheckpointFlash.tsx`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\sim\components\flow-designer\animation\SimClock.tsx`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\App.tsx` (lines 1-100, for CSS var examples)

## Deliverables
- [ ] All 6 components updated (theme.ts import removed)
- [ ] All color props use `var(--sd-*)` syntax
- [ ] All inline styles use CSS variables
- [ ] No hex literals anywhere (e.g., #8b5cf6)
- [ ] No rgb() literals anywhere (e.g., rgba(139,92,246,0.15))
- [ ] Fonts use `var(--sd-font-mono)` and `var(--sd-font-sans)`
- [ ] Default prop values use CSS variables
- [ ] Dynamic color calculations still work (e.g., ResourceBar thresholds)

## CSS Variable Reference (Common Colors)
Based on usage in App.tsx and buildMonitorAdapter.tsx:
- `var(--sd-purple)` — primary brand color
- `var(--sd-green)` — success, active state
- `var(--sd-orange)` — warning, paused state
- `var(--sd-red)` — error, high utilization
- `var(--sd-blue)` — info
- `var(--sd-cyan)` — accent
- `var(--sd-text-primary)` — main text
- `var(--sd-text-secondary)` — muted text
- `var(--sd-text-muted)` — dimmer text
- `var(--sd-bg-terminal)` — dark background
- `var(--sd-border)` — border color
- `var(--sd-font-mono)` — monospace font
- `var(--sd-font-sans)` — sans-serif font
- `var(--sd-font-sm)`, `var(--sd-font-md)` — font sizes
- `var(--sd-shadow-sm)`, `var(--sd-shadow-xl)` — shadows

Dimmed variants (for transparency):
- `var(--sd-purple-dim)` — 15% opacity purple
- `var(--sd-purple-dimmer)` — more transparent purple
- `var(--sd-green-dim)`, `var(--sd-green-dimmer)`, etc.

## Test Requirements
- [ ] After changes, run: `cd browser && npx vitest run src/apps/sim/components/flow-designer/animation/`
- [ ] All non-skipped tests pass (assumes TASK-147 completed first)
- [ ] Visual inspection: load flow designer in browser, verify animations render correctly
- [ ] No console errors about undefined CSS variables

## Edge Cases
- **TokenAnimation canvas gradient:** May need to extract color from CSS variable at runtime for canvas API
- **NodePulse boxShadow:** Ensure glow effect color matches dot color
- **SimClock keyframe animations:** CSS vars in inline `<style>` tags may need special handling
- **ResourceBar dynamic colors:** Threshold logic (>0.8 red) must still use CSS vars

## Constraints
- Max 500 lines per file (all files currently under 200)
- CSS: var(--sd-*) ONLY — this is the entire point of this task
- No stubs — every color replacement must be complete
- TDD: Tests may fail after changes, must fix and verify pass

## Smoke Test Command
```bash
cd C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser
npx vitest run src/apps/sim/components/flow-designer/animation/
npm run build 2>&1 | tail -20
```

Expected: Tests pass, build succeeds, no TypeScript errors about missing colors export

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `.deia/hive/responses/20260315-TASK-148-RESPONSE.md`

The response MUST contain these 8 sections:
1. **Header** — task ID, title, status (COMPLETE/FAILED), model, date
2. **Files Modified** — every file created/modified/deleted, full paths
3. **What Was Done** — bullet list of concrete changes (how many color replacements per file)
4. **Test Results** — test files run, pass/fail counts
5. **Build Verification** — npm run build output (last 20 lines)
6. **Acceptance Criteria** — copy from task, mark [x] or [ ]
7. **Clock / Cost / Carbon** — all three, never omit any
8. **Issues / Follow-ups** — any CSS vars that needed runtime extraction, visual issues

DO NOT skip any section.

## Heartbeat Requirement
POST to http://localhost:8420/build/heartbeat every 3 minutes:
```json
{"task_id": "TASK-148", "status": "running", "model": "haiku", "message": "fixing hardcoded colors"}
```
