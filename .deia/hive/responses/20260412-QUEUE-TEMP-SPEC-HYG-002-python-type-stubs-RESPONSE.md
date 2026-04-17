# SPEC-HYG-002-python-type-stubs: Install missing Python type stubs for mypy -- COMPLETE

**Status:** COMPLETE
**Model:** Sonnet 4.5
**Date:** 2026-04-12

## Files Modified
- C:/Users/davee/OneDrive/Documents/GitHub/simdecisions/pyproject.toml

## What Was Done
- Added `[project.optional-dependencies]` section to pyproject.toml with a `dev` group
- Added `types-PyYAML>=6.0` to dev dependencies
- Added `types-requests>=2.0` to dev dependencies
- Installed both type stub packages successfully
- Verified that mypy no longer reports "Library stubs not installed" errors for yaml and requests

## Tests Run
- ✅ Installed types-PyYAML and types-requests via pip
- ✅ Confirmed packages installed: types-PyYAML v6.0.12.20260408, types-requests v2.33.0.20260408
- ✅ Ran mypy on hivenode/wiki/parser.py (which imports yaml) — no stub errors
- ✅ Ran mypy on multiple files — confirmed no "Library stubs not installed" errors for yaml or requests

## Acceptance Criteria
- [x] `types-PyYAML` is listed in pyproject.toml under dev dependencies
- [x] `types-requests` is listed in pyproject.toml under dev dependencies
- [x] Running `python -m mypy hivenode/ simdecisions/` no longer reports "Library stubs not installed" for yaml
- [x] Running `python -m mypy hivenode/ simdecisions/` no longer reports "Library stubs not installed" for requests
- [x] Both packages are installable via `pip install -e ".[dev]"` or equivalent

## Smoke Test Results
- ✅ `pip install types-PyYAML types-requests` — successful install
- ✅ Checked for "Library stubs not installed" errors for yaml/requests — zero matches (confirmed eliminated)

## Notes
- The mypy report still contains 481 errors across 129 files, but none of them are "Library stubs not installed" errors for yaml or requests
- The remaining errors are different type issues (union-attr, attr-defined, import-not-found, var-annotated, etc.) which are outside the scope of this task
- Users can now install dev dependencies with `pip install -e ".[dev]"` to get type stubs
