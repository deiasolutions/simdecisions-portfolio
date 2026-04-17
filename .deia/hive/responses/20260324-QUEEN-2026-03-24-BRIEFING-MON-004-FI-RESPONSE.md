# QUEEN-2026-03-24-BRIEFING-MON-004-FI: MON-004 Task File Final Correction -- COMPLETE

**Status:** COMPLETE
**Model:** Sonnet
**Date:** 2026-03-24
**Correction Cycle:** 2 of 2 (FINAL)

## Files Modified

- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\queue\_stage\2026-03-24-TASK-MON-004-code-egg.md` (corrected)

## What Was Done

**CORRECTION #1: Converted All Relative Paths to Absolute Paths**

- **Line 26:** Changed `src/eggs/code.egg.md` and `src/eggs/index.ts` to full absolute paths:
  - `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\eggs\code.egg.md`
  - `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\eggs\index.ts`

- **Lines 111-117 (File Locations section):** Converted all relative directory paths to absolute paths:
  - `src/eggs/` → `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\eggs\`
  - `browser/src/eggs/` → `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\eggs\`

- **Line 102:** Added absolute path comment to import statement:
  - `import codeEgg from './code.egg.md'  // C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\eggs\code.egg.md`

**CORRECTION #2: Fixed Subdomain Registration Wording**

- **Lines 95-97:** Changed misleading instruction from "Add `code` subdomain" to accurate verification instruction:
  - **Before:** "Add `code` subdomain to the EGG router so `code.shiftcenter.com` resolves to `code.egg.md`. Follow the same pattern as `efemera.egg.md` subdomain registration."
  - **After:** "Verify `code` subdomain exists in `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\eggs\eggResolver.ts` hardcoded fallback table (should already be present at line ~135 as `'code.shiftcenter.com': 'code'`). If missing, add it following the same pattern as efemera subdomain."

## Test Results

N/A — This is a Q33N task file correction, not code implementation.

## Build Verification

N/A — No code changes, only task file documentation corrections.

## Acceptance Criteria

- [x] Q33N reads briefing
- [x] Q33N applies both corrections to task file
- [x] All relative paths converted to absolute paths (Rule 8 compliance)
- [x] Subdomain registration wording corrected (verify vs add)
- [x] Task file ready for Q33NR final review

## Clock / Cost / Carbon

- **Clock:** 3 minutes
- **Cost:** ~$0.02 USD
- **Carbon:** ~0.5g CO2e

## Issues / Follow-ups

**Status:** Task file is now fully corrected and ready for Q33NR approval (cycle 2 of 2).

**Changes Summary:**
1. ✅ All file paths now absolute (4 locations corrected)
2. ✅ Subdomain wording now accurate (verify existing vs unconditional add)

**Next Step:** Q33NR final review and approval for BEE-HAIKU dispatch.

---

## Detailed Change Log

### Change 1: Line 26 (Scope section)
- **Old:** `Write src/eggs/code.egg.md and register it in src/eggs/index.ts.`
- **New:** `Write C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\eggs\code.egg.md and register it in C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\eggs\index.ts.`

### Change 2: Lines 95-97 (Subdomain registration section)
- **Old:** "Add `code` subdomain to the EGG router so `code.shiftcenter.com` resolves to `code.egg.md`. Follow the same pattern as `efemera.egg.md` subdomain registration."
- **New:** "Verify `code` subdomain exists in `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\eggs\eggResolver.ts` hardcoded fallback table (should already be present at line ~135 as `'code.shiftcenter.com': 'code'`). If missing, add it following the same pattern as efemera subdomain."

### Change 3: Line 102 (index.ts registration example)
- **Old:** `import codeEgg from './code.egg.md'`
- **New:** `import codeEgg from './code.egg.md'  // C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\eggs\code.egg.md`

### Change 4: Lines 111-117 (File Locations section)
- **Old:** Relative paths `src/eggs/` and `browser/src/eggs/`
- **New:** Absolute paths `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\eggs\` and `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\eggs\`

---

## Rule 8 Compliance Verification

**Rule 8:** All file paths must be absolute in task docs and specs.

✅ Line 26: Absolute paths used
✅ Line 102: Absolute path in comment
✅ Lines 111-117: Absolute paths in file tree
✅ Line 97: Absolute path in eggResolver.ts reference

**All 4 instances corrected. Task file is now fully Rule 8 compliant.**
