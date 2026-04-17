# Q33N Report: TASK-236-REQUEUE Task File Ready for Review

**From:** Q33N (Queen Coordinator)
**To:** Q33NR (Queen Regent)
**Date:** 2026-03-18
**Status:** AWAITING Q33NR APPROVAL

---

## Summary

Task file created for TASK-236-REQUEUE (Error States Integration). However, I discovered a **CRITICAL INACCURACY** in the briefing that required a scope adjustment.

---

## Critical Finding: Briefing Was Outdated

**The briefing stated:**
> "The previous bee created excellent error infrastructure but only wired it into ONE error path out of ~5."

**The reality (after reading useTerminal.ts):**
- ✅ Line 413-419: Shell execution errors — ALREADY uses `classifyError()` + `getErrorMessage()`
- ✅ Line 560-567: Canvas routing errors — ALREADY uses `classifyError()` + `getErrorMessage()`
- ✅ Line 764-780: Main LLM request errors — ALREADY uses `classifyError()` + `getErrorMessage()`

**3 out of 4 critical error paths are ALREADY integrated.** The briefing's line number references were outdated.

---

## Actual Scope (Corrected)

The task file I created focuses on what's **actually** missing:

1. **PaneErrorBoundary integration** — still shows raw `error.message`, needs classifier
2. **Test coverage** — existing integrations have no test coverage

**NOT included in task (already complete):**
- useTerminal.ts error path integration (already done)
- Shell execution error classifier integration (already done)
- Canvas routing error classifier integration (already done)

---

## Task File Details

**File created:** `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\tasks\2026-03-18-TASK-236-REQUEUE-error-states-integration.md`

**Deliverables:**
1. Integrate error classifier into PaneErrorBoundary (5 changes)
2. Add test coverage for useTerminal.ts error paths (new file, 8+ tests)
3. Add test coverage for PaneErrorBoundary error classification (new file, 6+ tests)

**Test requirements:**
- All existing error tests still pass (3 files)
- New tests: 14+ tests across 2 new test files
- TDD approach: tests first, then implementation

**Constraints enforced:**
- No file over 500 lines
- CSS: `var(--sd-*)` only
- No stubs
- TDD required
- Response file with all 8 sections

---

## Files the Bee Will Modify

1. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\components\PaneErrorBoundary.tsx` (modify)
2. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\terminal\__tests__\useTerminal.errorPaths.test.tsx` (create)
3. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\components\__tests__\PaneErrorBoundary.errorClassifier.test.tsx` (create)

---

## Smoke Test Commands

```bash
# Existing error tests (must still pass)
cd browser && npx vitest run --reporter=verbose src/primitives/terminal/__tests__/errorClassifier.test.ts
cd browser && npx vitest run --reporter=verbose src/primitives/terminal/__tests__/errorMessages.test.ts
cd browser && npx vitest run --reporter=verbose src/primitives/terminal/__tests__/errorIntegration.test.tsx

# New tests
cd browser && npx vitest run --reporter=verbose src/primitives/terminal/__tests__/useTerminal.errorPaths.test.tsx
cd browser && npx vitest run --reporter=verbose src/shell/components/__tests__/PaneErrorBoundary.errorClassifier.test.tsx
```

---

## Questions for Q33NR

1. **Is the corrected scope acceptable?** The briefing requested useTerminal.ts integration, but that's already complete. The task file focuses on PaneErrorBoundary + tests.

2. **Should I note the briefing inaccuracy in coordination/?** This seems like feedback that should flow back to you.

3. **Are 14+ new tests sufficient?** (8 for useTerminal error paths, 6 for PaneErrorBoundary)

---

## Next Steps

Awaiting Q33NR review and approval before dispatching bee.

**Dispatch command (when approved):**
```bash
python .deia/hive/scripts/dispatch/dispatch.py .deia/hive/tasks/2026-03-18-TASK-236-REQUEUE-error-states-integration.md --model sonnet --role bee --inject-boot
```

---

## End of Report
