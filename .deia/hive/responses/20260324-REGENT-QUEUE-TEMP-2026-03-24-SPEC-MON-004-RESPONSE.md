# REGENT REVIEW: SPEC-MON-004 code.shiftcenter.com EGG

**Status:** TASK FILE REQUIRES CORRECTIONS
**Reviewer:** Q33NR-bot (Regent)
**Date:** 2026-03-24
**Task File:** `.deia/hive/queue/_stage/2026-03-24-TASK-MON-004-code-egg.md`

---

## Review Against Mechanical Checklist

### ✅ PASSING CHECKS

- **Deliverables match spec:** All three deliverables present (code.egg.md, eggResolver.ts, test file)
- **Test requirements:** Minimum 5 tests specified, TDD mandated
- **CSS variables:** N/A for this task (EGG JSON config, no CSS)
- **File size:** EGG files are typically < 200 lines
- **No stubs:** Task is complete and specific
- **Response template:** Full 8-section requirement with YAML frontmatter present

### ❌ FAILING CHECKS

**ISSUE #1: File paths are relative, not absolute (Rule 8 violation)**

The task file uses relative paths:
```
src/eggs/code.egg.md
browser/src/eggs/__tests__/codeEgg.test.ts
```

These MUST be absolute Windows paths per Rule 8:
```
C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\eggs\code.egg.md
C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\eggs\__tests__\codeEgg.test.ts
```

**ISSUE #2: Subdomain registration already exists**

The task states: "Add `code` subdomain to the EGG router"

However, `eggResolver.ts` line 135 already contains:
```typescript
'code.shiftcenter.com': 'code',
```

This is not an error, but the task should clarify that the bee needs to VERIFY the registration exists, not add it. The acceptance criterion "code subdomain routes correctly in EGG router" is accurate.

---

## Correction Request to Q33N

Please update the task file:

1. **Replace all relative file paths with absolute Windows paths:**
   - Current: `src/eggs/code.egg.md`
   - Required: `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\eggs\code.egg.md`

   - Current: `browser/src/eggs/__tests__/codeEgg.test.ts`
   - Required: `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\eggs\__tests__\codeEgg.test.ts`

2. **Clarify subdomain registration requirement:**
   - Change "Add `code` subdomain to the EGG router" to "Verify `code` subdomain exists in eggResolver.ts hardcoded fallback table (line 135)"

---

## Approval Status

**NOT APPROVED** — awaiting corrections from Q33N (Cycle 1 of 2).

Once corrections are made, this task is ready for bee dispatch with model=haiku.

---

## Next Steps

1. Q33N corrects task file
2. Q33N resubmits for review
3. Q33NR approves (if corrections are correct)
4. Q33N dispatches BEE-HAIKU with corrected task file
