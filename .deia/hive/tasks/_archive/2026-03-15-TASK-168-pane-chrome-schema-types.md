# TASK-168: Add Pane Chrome Option Types

## Objective
Extend EGG schema and shell types to support three new chrome options per pane: `chromeClose`, `chromePin`, `chromeCollapsible`.

## Context
BL-151 requires granular control over pane chrome behavior:
- `chromeClose` (boolean) — show/hide close X button
- `chromePin` (boolean) — enable pin toggle (when pinned, pane takes full width, sibling collapses)
- `chromeCollapsible` (boolean) — enable collapse toggle (pane can shrink to ~34px icon strip)

These are configured per-pane in EGG layout and passed to shell pane renderer.

## Files to Read First
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\eggs\types.ts`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\types.ts`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\eggToShell.ts`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\docs\specs\SPEC-EGG-SCHEMA-v1.md`

## Deliverables
- [ ] Add `chromeClose`, `chromePin`, `chromeCollapsible` optional boolean fields to `EggLayoutNode` interface in `browser/src/eggs/types.ts`
- [ ] Add `chromeOptions` field to `AppNode` interface in `browser/src/shell/types.ts`:
  ```typescript
  interface ChromeOptions {
    close?: boolean;
    pin?: boolean;
    collapsible?: boolean;
  }
  ```
- [ ] Update `eggLayoutToShellTree()` in `browser/src/shell/eggToShell.ts` to read chrome options from EGG pane config and set them on AppNode:
  ```typescript
  chromeOptions: {
    close: eggNode.chromeClose ?? true,
    pin: eggNode.chromePin ?? false,
    collapsible: eggNode.chromeCollapsible ?? false,
  }
  ```
- [ ] Update SPEC-EGG-SCHEMA-v1.md to document the three new optional pane properties

## Test Requirements
- [ ] Tests written FIRST (TDD)
- [ ] Test `eggLayoutToShellTree()` correctly reads chrome options from EGG config and sets defaults
- [ ] Test AppNode has correct chromeOptions shape
- [ ] All tests pass
- [ ] Edge cases:
  - Chrome options undefined → defaults (close: true, pin: false, collapsible: false)
  - Chrome options explicitly set → values preserved
  - Seamless panes still work (existing behavior)

## Constraints
- No file over 500 lines
- CSS: var(--sd-*) only (not applicable — types only)
- No stubs
- All file paths must be absolute

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260315-TASK-168-RESPONSE.md`

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

## Build Heartbeat
POST to http://localhost:8420/build/heartbeat every 3 minutes with JSON:
```json
{"task_id": "TASK-168", "status": "running", "model": "haiku", "message": "working"}
```

## File Claim
POST to http://localhost:8420/build/claim before modifying files with JSON:
```json
{"task_id": "TASK-168", "files": ["browser/src/eggs/types.ts", "browser/src/shell/types.ts", "browser/src/shell/eggToShell.ts", "docs/specs/SPEC-EGG-SCHEMA-v1.md"]}
```
