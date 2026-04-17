# Q33N Response: AUTH-D Hivenode Config Rebrand Task File

**Status:** TASK FILE READY FOR REVIEW
**Date:** 2026-03-24
**Briefing:** 2026-03-24-BRIEFING-AUTH-D-HIVENODE-CONFIG-REBRAND.md

---

## Task File Created

**Location:** `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\tasks\2026-03-24-TASK-AUTH-D-HIVENODE-CONFIG-REBRAND.md`

**Model Assignment:** Haiku
**Priority:** P1
**Scope:** Single bee, backend only (hivenode config + auth)

---

## Summary

I have created a comprehensive task file for the hivenode auth config rebrand from ra96it → auth. The task covers:

### Config Changes
1. **Field renaming** in config.py:
   - `ra96it_public_key` → `auth_public_key`
   - `ra96it_public_key_path` → `auth_public_key_path`
   - `ra96it_jwks_url` → `auth_jwks_url`
   - `get_ra96it_public_key()` → `get_auth_public_key()`
   - Default JWKS URL: `https://hodeia.com/.well-known/jwks.json`

2. **Dual-issuer JWT validation** in dependencies.py:
   - Change `issuer="ra96it"` to `issuer=["ra96it", "hodeia"]` in BOTH jwt.decode() calls
   - Maintains backwards compatibility during transition

3. **Reference updates** in:
   - main.py (lines 207-211): JWKS cache initialization
   - jwks_cache.py (line 26): docstring updates

4. **Test updates**:
   - conftest.py: fixture field names
   - New file: test_auth_dual_issuer.py with 6+ tests
   - Verify all existing auth tests still pass

### Deliverables Structure
- **8 files to read first** — all absolute paths provided
- **5 deliverable sections** — config, JWT validation, JWKS cache, main.py, tests
- **3 test requirement sections** — new tests, existing test updates, edge cases
- **11 acceptance criteria** — specific, measurable, complete
- **8-section response template** — mandatory format enforced

### TDD Approach
Task requires:
- Tests written FIRST
- New test file: `test_auth_dual_issuer.py` with 6+ tests
- Edge case coverage: both issuers (ra96it, hodeia), both audiences (shiftcenter, deiasolutions), invalid issuer rejection
- All existing auth tests must continue passing

### Constraints Enforced
- No file over 500 lines (config.py at 165 lines, dependencies.py at 289 lines — both safe)
- No stubs
- Dual-issuer MUST work (backwards compatibility required)
- No breaking changes to existing ra96it JWT validation

---

## Files Scanned

I reviewed all 8 files listed in the briefing:
1. `hivenode/config.py` — config field declarations (lines 46-49, 154-160)
2. `hivenode/dependencies.py` — JWT issuer validation (lines 214, 226)
3. `hivenode/services/jwks_cache.py` — docstring references (line 26)
4. `hivenode/main.py` — JWKS cache init (lines 207-211)
5. `tests/hivenode/conftest.py` — test fixtures (lines 72, 99)
6. `tests/hivenode/test_auth_routes.py` — scanned for ra96it references
7. `tests/hivenode/test_auth_identity.py` — scanned for ra96it references
8. `tests/hivenode/test_rate_limiter.py` — scanned for ra96it references

All references identified and documented in task file.

---

## Task File Completeness Check

- [x] Objective: Single sentence, clear deliverable
- [x] Context: Explains current state → target state
- [x] Files to Read First: 8 files, all absolute paths
- [x] Deliverables: 5 sections, 22 specific items with checkboxes
- [x] Test Requirements: TDD approach, 6+ new tests, edge cases, existing test verification
- [x] Constraints: File size, no stubs, TDD, backwards compat, no breaking changes
- [x] Acceptance Criteria: 11 items, specific and measurable
- [x] Response Requirements: 8-section template, mandatory compliance
- [x] Notes: Context on auth rebrand initiative, dual-issuer rationale, PyJWT usage

---

## What I Did NOT Include

- **No code snippets** — bee will read files directly
- **No implementation details** — bee decides approach within constraints
- **No Git operations** — bee writes code and tests only
- **No dispatch instructions** — Q33NR will approve first, then I dispatch

---

## Ready for Q33NR Review

The task file is complete and ready for your review. Please verify:

1. **Scope appropriate for haiku?** — backend config renaming + dual-issuer JWT validation, ~4 files modified, 6+ tests
2. **Acceptance criteria complete?** — all 11 items match briefing requirements
3. **Test requirements clear?** — TDD approach, new test file, edge cases, existing test verification
4. **No ambiguity?** — all file paths absolute, all deliverables specific
5. **Backwards compatibility enforced?** — dual-issuer requirement explicit, no breaking changes

If approved, I will dispatch the bee with:
```bash
python .deia/hive/scripts/dispatch/dispatch.py .deia/hive/tasks/2026-03-24-TASK-AUTH-D-HIVENODE-CONFIG-REBRAND.md --model haiku --role bee --inject-boot
```

Awaiting your approval or corrections.

---

**Q33N out.**
