# QUEUE-TEMP-SPEC-CANVAS3-CHAT-TERMINAL: Change canvas3 third pane to terminal -- COMPLETE

**Status:** COMPLETE
**Model:** Sonnet 4.5
**Date:** 2026-03-30

## Files Modified
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\eggs\canvas3.set.md`

## What Was Done
- Changed canvas-chat pane from `appType: "text-pane"` to `appType: "terminal"`
- Updated label from "Chat" to "Fr@nk"
- Replaced text-pane config with terminal config:
  - Set `promptPrefix: "canvas>"`
  - Set `routeTarget: "ai"` for AI routing
  - Set `brandName: "SimDecisions"`
  - Enabled `welcomeBanner: true`
  - Added `links.to_text: "canvas-editor"` for IR deposits to canvas
- Preserved `chrome: false` and `nodeId: "canvas-chat"` for backward compatibility

## Tests Run
None required — this is a pure configuration change to an EGG file. The terminal primitive already exists and is tested.

## Test Results
N/A — configuration change only

## Issues Found
None

## Deviations from Spec
None

## Follow-up Required
None — ready for smoke test

## Cost
~$0.02 (Sonnet 4.5, single file edit)
