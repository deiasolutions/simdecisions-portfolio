# TASK-E: Generate MW Spec Files — Phase 5 Mobile CSS

## Objective
Generate spec files for Phase 5 mobile CSS tasks. These are pure CSS optimization tasks for existing primitives to make them mobile-friendly. Total: 11 spec files.

## Context
Phase 5 tasks add mobile CSS to existing primitives. No new components — just responsive breakpoints, touch-optimized spacing, safe area handling, and mobile-specific layouts.

**Phase 5 (Mobile CSS):**
- MW-023: BUILD: text-pane mobile CSS
- MW-024: BUILD: terminal mobile CSS + pills
- MW-025: BUILD: tree-browser mobile CSS
- MW-026: BUILD: efemera-connector mobile CSS
- MW-027: BUILD: settings mobile CSS
- MW-028: BUILD: dashboard mobile CSS
- MW-029: BUILD: progress-pane polish
- MW-030: BUILD: top-bar mobile CSS
- MW-031: BUILD: menu-bar → drawer
- MW-032: BUILD: status-bar mobile CSS
- MW-033: BUILD: command-palette mobile overlay

## Files to Read First
- `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/hivenode/scheduler/scheduler_mobile_workdesk.py` — task registry
- `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/.deia/hive/queue/_active/SPEC-MW-S01-command-interpreter.md` — spec template
- `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/browser/src/primitives/text-pane/` — existing text-pane component + CSS
- `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/browser/src/primitives/terminal/` — existing terminal component + CSS
- `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/browser/src/primitives/tree-browser/` — existing tree-browser component + CSS
- `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/browser/src/primitives/efemera-connector/` — existing connector component + CSS (if it exists yet)
- `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/browser/src/shell/` — top-bar, menu-bar, status-bar components
- `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/browser/src/primitives/command-palette/` — existing command-palette
- `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/browser/src/styles/` — global CSS variables, theme CSS

## Deliverables
Write 11 spec files to `.deia/hive/queue/backlog/`:
- [ ] `SPEC-MW-023-text-pane-mobile-css.md`
- [ ] `SPEC-MW-024-terminal-mobile-css.md`
- [ ] `SPEC-MW-025-tree-browser-mobile-css.md`
- [ ] `SPEC-MW-026-efemera-connector-mobile-css.md`
- [ ] `SPEC-MW-027-settings-mobile-css.md`
- [ ] `SPEC-MW-028-dashboard-mobile-css.md`
- [ ] `SPEC-MW-029-progress-pane-polish.md`
- [ ] `SPEC-MW-030-top-bar-mobile-css.md`
- [ ] `SPEC-MW-031-menu-bar-drawer.md`
- [ ] `SPEC-MW-032-status-bar-mobile-css.md`
- [ ] `SPEC-MW-033-command-palette-mobile.md`

## Spec Writing Guidelines
CSS-only specs are different from BUILD specs:
1. **No tests required** (CSS is visual — smoke test via browser)
2. **Constraints:** Use ONLY `var(--sd-*)` CSS variables. NO hardcoded colors, NO rgb(), NO hex.
3. **Mobile breakpoints:** Use `@media (max-width: 768px)` for tablet, `@media (max-width: 480px)` for phone.
4. **Safe area:** Use `env(safe-area-inset-*)` for notched devices.
5. **Touch targets:** Minimum 48px tap targets (buttons, links, interactive elements).
6. **Deliverables:** Describe the CSS changes, new classes, responsive behavior.

**Example spec structure for CSS task:**
- **Objective:** Add mobile CSS to [component] to make it touch-friendly and responsive.
- **Context:** Describe current desktop layout, what needs to change on mobile (font sizes, spacing, layout direction, hidden elements).
- **Files to Read First:** Existing CSS file, component JSX/TSX.
- **Acceptance Criteria:**
  - [ ] Add `@media (max-width: 768px)` breakpoint
  - [ ] Reduce font sizes for mobile (e.g., 16px → 14px)
  - [ ] Increase touch targets to 48px minimum
  - [ ] Use `env(safe-area-inset-bottom)` for bottom elements
  - [ ] Hide non-essential elements on mobile (if applicable)
  - [ ] Test on Chrome DevTools mobile emulator
- **Smoke Test:** Open component on 375px viewport, verify layout doesn't break, text is readable, buttons are tappable.
- **Model Assignment:** "sonnet" (CSS tasks benefit from codebase understanding)
- **Constraints:** CSS only (no JSX changes unless required for class names), no hardcoded colors, max 200 lines of new CSS per file.

**MW-024 (terminal + pills):** This is special — adds pill UI for command suggestions. Not just CSS, but also JSX for pill rendering. Make this clear in the spec.

**MW-031 (menu-bar → drawer):** This is structural — convert menu-bar to a slide-out drawer on mobile. Requires JSX changes + CSS animation.

**MW-033 (command-palette mobile):** Fullscreen overlay on mobile instead of centered modal. Requires JSX + CSS changes.

## Test Requirements
N/A — CSS specs don't have automated tests. Smoke test is manual browser testing.

## Acceptance Criteria
- [ ] 11 spec files created in `.deia/hive/queue/backlog/`
- [ ] Each spec is 40-70 lines (CSS specs are shorter)
- [ ] Each spec clearly describes what CSS changes are needed
- [ ] "Files to Read First" lists existing component CSS files
- [ ] Dependencies: Phase 5 has NO dependencies (can start at t=0 per scheduler)
- [ ] All specs use "sonnet" model
- [ ] Naming: `SPEC-MW-{ID}-{component}-mobile-css.md`

## Smoke Test
- [ ] All 11 files exist in `.deia/hive/queue/backlog/`
- [ ] Each file has required sections (no "Test Requirements" section for CSS)
- [ ] Open MW-023 spec — describes specific CSS changes to text-pane (e.g., padding reduction, font size adjustment)
- [ ] Open MW-031 spec — describes drawer animation, JSX changes for slide-out menu

## Constraints
- Output location: `.deia/hive/queue/backlog/`
- Each spec: 40-70 lines
- NO STUBS — write real content
- Read existing CSS files first
- CSS-only specs don't need "Test Requirements" section
- Use absolute paths

## Response Requirements — MANDATORY
When you finish your work, write a response file:
  `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/.deia/hive/responses/20260405-TASK-E-MW-SPECS-PHASE5-RESPONSE.md`

The response MUST contain these 8 sections:
1. **Header** — task ID, title, status (COMPLETE/FAILED), model, date
2. **Files Modified** — every file created/modified/deleted, full paths
3. **What Was Done** — bullet list of concrete changes
4. **Test Results** — N/A
5. **Build Verification** — N/A
6. **Acceptance Criteria** — copy from task, mark [x] or [ ]
7. **Clock / Cost / Carbon** — all three, never omit any
8. **Issues / Follow-ups** — edge cases, dependencies, next tasks

DO NOT skip any section.
