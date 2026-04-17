# REGENT REVIEW: TASK-MON-001 — CORRECTION CYCLE 1

**Status:** CORRECTIONS REQUIRED
**Reviewer:** Q33NR (REGENT-QUEUE-TEMP-2026-03-24-SPEC-MON)
**Date:** 2026-03-24
**Cycle:** 1 of 2

---

## Mechanical Review Checklist Results

| Check | Result | Notes |
|-------|--------|-------|
| ✅ Deliverables match spec | PASS | All spec acceptance criteria have corresponding task deliverables |
| ❌ File paths are absolute | **FAIL** | **Relative paths used — must be absolute per Rule 8** |
| ✅ Test requirements present | PASS | 8+ tests specified with concrete scenarios |
| ✅ CSS uses var(--sd-*) | PASS | Constraint stated clearly in two locations |
| ✅ No file over 500 lines | PASS | Constraint stated |
| ⚠️ No stubs/TODOs | MINOR | Wording could be clearer (see note below) |
| ✅ Response template | PASS | All 8 sections + YAML frontmatter specified |

---

## Required Corrections

### CRITICAL: Convert all file paths to absolute format

**Location:** Lines 82-92 (File Locations section)

**Current (relative paths):**
```
browser/src/primitives/code-editor/
  MonacoApplet.tsx
  MonacoApplet.css
  monacoAppletAdapter.ts
  index.ts
  __tests__/
    MonacoApplet.test.tsx
```

**Required (absolute paths):**
```
C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\code-editor\MonacoApplet.tsx
C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\code-editor\MonacoApplet.css
C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\code-editor\monacoAppletAdapter.ts
C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\code-editor\index.ts
C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\code-editor\__tests__\MonacoApplet.test.tsx
```

**Why this matters:** Rule 8 requires absolute paths in all task docs and specs. Bees need unambiguous file locations.

---

## Optional Clarification (Minor)

**Location:** Lines 23-25 (Context section)

**Current wording:**
> **Hard constraint:** Monaco has zero direct filesystem access. All I/O is through the Named
> Volume System adapter (TASK-MON-002). This task wires the component shell only — file load/save
> stubs are left for MON-002 to implement.

**Suggested clarification:**
> **Hard constraint:** Monaco has zero direct filesystem access. All I/O is through the Named
> Volume System adapter (TASK-MON-002). This task wires the component shell only. The `getValue()` and `setValue()` methods work with in-memory editor content (not stubs — Monaco provides these). File load/save from Named Volumes is TASK-MON-002's responsibility (separate concern, not a stub).

**Why:** The current wording "stubs are left for MON-002" could be misread as violating Rule 6 (NO STUBS). The clarification emphasizes that getValue/setValue are fully functional (work with Monaco's in-memory content), and file I/O is a separate layer.

**This is NOT a blocking issue** — the task does not actually violate the no-stubs rule. But the clarification prevents confusion.

---

## What Passes Review

The following aspects are solid and require no changes:

1. **Deliverables coverage** — Every spec acceptance criterion maps to a task deliverable
2. **Test requirements** — Specific scenarios listed, minimum 8 tests required
3. **CSS constraint** — var(--sd-*) only, stated twice for clarity
4. **File size constraint** — 500-line limit stated
5. **Response template** — All 8 sections + YAML frontmatter detailed
6. **TDD enforcement** — "write tests before implementation" stated clearly
7. **Reference files** — terminalAdapter.tsx pattern specified
8. **Scope boundaries** — Clear distinction between MON-001 (component shell) and MON-002 (volume I/O)

---

## Next Steps

**Q33N:** Fix the file paths (convert to absolute) in the task file. Optionally clarify the "stubs" wording. Resubmit for Cycle 2 review.

**After corrections:** Q33NR will re-review and approve dispatch if no further issues.

---

## Correction Cycle Status

- ✅ Cycle 1: CORRECTIONS REQUIRED (file paths)
- ⏸️ Cycle 2: Pending resubmission
- 🔄 Max cycles: 2 (per HIVE.md correction cycle rule)

If issues persist after Cycle 2, task will be approved with `⚠️ APPROVED_WITH_WARNINGS` flag and bees will expose any remaining issues empirically.
