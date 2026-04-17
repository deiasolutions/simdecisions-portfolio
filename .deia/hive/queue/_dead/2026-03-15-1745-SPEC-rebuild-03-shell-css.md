# SPEC: Rebuild shell CSS fixes + menu bar dropdown CSS

## Priority
P0.15

## Model Assignment
haiku

## Objective
Two CSS rebuilds needed:

### Part A: Fix 4 hardcoded rgba() violations (TASK-158 redo)
In `browser/src/shell/components/ShellTabBar.tsx`:
- Line ~150: Replace `rgba(0, 0, 0, 0.15)` with `var(--sd-shadow-sm)` (box shadow)

In `browser/src/shell/components/WorkspaceBar.tsx`:
- Line ~57: Replace `rgba(139,92,246,0.06)` with `var(--sd-accent-subtle)` (UndoRedoButtons hover)
- Line ~146: Replace `rgba(139,92,246,0.06)` with `var(--sd-accent-subtle)` (ActivePaneIndicator bg)
- Line ~230: Replace `rgba(0,0,0,0.5)` with `var(--sd-shadow-xl)` (ThemeToggle menu shadow)

### Part B: Add menu bar dropdown CSS from platform
Append missing CSS rules to `browser/src/shell/components/shell.css` AFTER the existing `.menu-divider` block. The source is `platform/simdecisions-2/src/components/shell/shell.css` lines 565-730.

Missing classes: `.menu-item`, `.menu-button`, `.menu-button.active`, `.menu-dropdown`, `.menu-dropdown-item`, `.menu-dropdown-item:hover`, `.menu-dropdown-item:disabled`, `.menu-dropdown-item.submenu`, `.menu-submenu`, `.menu-modal-overlay`, `.menu-modal`, `.menu-modal h3`, `.menu-modal-content`, `.menu-modal-content p`, `.menu-modal-content strong`, `.menu-modal-close`, `.menu-modal::-webkit-scrollbar*`

Read the platform file to get exact CSS. All colors must use `var(--sd-*)` variables — no hex, no rgb, no named colors.

## Recovery Sources
- `.deia/hive/responses/20260315-TASK-158-RESPONSE.md` (exact line numbers and replacements for Part A)
- `platform/simdecisions-2/src/components/shell/shell.css` lines 551-730 (Part B source)
- `docs/specs/SPEC-PORT-SHELL-001-shell-chrome-port.md` (shell chrome spec)

## Acceptance Criteria
- [ ] Zero hardcoded colors in ShellTabBar.tsx and WorkspaceBar.tsx
- [ ] Menu bar dropdowns have CSS rules in shell.css
- [ ] `grep -E "(#[0-9a-fA-F]{3,6}|rgb\(|rgba\(|hsl\()" ShellTabBar.tsx WorkspaceBar.tsx` returns nothing
- [ ] `cd browser && npx vitest run src/shell/components/__tests__/MenuBar.test.tsx src/shell/components/__tests__/ShellTabBar.test.tsx src/shell/components/__tests__/WorkspaceBar.test.tsx` — all pass
- [ ] No regressions

## Constraints
- CSS: var(--sd-*) only. No hex, no rgb(), no named colors.
- Max 500 lines per file
- POST heartbeats to http://localhost:8420/build/heartbeat every 3 minutes with JSON:
  {"task_id": "2026-03-15-1745-SPEC-rebuild-03-shell-css", "status": "running", "model": "haiku", "message": "working"}

## File Claims (IMPORTANT — parallel bees)
Before modifying any file, claim it:
1. POST http://localhost:8420/build/claim with JSON:
   {"task_id": "2026-03-15-1745-SPEC-rebuild-03-shell-css", "files": ["browser/src/shell/components/shell.css", "browser/src/shell/components/ShellTabBar.tsx", "browser/src/shell/components/WorkspaceBar.tsx"]}
2. If response has conflicts (ok=false), poll GET http://localhost:8420/build/claims every 30s until yours.
