# SPEC-HYG-010-hardcoded-colors: Remove Hardcoded Colors from Backend Routes -- COMPLETE

**Status:** COMPLETE
**Model:** Sonnet
**Date:** 2026-04-14

## Files Modified

- `C:\Users\davee\OneDrive\Documents\GitHub\simdecisions\hivenode\routes\kanban_routes.py` (336 lines)
- `C:\Users\davee\OneDrive\Documents\GitHub\simdecisions\simdecisions\phase_ir\mermaid.py` (486 lines)
- `C:\Users\davee\OneDrive\Documents\GitHub\simdecisions\tests\simdecisions\phase_ir\test_color_token_resolution.py` (NEW, 93 lines)

## What Was Done

- Replaced hardcoded hex colors in `COLUMN_DEFINITIONS` (kanban_routes.py) with semantic token names: `sd-kanban-icebox`, `sd-kanban-backlog`, `sd-kanban-in-progress`, `sd-kanban-review`, `sd-kanban-done`
- Added documentation comment mapping each token to its intended CSS variable (e.g., `"sd-kanban-icebox" -> var(--sd-kanban-icebox)`)
- Replaced hardcoded hex colors in `_DEFAULT_THEME` (mermaid.py) with semantic tokens: `sd-node-human`, `sd-node-python`, etc.
- Created `_TOKEN_TO_HEX_MAP` lookup table in mermaid.py to store the render-time hex values (required for Mermaid syntax compatibility)
- Implemented `_resolve_color_tokens()` function that converts semantic tokens to hex values only at render time
- Modified `add_styling()` to call `_resolve_color_tokens()` before emitting Mermaid classDef lines
- Added comprehensive documentation explaining the token-to-CSS-variable mapping for frontend team
- Created 7 new integration tests verifying color token resolution works correctly
- Used length-descending sort to prevent partial token matches during replacement

## Tests Run

- All 23 existing kanban_routes tests: PASS
- All 19 existing mermaid_export tests: PASS
- 7 new color_token_resolution tests: PASS
- **Total: 49 tests passed**

## Smoke Tests

- ✅ `grep '#[0-9a-fA-F]\{6\}' hivenode/routes/kanban_routes.py` returns no matches
- ✅ `grep '#[0-9a-fA-F]\{6\}' simdecisions/phase_ir/mermaid.py` returns matches only in `_TOKEN_TO_HEX_MAP` lookup table (render-time resolution, as specified)
- ✅ No `rgb()` calls
- ✅ No named colors (except in lookup table)

## Acceptance Criteria

- [x] `COLUMN_DEFINITIONS` in `kanban_routes.py` uses semantic color token names instead of hex codes
- [x] `_DEFAULT_THEME` in `mermaid.py` uses semantic color token names instead of hex codes
- [x] A mapping dict documents which CSS variable each token maps to (see comments in both files + `_TOKEN_TO_HEX_MAP`)
- [x] No hex codes, `rgb()`, or named colors remain in API surface of either file (hex only in render-time lookup)
- [x] All existing tests still pass (42 existing + 7 new = 49 total)
- [x] Mermaid diagram rendering still works (tests verify hex resolution at render time)

## Implementation Notes

### Kanban Routes Approach

Straightforward token replacement in `COLUMN_DEFINITIONS`. The API now returns semantic tokens like `"sd-kanban-backlog"` to the frontend, which can resolve them to `var(--sd-kanban-backlog)` in CSS.

### Mermaid Approach (Render-Time Lookup)

Mermaid syntax requires inline hex colors in `fill:` and `stroke:` attributes. The solution:

1. Store semantic tokens in `_DEFAULT_THEME` (e.g., `"fill:sd-node-human,stroke:sd-node-human-stroke"`)
2. Maintain `_TOKEN_TO_HEX_MAP` with the actual hex values (centralized color authority)
3. Call `_resolve_color_tokens()` at render time to convert tokens → hex for Mermaid output
4. Frontend team can sync their CSS variables with the values in `_TOKEN_TO_HEX_MAP`

This approach satisfies the spec's constraint: "If mermaid syntax requires inline hex for fill/stroke, use a render-time lookup: store semantic tokens in the dict, resolve to hex only at render time from a centralized color map."

### Token Replacement Fix

Initial implementation had a bug where replacing "sd-node-human" would partially match "sd-node-human-stroke", producing "#4CAF50-stroke". Fixed by sorting tokens by length (descending) before replacement, ensuring longer tokens are replaced first.

## CSS Variable Mapping for Frontend Team

### Kanban Columns
- `sd-kanban-icebox` → `var(--sd-kanban-icebox)`
- `sd-kanban-backlog` → `var(--sd-kanban-backlog)`
- `sd-kanban-in-progress` → `var(--sd-kanban-in-progress)`
- `sd-kanban-review` → `var(--sd-kanban-review)`
- `sd-kanban-done` → `var(--sd-kanban-done)`

### Mermaid Node Types
- `sd-node-human` → `var(--sd-node-human)` (fill)
- `sd-node-human-stroke` → `var(--sd-node-human-stroke)` (stroke)
- `sd-node-python` → `var(--sd-node-python)` (fill)
- `sd-node-python-stroke` → `var(--sd-node-python-stroke)` (stroke)
- `sd-node-llm` → `var(--sd-node-llm)` (fill)
- `sd-node-llm-stroke` → `var(--sd-node-llm-stroke)` (stroke)
- `sd-node-http` → `var(--sd-node-http)` (fill)
- `sd-node-http-stroke` → `var(--sd-node-http-stroke)` (stroke)
- `sd-node-subprocess` → `var(--sd-node-subprocess)` (fill)
- `sd-node-subprocess-stroke` → `var(--sd-node-subprocess-stroke)` (stroke)
- `sd-node-wait` → `var(--sd-node-wait)` (fill)
- `sd-node-wait-stroke` → `var(--sd-node-wait-stroke)` (stroke)
- `sd-node-signal` → `var(--sd-node-signal)` (fill)
- `sd-node-signal-stroke` → `var(--sd-node-signal-stroke)` (stroke)
- `sd-node-source` → `var(--sd-node-source)` (fill)
- `sd-node-source-stroke` → `var(--sd-node-source-stroke)` (stroke)
- `sd-node-sink` → `var(--sd-node-sink)` (fill)
- `sd-node-sink-stroke` → `var(--sd-node-sink-stroke)` (stroke)
- `sd-node-solver` → `var(--sd-node-solver)` (fill)
- `sd-node-solver-stroke` → `var(--sd-node-solver-stroke)` (stroke)
- `sd-text-light` → `var(--sd-text-light)` (text color on dark backgrounds)
- `sd-text-dark` → `var(--sd-text-dark)` (text color on light backgrounds)

Current hex values are documented in `_TOKEN_TO_HEX_MAP` for reference.

## Blockers

None.
