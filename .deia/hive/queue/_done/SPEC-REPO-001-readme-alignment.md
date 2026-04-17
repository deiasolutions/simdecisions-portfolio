# SPEC-REPO-001-readme-alignment: Update README to Match Flat Monorepo

## Priority
P2

## Depends On
None

## Model Assignment
haiku

## Objective

The root `README.md` still describes a `packages/` workspace layout that was flattened in April 2026. Setup instructions reference `pip install -e ./packages/core` which fails. Update README.md to reflect the current flat structure with top-level `hivenode/`, `simdecisions/`, `browser/`, `_tools/` directories.

## Files to Read First

- README.md
- CLAUDE.md

## Acceptance Criteria

- [ ] README.md layout section matches current root-level directories (hivenode/, simdecisions/, browser/, _tools/, hodeia_auth/, tests/)
- [ ] No references to `packages/` directory anywhere in README.md
- [ ] Setup instructions use `pip install -e .` (not `pip install -e ./packages/core`)
- [ ] Frontend setup references `cd browser && npm install` (not `cd packages/browser`)
- [ ] All file paths mentioned in README.md point to files that actually exist
- [ ] README.md does not contradict CLAUDE.md on any structural claims
- [ ] Estimation Calibration section paths updated to `_tools/` prefix

## Smoke Test

- [ ] `grep -i packages README.md` returns no matches (except if discussing the concept generically)

## Constraints

- No file over 500 lines
- No stubs — every function complete
- No git operations
- Do not remove any sections — only update paths and layout descriptions
- CLAUDE.md is the source of truth for structure; README.md is for human onboarding
