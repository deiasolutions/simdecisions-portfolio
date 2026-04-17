# SPEC-HYG-010-hardcoded-colors: Remove Hardcoded Colors from Backend Routes

## Priority
P1

## Depends On
None

## Model Assignment
haiku

## Objective

Hard Rule 3 forbids hardcoded colors — only CSS variables (`var(--sd-*)`) are allowed. Two backend route files have hardcoded hex colors that are served to the frontend: `kanban_routes.py` has hex in COLUMN_DEFINITIONS (lines 31-35) and `mermaid.py` has hex in _DEFAULT_THEME (lines 332-341). Replace these with semantic token names that the frontend resolves to CSS variables.

## Files to Read First

- hivenode/routes/kanban_routes.py
- simdecisions/phase_ir/mermaid.py

## Acceptance Criteria

- [ ] `COLUMN_DEFINITIONS` in `kanban_routes.py` uses semantic color token names (e.g. `"sd-kanban-icebox"`, `"sd-kanban-backlog"`) instead of hex codes
- [ ] `_DEFAULT_THEME` in `mermaid.py` uses semantic color token names (e.g. `"sd-node-human"`, `"sd-node-python"`) instead of hex codes
- [ ] A mapping dict or comment documents which CSS variable each token maps to, so the frontend team can wire them
- [ ] No hex codes (`#XXXXXX`), no `rgb()`, no named colors remain in either file
- [ ] All existing tests still pass
- [ ] Mermaid diagram rendering still works (tokens are valid in mermaid fill/stroke syntax — if not, use a different approach like a lookup table that the renderer resolves)

## Smoke Test

- [ ] `grep -r '#[0-9a-fA-F]\{6\}' hivenode/routes/kanban_routes.py` returns no matches
- [ ] `grep -r '#[0-9a-fA-F]\{6\}' simdecisions/phase_ir/mermaid.py` returns no matches

## Constraints

- No file over 500 lines
- No stubs — every function complete
- No git operations
- Only modify the two named files — do not touch frontend CSS files (that's a separate spec)
- If mermaid syntax requires inline hex for fill/stroke, use a render-time lookup: store semantic tokens in the dict, resolve to hex only at render time from a centralized color map
