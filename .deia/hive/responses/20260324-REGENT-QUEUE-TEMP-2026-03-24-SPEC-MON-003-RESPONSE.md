# REGENT-QUEUE-TEMP-2026-03-24-SPEC-MON-003: Task File Review -- NEEDS_CORRECTION

**Status:** NEEDS_CORRECTION (cycle 1/2)
**Model:** Sonnet
**Date:** 2026-03-24

---

## Review Summary

Task file `.deia/hive/queue/_stage/2026-03-24-TASK-MON-003-monaco-relay-bus.md` reviewed.

**Result:** RETURN TO Q33N for correction before dispatch.

---

## Mechanical Checklist Results

- [x] Deliverables match spec (monacoRelayBus.ts, MonacoApplet.tsx, tests)
- [ ] **File paths are absolute** — VIOLATION (relative paths used)
- [x] Test requirements present (min 10 tests, TDD, specific scenarios)
- [x] CSS uses var(--sd-*) only (N/A — no CSS in this task)
- [x] No file over 500 lines (constraint explicitly stated)
- [x] No stubs or TODOs (full interface specified)
- [x] Response file template present (8 sections + YAML frontmatter)

---

## Issues Found

### BLOCKING: File Paths Not Absolute

**Rule 8 from BOOT.md:** "All file paths must be absolute in task docs and specs."

**Current (incorrect):**
```
browser/src/primitives/code-editor/
  monacoRelayBus.ts
  MonacoApplet.tsx
  __tests__/
    monacoRelayBus.test.ts
```

**Required (absolute paths):**
```
C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\code-editor\
  monacoRelayBus.ts
  MonacoApplet.tsx
  __tests__\
    monacoRelayBus.test.ts
```

Also update the "Scope" section:
- "Build `browser/src/primitives/code-editor/monacoRelayBus.ts`" → "Build `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\code-editor\monacoRelayBus.ts`"
- "Wire into MonacoApplet.tsx" → "Wire into `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\code-editor\MonacoApplet.tsx`"

---

## Correction Required

**Q33N: Fix file paths to be absolute throughout the task file.**

Replace every occurrence of:
- `browser/src/primitives/code-editor/` → `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\code-editor\`

Then resubmit for approval.

---

## What Works Well

- Acceptance criteria comprehensive and testable
- TDD approach mandated
- Debounce and loop-guard scenarios explicitly called out
- Response file requirements complete (8 sections + YAML)
- File size constraint present
- Depends-on relationship documented

---

## Next Steps

1. Q33N corrects file paths in TASK-MON-003
2. Q33N resubmits for review
3. If clean: approve dispatch
4. If still issues: correction cycle 2/2

---

## Correction Cycle Status

**Cycle:** 1/2
**Max cycles before forced approval:** 2
