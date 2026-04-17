# SPEC-VIDEO-GOVERNED-BUILD-001: The Governed Build vs Black Box Development -- COMPLETE

**Status:** COMPLETE
**Model:** Sonnet
**Date:** 2026-04-12
**Bot ID:** BEE-QUEUE-TEMP-SPEC-VIDEO-GOVERNED-BUILD-001

## Files Modified

- `C:\Users\davee\OneDrive\Documents\GitHub\simdecisions\production\episodes\governed-build\governed_build.py` (created)

## What Was Done

- Created production directory structure at `production/episodes/governed-build/`
- Wrote complete Manim animation scene file implementing all spec requirements
- Defined all brand constants (SD_DARK, SD_SURFACE, SD_BLUE, SD_GREEN, SD_AMBER, SD_WHITE, SD_MUTED, SD_CARBON, SD_RED, SD_CLOCK, SD_COIN) at top of file before imports
- Implemented helper functions: `make_node()`, `make_black_box()`, `make_divider()`, `make_column_header()`
- Implemented `GovernedBuild` scene class with 9 acts:
  - ACT 0: Title frame with @daaaave-atx handle and "Two ways to build with AI." title
  - ACT 1: Split screen with "THE GOVERNED BUILD" (green) and "BLACK BOX DEVELOPMENT" (red) headers
  - ACT 2: Black box visualization - prompt → black box with "?" → output → "nothing else." label
  - ACT 3: Governed build - human ↔ claude double arrow → spec → "questions answered." label
  - ACT 4: DAG formation - TASK-001/002 in parallel → TASK-003 dependent
  - ACT 5: Model tags (haiku/sonnet/opus) beneath tasks
  - ACT 6: Both sides produce output, left shows "+ full transcript." label
  - ACT 7: "BAT validates." label and Three Currencies (CLOCK/COIN/CARBON) in correct order
  - ACT 8: Right side dims to 15% opacity, left header brightens to SD_GREEN
  - ACT 9: Ending frame with "SimDecisions", "Build governed." tagline, and both CTAs (simdecisions.com, @daaaave-atx)
- Added NARRATION comments at all major beats matching the spec
- Tuned wait times to achieve 80.13 seconds at low quality, 80.2 seconds at high quality (within 80-100 second target)
- No hardcoded hex colors - all colors use brand constants
- Module docstring includes all required fields (concept, duration, scene class, voice, channel, created date, spec ID, round)

## Tests Run

✓ Low quality render: `manim governed_build.py GovernedBuild -ql`
  - Rendered successfully without errors
  - Video duration: 80.13 seconds (within 80-100 second target)
  - Output: `production/episodes/governed-build/media/videos/governed_build/480p15/GovernedBuild.mp4` (437KB)

✓ High quality render: `manim governed_build.py GovernedBuild -qh`
  - Rendered successfully without errors
  - Video duration: 80.2 seconds (within 80-100 second target)
  - Output: `production/episodes/governed-build/media/videos/governed_build/1080p60/GovernedBuild.mp4`

## Acceptance Criteria Status

- [x] Scene renders without error at `-ql`
- [x] Scene renders without error at `-qh`
- [x] Video length is 80-100 seconds (80.13s at -ql, 80.2s at -qh)
- [x] Title frame shows `@daaaave-atx` handle
- [x] Split screen shows both column headers (THE GOVERNED BUILD / BLACK BOX DEVELOPMENT)
- [x] Left side shows: spec, DAG, model tags, BAT, Three Currencies
- [x] Right side shows: black box with "?" and "nothing else." label
- [x] All narration cue comments present at correct beats
- [x] Right side dims to low opacity at final beat (0.15 opacity)
- [x] Ending frame shows: SimDecisions, "Build governed.", both CTAs (simdecisions.com, @daaaave-atx)
- [x] No hardcoded hex colors — brand constants only
- [x] Module docstring present with all required fields
- [x] Output file at `production/episodes/governed-build/governed_build.py`

## Visual Elements Implemented

**Split Screen Layout:**
- Vertical divider line at center
- Left column header: "THE GOVERNED BUILD" (SD_GREEN)
- Right column header: "BLACK BOX DEVELOPMENT" (SD_RED)

**Left Side (Governed Build):**
- human + claude nodes with double arrow (co-authoring)
- spec node (SD_GREEN stroke)
- "questions answered." label (SD_GREEN)
- TASK-001, TASK-002 (parallel, SD_BLUE stroke)
- TASK-003 (dependent, SD_MUTED stroke)
- "depends_on" label
- Model tags: haiku (SD_AMBER), sonnet (SD_BLUE), opus (SD_CARBON)
- output node (SD_GREEN stroke)
- "+ full transcript." label (SD_GREEN)
- "BAT validates." label (SD_GREEN)
- Three Currencies: CLOCK (SD_CLOCK), COIN (SD_COIN), CARBON (SD_CARBON) in correct order

**Right Side (Black Box):**
- prompt node (SD_MUTED)
- Black box rectangle with "?" (black fill, SD_MUTED stroke)
- output node (SD_MUTED)
- "nothing else." label (SD_RED)

**Ending Frame:**
- "SimDecisions" (large, white, bold)
- "Build governed." (green tagline)
- "simdecisions.com" (blue CTA)
- "@daaaave-atx" (muted CTA)

## Notes

- All timing carefully tuned to match ~2.5 words/second narration pace
- Animation progression flows naturally from title → split screen → black box demo → governed build demo → comparison → ending
- Final beat dims right side to 15% opacity while brightening left header to SD_GREEN as specified
- All 47 animations rendered successfully
- Scene follows all ManimCE patterns from reference docs
- No LaTeX, no external assets, no ThreeDScene/MovingCameraScene as constrained
- Ready for voice-over with bf_emma (Kokoro-82M British female)
