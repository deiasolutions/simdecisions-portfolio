# TRIAGE ESCALATION: MW-058

**Date:** 2026-04-12 19:07:40 UTC
**Reason:** 3 requeue attempts (max 3)
**Status:** NEEDS MANUAL REVIEW

## Summary

Spec `SPEC-MW-058-queue-data-connection.md` has been requeued 3 times and failed each time.
Automated triage has moved it to `_escalated/` for manual review.

## Triage History

- 2026-04-12T18:52:40.087925Z — requeued (empty output)
- 2026-04-12T18:57:40.145450Z — requeued (empty output)
- 2026-04-12T19:02:40.232784Z — requeued (empty output)

## Next Steps

1. **Review spec file** in `queue/_escalated/SPEC-MW-058-queue-data-connection.md`
2. **Diagnose root cause** — why is this spec failing repeatedly?
3. **Options:**
   - Fix spec and move back to backlog/
   - Archive spec if no longer needed
   - Break into smaller specs
   - Escalate to architect (Mr. AI) if systemic issue

## Original Spec

```markdown
## Clean Retry

**Previous attempt failed with no output.**

This is a clean retry — start from scratch. Check logs if available to
understand why the previous attempt failed.

---

## Clean Retry

**Previous attempt failed with no output.**

This is a clean retry — start from scratch. Check logs if available to
understand why the previous attempt failed.

---

## Clean Retry

**Previous attempt failed with no output.**

This is a clean retry — start from scratch. Check logs if available to
understand why the previous attempt failed.

---

# SPEC-MW-058-queue-data-connection: Fix queue pane showing "Waiting for data" on workdesk

## Priority
P1

## Depends On
None

## Model Assignment
sonnet

## Objective

On the workdesk set, the Queue pane (appType `tree-browser` with adapter `bus`) shows "Waiting for data..." and never loads any queue items. The workdesk queue is configured with `"adapter": "bus"`, `"busEvent": "build:runner-updated"`, meaning it expects queue data to arrive via the relay bus. Investigate why no data arrives. Possible causes: 1) The backend is not emitting `build:runner-updated` bus events, 2) The tree-browser bus adapter is not subscribing correctly, 3) The bus connection is not established on the production deployment, 4) The data format from the bus does not match what the tree-browser expects. Find the root cause and fix it so the queue pane shows the actual factory queue state.

## Files to Read First

- browser/src/primitives/tree-browser/TreeBrowser.tsx
- browser/src/apps/treeBrowserAdapter.tsx
- browser/src/primitives/tree-browser/adapters/busAdapter.ts
- browser/sets/workdesk.set.md
- hivenode/routes/des_routes.py

## Acceptance Criteria

- [ ] The Queue pane on workdesk loads and displays queue items (specs in backlog, active, done)
- [ ] The queue refreshes when new specs are added or status changes
- [ ] If the backend is not reachable, the queue shows a clear error message instead of "Waiting for data..."
- [ ] The search box filters queue items when text is entered
- [ ] No TypeScript compilation errors (`npx tsc --noEmit` passes)

## Smoke Test

- [ ] Open `http://localhost:5173/?set=workdesk` with backend running — verify queue pane shows spec items
- [ ] If backend is not running, verify a connection error is shown instead of indefinite "Waiting for data..."

## Constraints

- No file over 500 lines
- No stubs — every function complete
- No git operations
- Use var(--sd-*) CSS variables only
- Do not change the queue pane config in workdesk.set.md unless the bus adapter approach is fundamentally broken

## Triage History
- 2026-04-12T18:52:40.087925Z — requeued (empty output)
- 2026-04-12T18:57:40.145450Z — requeued (empty output)
- 2026-04-12T19:02:40.232784Z — requeued (empty output)

```

---

**Automated escalation by triage daemon**
