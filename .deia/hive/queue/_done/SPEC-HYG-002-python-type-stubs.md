# SPEC-HYG-002-python-type-stubs: Install missing Python type stubs for mypy

## Priority
P2

## Depends On
None

## Model Assignment
haiku

## Objective

Install `types-PyYAML` and `types-requests` as dev dependencies and add them to pyproject.toml so that mypy no longer reports "Library stubs not installed" errors for the yaml and requests packages. This eliminates the stub-related noise from the mypy report, making real type errors easier to find.

## Files to Read First

- .deia/reports/mypy.txt
- pyproject.toml

## Acceptance Criteria

- [ ] `types-PyYAML` is listed in pyproject.toml under dev dependencies
- [ ] `types-requests` is listed in pyproject.toml under dev dependencies
- [ ] Running `python -m mypy hivenode/ simdecisions/` no longer reports "Library stubs not installed" for yaml
- [ ] Running `python -m mypy hivenode/ simdecisions/` no longer reports "Library stubs not installed" for requests
- [ ] Both packages are installable via `pip install -e ".[dev]"` or equivalent

## Smoke Test

- [ ] Run `pip install types-PyYAML types-requests` and confirm successful install
- [ ] Run `python -m mypy hivenode/ simdecisions/ 2>&1 | grep "Library stubs not installed"` and confirm zero matches for yaml and requests

## Constraints

- No file over 500 lines
- No stubs — every function complete
- No git operations
- All existing tests must still pass after changes
- Run `python -m mypy` to verify fixes
- Only modify pyproject.toml for dependency additions — do not change any Python source files
