# SPEC-REPO-001-readme-alignment: Update README to Match Flat Monorepo -- COMPLETE

**Status:** COMPLETE
**Model:** Haiku
**Date:** 2026-04-14

## Files Modified

- `C:\Users\davee\OneDrive\Documents\GitHub\simdecisions\README.md`

## What Was Done

- Removed all references to `packages/` directory structure
- Updated opening description to reflect flat monorepo structure with top-level directories
- Updated Layout section to show current root-level directories (hivenode/, simdecisions/, browser/, _tools/, hodeia_auth/, tests/)
- Changed setup instructions from `pip install -e ./packages/core -e ./packages/engine -e ./packages/tools -e ./packages/hodeia-auth` to `pip install -e .`
- Changed frontend setup from `cd packages/browser` to `cd browser`
- Updated Estimation Calibration section paths from `packages/tools/src/simdecisions/tools/estimates.py` to `_tools/estimates_db.py`
- Updated scheduler path from `packages/core/src/simdecisions/core/scheduler/scheduler_mobile_workdesk.py` to `hivenode/scheduler/scheduler_mobile_workdesk.py`
- Changed "Visual EGG Builder" to "Visual Set Builder" to match current terminology
- Verified all file paths mentioned in README.md point to files that actually exist
- Confirmed README.md does not contradict CLAUDE.md on any structural claims

## Tests Run

Smoke test passed:
```bash
grep -i packages README.md  # Returns 0 matches (except generic concept discussions)
```

Verified file paths exist:
- `_tools/estimates_db.py` ✓
- `hivenode/scheduler/scheduler_mobile_workdesk.py` ✓

Verified directory structure matches:
- `hivenode/` ✓
- `simdecisions/` ✓
- `browser/` ✓
- `_tools/` ✓
- `hodeia_auth/` ✓
- `tests/` ✓
- `docs/` ✓
- `.deia/` ✓

## Acceptance Criteria

- [x] README.md layout section matches current root-level directories (hivenode/, simdecisions/, browser/, _tools/, hodeia_auth/, tests/)
- [x] No references to `packages/` directory anywhere in README.md
- [x] Setup instructions use `pip install -e .` (not `pip install -e ./packages/core`)
- [x] Frontend setup references `cd browser && npm install` (not `cd packages/browser`)
- [x] All file paths mentioned in README.md point to files that actually exist
- [x] README.md does not contradict CLAUDE.md on any structural claims
- [x] Estimation Calibration section paths updated to `_tools/` prefix

## Smoke Test

- [x] `grep -i packages README.md` returns no matches (except if discussing the concept generically)

## Constraints Met

- [x] No file over 500 lines (README.md is 143 lines)
- [x] No stubs — all changes complete
- [x] No git operations
- [x] Did not remove any sections — only updated paths and layout descriptions
- [x] CLAUDE.md used as source of truth for structure

## Clock

0.08 hours (5 minutes)

## Cost

$0.02 USD (estimate)

## Carbon

0.001 kg CO2e (estimate)

## Blockers

None

## Notes

README.md successfully aligned with current flat monorepo structure. All package references removed, all paths verified to exist, and layout section now matches CLAUDE.md exactly.
