# BRIEFING: Fix TASK-202 Dispatch Error

**From:** Q33NR
**To:** Q33N
**Date:** 2026-03-16
**Re:** TASK-202 subdomain EGG routing dispatch failure

---

## Issue

TASK-202 was dispatched with `--role regent` instead of `--role bee`. The regent (correctly) refused to write code per HIVE.md rules.

**Error details from bee response:**
```
CRITICAL ISSUE DETECTED: I am assigned role Q33NR (regent), but the task file is written for a BEE.
```

**Root cause:** Queue runner dispatched a BEE task file to a regent role.

---

## What Needs to Happen

The task file is **already correct and ready**. It just needs to be dispatched to the right role:

**File:** `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\tasks\2026-03-16-TASK-202-subdomain-egg-routing.md`

**Action needed:** Dispatch TASK-202 to a **BEE** with **haiku** model.

---

## Your Instructions

1. **Read the task file** to verify it's complete (it should be):
   - `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\tasks\2026-03-16-TASK-202-subdomain-egg-routing.md`

2. **Dispatch to BEE** (not regent):
   ```bash
   python .deia/hive/scripts/dispatch/dispatch.py \
     C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\tasks\2026-03-16-TASK-202-subdomain-egg-routing.md \
     --model haiku \
     --role bee \
     --inject-boot
   ```

3. **Wait for bee response** in `.deia/hive/responses/`

4. **Review response** for:
   - All 8 sections present
   - Tests passing (10+ tests required)
   - Acceptance criteria met
   - No stubs shipped

5. **Report back** to me (Q33NR) with completion summary

---

## Expected Deliverables

From the BEE:
- [ ] `canvas.shiftcenter.com` added to hostname map in `eggResolver.ts`
- [ ] Test file created: `browser/src/eggs/__tests__/eggResolver.test.ts`
- [ ] 10+ tests passing
- [ ] Response file: `.deia/hive/responses/20260316-TASK-202-RESPONSE.md`

---

## Original Spec Context

**Original spec:** W3-03 Subdomain EGG Routing
**Objective:** Add hostname -> EGG mapping for multi-product deployment
**Model:** haiku
**Priority:** P1

---

## Notes

- This is NOT a code problem — the task file is correct
- This is NOT a spec problem — the original spec was clear
- This IS a dispatch problem — wrong role was used
- Fix: Re-dispatch with correct role
