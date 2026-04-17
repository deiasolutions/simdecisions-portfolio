# SPEC-REPO-001: Align README.md with Flat Monorepo Structure

## Objective
Update the root `README.md` to remove all references to the legacy `packages/` workspace and provide accurate setup instructions for the current flat layout.

## Current Issues (Evidence)
- `README.md` still describes a `packages/` workspace that was flattened during the refactor.
- Setup instructions reference `pip install -e ./packages/core`, which will fail as the directory no longer exists.

## Deliverables
- [ ] Update `Layout` section to match current root-level directories (`hivenode/`, `simdecisions/`, `_tools/`).
- [ ] Update `Setup` section with current `pip install -e .` and `npm install` paths.
- [ ] Update `Estimation Calibration` section paths (e.g., `_tools/estimates.py` instead of `packages/tools/src/simdecisions/tools/estimates.py`).

## Test Requirements
- [ ] Manual verification: All absolute paths in the new `README.md` must point to existing files.
- [ ] Manual verification: Setup commands should correctly initialize the environment in a fresh clone.

## Constraints
- Do not remove the "Calibration Calibration" section, just update its paths.
- Keep `CLAUDE.md` as the source of truth for AI agents; `README.md` is for humans.
