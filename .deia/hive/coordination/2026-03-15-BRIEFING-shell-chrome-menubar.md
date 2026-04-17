# BRIEFING: Port shell chrome MenuBar + ShellTabBar + WorkspaceBar

**From:** Q33NR
**To:** Q33N (Queen Coordinator)
**Date:** 2026-03-15
**Spec ID:** 2026-03-15-1332-SPEC-w1-12-shell-chrome-menubar
**Model Assignment:** sonnet
**Priority:** P0.60

---

## Objective

Port 3 shell chrome components from platform to shiftcenter:
1. **MenuBar** — app menu with File/Edit/View/Help structure
2. **ShellTabBar** — workspace tabs component
3. **WorkspaceBar** — workspace selector component

Total: ~906 lines source code.

---

## Context from Q88N

This is part of W1 (Week 1) shell chrome buildout. Previous tasks in this series have ported other chrome components. These 3 components complete the core shell UI.

The source repo is `platform/` (sibling directory to shiftcenter). The components are in `platform/shell/components/`.

Target location: `browser/src/shell/components/`

---

## Source Files

Check these paths in the platform repo:
- `platform/shell/components/MenuBar.tsx`
- `platform/shell/components/ShellTabBar.tsx`
- `platform/shell/components/WorkspaceBar.tsx`

Also check for corresponding test files:
- `platform/shell/components/__tests__/MenuBar.test.tsx`
- `platform/shell/components/__tests__/ShellTabBar.test.tsx`
- `platform/shell/components/__tests__/WorkspaceBar.test.tsx`

---

## Target Files

The ported components go here:
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\components\MenuBar.tsx`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\components\ShellTabBar.tsx`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\components\WorkspaceBar.tsx`

Tests go here:
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\components\__tests__\MenuBar.test.tsx`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\components\__tests__\ShellTabBar.test.tsx`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\components\__tests__\WorkspaceBar.test.tsx`

---

## Existing Ported Components

WorkspaceBar has ALREADY been ported (see git status: `M browser/src/shell/components/WorkspaceBar.tsx`). Check if it needs updates or if it's complete.

Check `browser/src/shell/components/` for what already exists:
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\components\`

Do NOT re-port what's already there. Only port what's missing or incomplete.

---

## Key Constraints (from 10 Hard Rules)

1. **TDD:** Tests first, then implementation (Rule 5)
2. **No file over 500 lines** (Rule 4)
3. **CSS: var(--sd-*) only** — no hex, no rgb(), no named colors (Rule 3)
4. **No stubs** — every function fully implemented (Rule 6)
5. **Absolute paths** in all task files (Rule 8)

---

## Acceptance Criteria (from Spec)

- [ ] MenuBar component ported with menu structure
- [ ] ShellTabBar component ported
- [ ] WorkspaceBar component ported (CHECK IF ALREADY DONE)
- [ ] All use var(--sd-*) CSS variables
- [ ] Tests written and passing

---

## Test Requirements

From spec smoke test:
```bash
cd browser && npx vitest run src/shell/components/__tests__/
```

All tests must pass. No new failures.

---

## Heartbeat Requirement

Task must POST heartbeats to `http://localhost:8420/build/heartbeat` every 3 minutes:
```json
{
  "task_id": "2026-03-15-1332-SPEC-w1-12-shell-chrome-menubar",
  "status": "running",
  "model": "sonnet",
  "message": "working"
}
```

Include this in the task file.

---

## Your Next Steps

1. **Read the source files** in platform repo to understand what needs to be ported
2. **Read the target directory** in shiftcenter to see what's already ported
3. **Write task files** for bees (likely 1-3 tasks, depending on what's missing)
4. **Return task files to Q33NR for review** — DO NOT dispatch bees yet
5. **Wait for Q33NR approval** before dispatching

---

## Questions to Answer Before Writing Tasks

- Is WorkspaceBar already complete? (It's been modified — check if it matches platform source)
- Are MenuBar and ShellTabBar missing entirely?
- Are there existing test files for WorkspaceBar?
- What dependencies do these components have? (hooks, services, types)
- Do the components reference any platform-specific imports that need to be adapted?

---

## Model Assignment

Use **sonnet** for this coordination work. Assign **haiku** or **sonnet** to bees based on complexity:
- Simple port (no logic changes): haiku
- Complex port (API changes, refactoring): sonnet

---

## Success Criteria

When Q33N returns:
- Task files are complete with all 8 required sections
- Deliverables are concrete and measurable
- Test requirements are specific (edge cases listed)
- File paths are absolute
- No vague acceptance criteria

When bees complete:
- All tests pass
- No stubs shipped
- CSS uses var(--sd-*) only
- No file exceeds 500 lines
- Response files have all 8 sections

---

**Q33N: Read this briefing, explore the codebase, write task files, return to Q33NR for review.**
