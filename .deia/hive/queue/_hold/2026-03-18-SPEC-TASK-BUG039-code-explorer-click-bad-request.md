# SPEC: BUG-039 — Code explorer click still shows "error loading file: bad request"

## Priority: P0

## Problem
Clicking a file in the Code EGG's explorer tree-browser shows "error loading file: bad request". BUG-031 bee claimed to fix this by adding name field and protocol prefix to the file:selected bus event, but the error persists at runtime.

## Context
- BUG-031 fix modified `treeBrowserAdapter.tsx` to add `name` and protocol-prefixed `uri` to file:selected events
- 8 tests pass for that fix
- Despite this, clicking a file in the Code EGG explorer STILL produces "error loading file: bad request"
- This means either: (a) the fix is incomplete, (b) the error comes from the backend HTTP call failing, or (c) the SDEditor file loading path has a different issue

## Investigation Required
1. Trace the FULL file loading flow:
   - Explorer tree click → treeBrowserAdapter publishes `file:selected` on bus
   - SDEditor receives `file:selected` → extracts uri/path → makes HTTP request to load file
   - Backend endpoint receives request → reads file → returns content
2. Check what HTTP request SDEditor actually makes — is the URL malformed? Wrong endpoint?
3. Check the backend route that serves file content — does it exist? Does it accept the URI format being sent?
4. Check browser dev console network tab behavior — what request is made and what's the 400 response?
5. "Bad request" specifically means HTTP 400 — the backend is rejecting the request. Find out WHY.
6. Check if the volume/filesystem routes are properly registered and what parameters they expect

## Files to Read First
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\treeBrowserAdapter.tsx`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\text-pane\SDEditor.tsx` (file loading handler)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\routes\` (find the file/volume serving route)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260317-BUG-031-RESPONSE.md`

## Fix
- Identify exactly why the backend returns 400
- Fix the request format, the backend validation, or both
- Do NOT just fix tests — the runtime behavior must work

## Test Requirements
- Integration test: file click → bus event → HTTP request → content returned
- Test the actual HTTP endpoint with the actual URI format being sent
- Test error cases: missing file, bad path, missing protocol
- All existing tests still pass

## Constraints
- No file over 500 lines
- CSS: var(--sd-*) only
- No stubs
- TDD

## Model: sonnet
