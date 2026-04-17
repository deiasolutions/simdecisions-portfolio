# SPEC: Rebuild terminal canvas wiring (types + useTerminal handler)

## Priority
P0.30

## Model Assignment
haiku

## Objective
Re-apply terminal canvas wiring from TASK-166 that was lost in a git reset.

### Changes needed
1. `browser/src/primitives/terminal/types.ts` — add 'canvas' to the routeTarget union type, add optional metrics field to relevant interface
2. `browser/src/primitives/terminal/useTerminal.ts` — add canvas mode handler block (was at lines 445-517, ~72 lines)

The canvas mode handler should:
- Detect when routeTarget is 'canvas'
- POST user input to `/api/canvas/chat` endpoint
- Handle the response (mutations, clarifications, errors)
- Display results in terminal output

## Recovery Sources
- `.deia/hive/responses/20260315-TASK-166-RESPONSE.md` (exact lines and implementation)
- `.deia/hive/tasks/2026-03-15-TASK-166-wire-canvas-route-target.md`
- `docs/specs/SPEC-TERMINAL-TO-CANVAS-WIRING.md` (architecture spec)
- `hivenode/routes/canvas_chat.py` (the endpoint it calls — survived as untracked)

**CRITICAL: Read the surviving test file — it IS the implementation spec:**
- `browser/src/primitives/terminal/__tests__/useTerminal.canvas.test.ts` — shows the exact routeTarget type, the API call pattern, the response handling, and all edge cases. This file survived and tells you exactly what useTerminal.ts needs to do.

## Acceptance Criteria
- [ ] 'canvas' is a valid routeTarget in types.ts
- [ ] useTerminal handles canvas mode with API call to /api/canvas/chat
- [ ] Existing terminal tests still pass
- [ ] New canvas terminal test(s) pass (check if test file exists in `browser/src/primitives/terminal/__tests__/useTerminal.canvas.test.ts`)
- [ ] No TypeScript errors

## Constraints
- Max 500 lines per file
- No stubs
- CSS: var(--sd-*) only
- POST heartbeats to http://localhost:8420/build/heartbeat every 3 minutes with JSON:
  {"task_id": "2026-03-15-1745-SPEC-rebuild-06-terminal-canvas", "status": "running", "model": "haiku", "message": "working"}

## File Claims (IMPORTANT — parallel bees)
Before modifying any file, claim it:
1. POST http://localhost:8420/build/claim with JSON:
   {"task_id": "2026-03-15-1745-SPEC-rebuild-06-terminal-canvas", "files": ["browser/src/primitives/terminal/types.ts", "browser/src/primitives/terminal/useTerminal.ts"]}
2. If response has conflicts (ok=false), poll GET http://localhost:8420/build/claims every 30s until yours.
