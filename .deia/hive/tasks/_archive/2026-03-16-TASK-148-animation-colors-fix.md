# TASK-148: Fix hardcoded colors in 6 animation components

## Objective
Replace all hardcoded color values in 6 animation components with CSS variables (`var(--sd-*)`).

## Context
Hard Rule #3: NO HARDCODED COLORS. Only CSS variables (`var(--sd-*)`). No hex, no rgb(), no named colors. Everything.

The 6 animation components currently violate this rule by:
1. Importing from `theme.ts` which contains hardcoded hex/rgb values
2. Using hardcoded rgba() values inline for gradients and shadows
3. Computing rgba values from hex strings at runtime

All components must be updated to use CSS variables defined in `shell-themes.css`.

## Files to Read First
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\shell-themes.css` (CSS variable definitions)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\sim\lib\theme.ts` (current hardcoded theme)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\sim\components\flow-designer\__tests__\animation.test.tsx` (existing tests)

## Deliverables

### 1. Remove theme.ts imports from all 6 components
- [ ] `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\sim\components\flow-designer\animation\TokenAnimation.tsx`
- [ ] `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\sim\components\flow-designer\animation\CheckpointFlash.tsx`
- [ ] `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\sim\components\flow-designer\animation\NodePulse.tsx`
- [ ] `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\sim\components\flow-designer\animation\QueueBadge.tsx`
- [ ] `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\sim\components\flow-designer\animation\ResourceBar.tsx`
- [ ] `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\sim\components\flow-designer\animation\SimClock.tsx`

### 2. Replace all hardcoded colors with CSS variables

#### TokenAnimation.tsx (line 28)
- **Replace:** `color = colors.purple` (default prop value)
- **With:** `color = 'var(--sd-purple)'`

#### CheckpointFlash.tsx
- **Line 20:** `diamondColor = colors.purple` → `diamondColor = 'var(--sd-purple)'`
- **Line 21:** `checkmarkColor = colors.text` → `checkmarkColor = 'var(--sd-text-primary)'`
- **Line 79:** `filter: drop-shadow(0 0 4px ${diamondColor}88)` → Use CSS variables with alpha (see notes)
- **Line 82:** `filter: drop-shadow(0 0 12px ${diamondColor}dd)` → Use CSS variables with alpha
- **Line 118:** `rgba(0, 0, 0, 0.2)` → Keep (black shadow is acceptable for drop-shadow filters)

#### NodePulse.tsx
- **Line 18:** `color = colors.purple` → `color = 'var(--sd-purple)'`
- **Lines 22-24:** Remove hex-to-RGB parsing logic (parseInt color.slice)
- **Lines 30-36:** Replace computed rgba values with CSS variables:
  - Use `var(--sd-purple)` or appropriate color variable
  - Alpha values: use separate CSS variables like `var(--sd-purple-dim)` for semi-transparent variants
- **Line 46-51:** Same fix for drop-shadow filters

#### QueueBadge.tsx
- **Line 20:** `color = colors.red` → `color = 'var(--sd-red)'`
- **Line 21:** `textColor = colors.text` → `textColor = 'var(--sd-text-primary)'`
- **Line 51:** `rgba(${parseInt...})` → Use `var(--sd-shadow-md)` or create inline style without hardcoded rgba

#### ResourceBar.tsx
- **Line 25:** `barColor = colors.green` → `barColor = 'var(--sd-green)'`
- **Line 26:** `backgroundColor = colors.bgTerminal` → `backgroundColor = 'var(--sd-surface-alt)'`
- **Line 27:** `textColor = colors.text` → `textColor = 'var(--sd-text-primary)'`
- **Line 37:** `dynamicColor = colors.red` → `dynamicColor = 'var(--sd-red)'`
- **Line 39:** `dynamicColor = colors.orange` → `dynamicColor = 'var(--sd-orange)'`
- **Line 64:** `rgba(0, 0, 0, 0.1)` → `var(--sd-shadow-sm)`

#### SimClock.tsx
- **Line 88:** `backgroundColor: colors.bgTerminal` → `backgroundColor: 'var(--sd-surface-alt)'`
- **Line 89:** `border: colors.border` → `border: '1px solid var(--sd-border)'`
- **Line 92:** `color: colors.text` → `color: 'var(--sd-text-primary)'`
- **Line 94:** `rgba(0, 0, 0, 0.2)` → `var(--sd-shadow-xl)`
- **Line 101:** `colors.orange` → `'var(--sd-orange)'`
- **Line 101:** `colors.green` → `'var(--sd-green)'`
- **Line 110:** `colors.textMuted` → `'var(--sd-text-muted)'`
- **Line 122:** `colors.purpleDim` → `'var(--sd-purple-dim)'`
- **Line 123:** `colors.purple` → `'var(--sd-purple)'`
- **Line 132:** `colors.orange` → `'var(--sd-orange)'`
- **Line 132:** `colors.green` → `'var(--sd-green)'`
- **Line 150:** `${colors.green}66` → `'var(--sd-green-dim)'` or create CSS variable with appropriate alpha
- **Line 154:** `${colors.green}00` → `'transparent'`
- **Line 161:** `colors.green`, `colors.purple`, `colors.orange` → respective CSS variables

### 3. Handle dynamic RGBA construction
Where components currently construct rgba() values dynamically (NodePulse, QueueBadge):
- **Option A (preferred):** Use existing CSS variables with alpha variants (e.g., `--sd-purple-dim`, `--sd-purple-dimmer`)
- **Option B (fallback):** Use CSS `color-mix()` function if alpha blending is required
- **NOT ALLOWED:** Hex-to-RGB parsing and template literal rgba construction

### 4. Update test expectations
- [ ] Update `animation.test.tsx` line 120: Change test expectation from hardcoded rgb values to CSS variable check
- [ ] Verify test passes with CSS variables instead of hex/rgb values

## Test Requirements
- [ ] All 17 animation tests pass (currently 14 active + 3 skipped)
- [ ] All browser tests pass (1122 tests expected)
- [ ] No console warnings about invalid colors
- [ ] Visual regression check: Run `npm run dev` and verify animations render correctly

## Edge Cases
1. **Drop-shadow filters with alpha:** For `drop-shadow(0 0 4px ${color}88)` patterns, use CSS variables without alpha suffix since drop-shadow accepts colors natively
2. **Gradient stops with transparency:** Replace `${color}00` (fully transparent) with `transparent` keyword
3. **Box-shadow with rgba:** Use predefined shadow CSS variables (`--sd-shadow-sm`, `--sd-shadow-md`, etc.)

## Constraints
- No file over 500 lines (all animation files are under 200 lines)
- CSS: `var(--sd-*)` only — no hex, no rgb(), no named colors except `transparent`
- No stubs — all color references must be replaced
- TDD: Update test expectations FIRST, then fix components

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260316-TASK-148-RESPONSE.md`

The response MUST contain these 8 sections:
1. **Header** — task ID, title, status (COMPLETE/FAILED), model, date
2. **Files Modified** — every file created/modified/deleted, full paths
3. **What Was Done** — bullet list of concrete changes
4. **Test Results** — test files run, pass/fail counts
5. **Build Verification** — test/build output summary
6. **Acceptance Criteria** — copy from task, mark [x] or [ ]
7. **Clock / Cost / Carbon** — all three, never omit any
8. **Issues / Follow-ups** — edge cases, dependencies, next tasks

DO NOT skip any section.
