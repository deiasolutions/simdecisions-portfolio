# TASK-081: Voice Output (TTS) Hook + Speaker Buttons -- COMPLETE

**Status:** COMPLETE
**Model:** Sonnet 4.5
**Date:** 2026-03-14

## Files Modified

### Created Files (7)
1. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\terminal\useSpeechSynthesis.ts` — Speech synthesis hook
2. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\terminal\SpeakerButton.tsx` — Speaker button component
3. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\terminal\__tests__\useSpeechSynthesis.test.ts` — Hook tests (5 tests)
4. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\terminal\__tests__\SpeakerButton.test.tsx` — Button tests (5 tests)
5. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\terminal\__tests__\TerminalOutput.tts.test.tsx` — Integration tests (3 tests)

### Modified Files (4)
6. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\terminal\terminal.css` — Added speaker button styles with pulsing animation
7. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\terminal\TerminalOutput.tsx` — Integrated TTS with speaker buttons on responses
8. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\terminal\TerminalResponsePane.tsx` — Added autoReadEnabled prop
9. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\terminal\TerminalApp.tsx` — Wire settings to auto-read

## What Was Done

### Hook Implementation
- Implemented `useSpeechSynthesis()` hook wrapping `window.speechSynthesis` API
- Graceful fallback when API not available (`isSupported: false`)
- Tracked speaking state via 100ms polling interval
- Auto-cancel stuck speech after 30s (browser bug workaround)
- Cleanup on unmount to stop ongoing speech
- Exposed `speak()`, `stop()`, `pause()`, `resume()` controls

### Speaker Button Component
- Created `SpeakerButton` component with 🔊 (idle) and ⏸ (speaking) icons
- Returns `null` when `speechSynthesis` not supported (graceful fallback)
- Click behavior: speak when idle, stop when speaking
- Active state with pulsing animation CSS
- Accessibility: `aria-label` and `title` attributes

### CSS Styles
- Added `.terminal-speaker-btn` base styles (transparent, muted color, 16px icon)
- Hover state: scale(1.1) + primary text color
- Active state: purple color + pulsing animation (`speaker-pulse` keyframe)
- All styles use `var(--sd-*)` CSS variables (no hex/rgb colors)

### Terminal Integration
- Modified `TerminalOutput` to accept `autoReadEnabled` prop
- Added state tracking: `speakingEntryIndex`, `isSpeaking`
- Auto-read latest response when `autoReadEnabled: true` (via useEffect)
- Clear speaking state when speech stops
- Pass TTS controls (`onSpeak`, `onStop`) to `TerminalLine`
- Speaker button appears on:
  - `entry.terminalMessage` (system message in response)
  - `entry.content` (main response content)

### Settings Integration
- Wire `voice_auto_read` setting from `settingsStore` to `TerminalApp`
- Pass `autoReadEnabled` through `TerminalResponsePane` → `TerminalOutput`
- Setting already exists in `types.ts` (from TASK-080)

## Test Results

### New Tests (13 tests, all passing)
```
✓ src/primitives/terminal/__tests__/useSpeechSynthesis.test.ts (5 tests)
  - Returns isSupported: false when speechSynthesis not available
  - Returns isSupported: true when API available
  - speak(text) creates utterance and calls synth.speak()
  - stop() calls synth.cancel()
  - isSpeaking reflects synth.speaking state

✓ src/primitives/terminal/__tests__/SpeakerButton.test.tsx (5 tests)
  - Renders null when isSupported: false
  - Renders 🔊 icon when not speaking
  - Renders ⏸ icon when speaking
  - Calls onSpeak when clicked (not speaking)
  - Calls onStop when clicked (speaking)

✓ src/primitives/terminal/__tests__/TerminalOutput.tts.test.tsx (3 tests)
  - Auto-read fires speak() for latest response when autoReadEnabled: true
  - Auto-read does NOT fire when autoReadEnabled: false
  - Speaker button on response entry calls speak() with entry content
```

### Full Test Suite
- **Browser tests:** 114 files, 1400 passed, 1 skipped (0 failures)
- **Build:** ✓ No TypeScript errors, 7.14s
- **No regressions**

## Build Verification

```bash
cd browser && npm test -- --run
# Test Files  114 passed (114)
#      Tests  1400 passed | 1 skipped (1401)

cd browser && npm run build
# ✓ built in 7.14s
```

## Acceptance Criteria

- [x] Speaker button (🔊) appears on each terminal response entry
- [x] Button hidden if browser doesn't support `speechSynthesis`
- [x] Click speaker → reads message aloud
- [x] Icon changes to ⏸ while speaking, pulsing animation
- [x] Click again → stops speaking
- [x] Auto-read mode: latest response spoken automatically when setting enabled
- [x] Auto-read respects `voice_auto_read` setting from settingsStore
- [x] Only one message speaks at a time (stop previous when starting new)
- [x] 13+ tests pass (mock speechSynthesis API)
- [x] CSS uses var(--sd-*) only
- [x] No file over 500 lines

## Clock / Cost / Carbon

**Clock:** 19 minutes (1,140 seconds)
**Cost:** $0.03 USD (estimated: 60K input tokens + 5K output tokens @ Sonnet 4.5 rates)
**Carbon:** ~12g CO2e (estimated: AWS us-east-1 region, CPU inference workload)

## Issues / Follow-ups

### Edge Cases Handled
- **No API support:** Graceful fallback, speaker buttons hidden
- **Stuck speech:** Auto-cancel after 30s (rare browser bug)
- **Multiple entries:** Only one entry speaks at a time (tracked via `speakingEntryIndex`)
- **Auto-read + manual:** Works together, latest action wins

### Dependencies
- Requires `voice_auto_read` setting in Settings UI (exists from TASK-080)
- No backend changes needed (purely browser-native API)

### Next Tasks
- **TASK-082:** Voice settings integration — UI toggle for auto-read mode
- **Future:** Voice selection dropdown (male/female, accents)
- **Future:** Rate/pitch/volume controls in settings
- **Future:** TTS for system messages and IR descriptions

### Notes
- All tests use mocked `speechSynthesis` API (not real browser TTS)
- Real browser TTS requires user interaction to work (security policy)
- Speaker buttons appear inline after text (right-aligned via margin-left)
- Auto-read fires on `entries.length` change (detects new responses)
- CSS animation is subtle (0.6 opacity min, 1s cycle)
