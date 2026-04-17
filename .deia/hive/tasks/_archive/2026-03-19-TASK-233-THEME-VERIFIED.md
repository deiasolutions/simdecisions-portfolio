# TASK-233: Theme Verified

## Objective
Scan all browser CSS and TSX files for hardcoded colors (hex, rgb, named colors) and replace with `var(--sd-*)` CSS variables to ensure theme consistency across ShiftCenter.

## Context
ShiftCenter uses a design token system defined in `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\shell-themes.css`. All colors MUST use `var(--sd-*)` variables. No hex, no rgb(), no named colors except `transparent`. Previous work (March 17, 2026) cleaned up hardcoded colors but was reverted during browser recovery. Some hardcoded colors may have crept back in.

**Previous offenders:**
- `browser/src/primitives/canvas/CanvasApp.tsx` had `#fef3c7` (fixed in RB4)
- Various primitives and shell components

**Design tokens location:** `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\shell-themes.css` (DO NOT MODIFY)

**Available variables include:**
- Background: `--sd-bg`, `--sd-surface`, `--sd-surface-alt`, `--sd-surface-hover`
- Borders: `--sd-border`, `--sd-border-hover`, `--sd-border-subtle`, `--sd-border-focus`, `--sd-border-muted`
- Text: `--sd-text-primary`, `--sd-text-secondary`, `--sd-text-muted`
- Colors: `--sd-purple`, `--sd-green`, `--sd-orange`, `--sd-cyan`, `--sd-red` (plus `-dim` variants)
- Glass: `--sd-glass-bg`, `--sd-glass-bg-heavy`, `--sd-glass-blur`
- Shadows: `--sd-shadow-sm`, `--sd-shadow-md`, `--sd-shadow-lg`, `--sd-shadow-xl`, `--sd-shadow-2xl`
- Many more (see shell-themes.css for full list)

## Files to Read First
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\shell-themes.css` (design tokens reference)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\canvas\CanvasApp.tsx` (known prior offender)
- Scan all `*.tsx`, `*.ts`, `*.css` files in `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\`

## Strategy
1. Use grep/ripgrep to find all hardcoded colors:
   - Hex: `#[0-9a-fA-F]{3,8}` (but NOT in comments or URLs)
   - RGB/RGBA: `rgba?\(`
   - Named colors: common CSS color names (white, black, red, blue, etc.) — EXCEPT `transparent`
2. For each match:
   - Read the file
   - Identify the appropriate `--sd-*` variable
   - Replace the hardcoded value with `var(--sd-*)`
3. **MAX 10 files modified** — if more than 10 files have hardcoded colors, document them and fix only the 10 most critical files (highest occurrence count)
4. Document all findings in the response file

## Files You May Modify
Any `.tsx`, `.ts`, or `.css` file in `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\` that contains hardcoded colors.

**Maximum files:** 10 (if more than 10 files have issues, prioritize by occurrence count)

## Files You Must NOT Modify
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\shell-themes.css` (design tokens are correct)
- Any files in `hivenode/` (backend)
- Any files in `engine/` (backend)
- Any files in `_tools/` (tooling)
- Any files in `.deia/` (hive)
- Any test files that assert specific hardcoded colors for test purposes (document them instead)

## Deliverables
- [ ] Grep/ripgrep scan results showing all hardcoded colors found
- [ ] List of all files containing hardcoded colors (with occurrence counts)
- [ ] For each modified file: before/after diff showing replacements
- [ ] Summary: total files scanned, total files with issues, total files modified, total replacements made
- [ ] If zero hardcoded colors found, document the verification

## Test Requirements
**Minimum tests:** 0 (verification task)

However:
- [ ] All existing tests MUST still pass after color replacements
- [ ] Visual regression testing is NOT required (this is a CSS variable substitution — output is identical)
- [ ] Build MUST succeed

## Build Verification
After making changes:
```bash
# Frontend tests
cd C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser && npx vitest run

# Frontend build
cd C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser && npm run build
```

Include test summary and last 5 lines of build output in response file.

## Constraints
- No file over 500 lines (if a file exceeds this after edits, modularize it)
- NO hardcoded colors — this is the entire point of the task
- NO stubs — all replacements must be complete
- Document any edge cases (e.g., hardcoded colors in test assertions, data-uri-encoded images, external library CSS)

## Response Requirements — MANDATORY
When you finish your work, write a response file:
  `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260319-TASK-233-RESPONSE.md`

The response MUST contain these 8 sections:
1. **Header** — task ID, title, status (COMPLETE/FAILED), model, date
2. **Files Modified** — every file created/modified/deleted, full paths
3. **What Was Done** — bullet list of concrete changes (not intent)
4. **Test Results** — test files run, pass/fail counts
5. **Build Verification** — test/build output summary
6. **Acceptance Criteria** — copy from task, mark [x] or [ ]
7. **Clock / Cost / Carbon** — all three, never omit any
8. **Issues / Follow-ups** — edge cases, dependencies, next tasks

DO NOT skip any section.

## Acceptance Criteria
- [ ] All `.tsx`, `.ts`, `.css` files in `browser/src/` scanned for hardcoded colors
- [ ] All hardcoded colors replaced with `var(--sd-*)` variables (or documented if in test assertions)
- [ ] All existing tests pass
- [ ] Build succeeds
- [ ] Response file documents: files scanned, files with issues, files modified, total replacements
- [ ] If more than 10 files had issues, response documents all issues + rationale for which 10 were prioritized

## Model Assignment
haiku

## Risk
LOW — CSS variable substitution with no logic changes
