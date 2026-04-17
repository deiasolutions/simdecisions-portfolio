# FIX-HAIKU-PRICING: Update Haiku Pricing Constant -- COMPLETE

**Status:** COMPLETE
**Model:** Haiku
**Date:** 2026-03-18

## Files Modified
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\adapters\cli\claude_cli_subprocess.py`

## What Was Done

- Located the outdated Haiku pricing constant in `PRICING` dict at lines 49-56
- Updated Haiku 4.5 pricing from:
  - input: 1.0 → 0.80 per million tokens
  - output: 5.0 → 4.0 per million tokens
- Test verification: `test_estimate_cost_haiku` now passes
  - Expected cost for 1000 input + 1000 output: $0.0048
  - Calculated: (1000/1M × 0.80) + (1000/1M × 4.0) = 0.0048 ✓
- All other cost calculation tests remain passing (sonnet, opus, defaults)

## Summary
Haiku 4.5 pricing constant corrected to match current Anthropic rate card. Test suite validates the fix.
