# SPEC-SWE-django-django-11734: SWE-bench Patch Generation -- COMPLETE

**Status:** COMPLETE
**Model:** Sonnet
**Date:** 2026-04-13

## Files Modified

- C:\Users\davee\OneDrive\Documents\GitHub\simdecisions\.deia\benchmark\swebench\patches\django__django-11734.diff (created)

## What Was Done

Created a unified diff patch that fixes the OuterRef issue in Django's ORM when used with exclude() or ~Q().

### Root Cause Analysis

The bug occurred when OuterRef was used in nested subqueries created by exclude() or ~Q(). The issue was in the `ResolvedOuterRef` class in `django/db/models/expressions.py`:

1. `OuterRef` converts to `ResolvedOuterRef` when first resolved
2. When nested subqueries are created (e.g., for M2M relations), `ResolvedOuterRef` was being resolved again
3. Since `ResolvedOuterRef` inherits from `F` but didn't override `resolve_expression()`, it was calling `F.resolve_expression()` which resolves against the wrong query (the intermediate subquery instead of the outermost query)
4. This caused SQL like `WHERE U2."category_id" = "V0"."id"` instead of `WHERE U2."category_id" = "queries_number"."id"`

### The Fix

Added `resolve_expression()` method to `ResolvedOuterRef` class that:
- Takes the outer query as a parameter (passed by Django's subquery resolution mechanism)
- Resolves the reference against the outer query using `query.resolve_ref()`
- Returns a proper `Col` object that references the correct table alias

The patch is minimal (7 lines added) and surgical - only modifying the exact class that needed the fix.

### Verification

- Patch applies cleanly to django/django at commit 999891bd80b3d02dd916731a7a239e1036174885
- Python syntax check passes
- Tested with both `exclude(tags__category_id=OuterRef('pk'))` and `filter(~Q(tags__category_id=OuterRef('pk')))`
- SQL generation works without ValueError
- Patch is in valid unified diff format

## Tests Run

Created and ran test script that verifies:
1. Number.objects.annotate(foo=Exists(Item.objects.exclude(tags__category_id=OuterRef('pk')))).filter(foo=True) - generates SQL successfully
2. Number.objects.annotate(foo=Exists(Item.objects.filter(~Q(tags__category_id=OuterRef('pk'))))).filter(foo=True) - generates SQL successfully

Both tests passed - SQL generation completed without raising ValueError about outer query references.

## Deliverables

✓ Patch file created at C:\Users\davee\OneDrive\Documents\GitHub\simdecisions\.deia\benchmark\swebench\patches\django__django-11734.diff
✓ Patch is in valid unified diff format
✓ Patch applies cleanly to the specified commit
✓ Patch addresses all requirements in the problem statement
✓ Patch follows Django's coding standards
✓ No syntax errors in patched code
✓ Patch is minimal (only 7 lines added)

## Notes

The fix aligns with Django's existing architecture where subqueries pass the outer query context to their expressions via the `query` parameter in `resolve_expression()`. The `ResolvedOuterRef` class now correctly uses this context to resolve references against the outer query rather than the immediate parent query.
