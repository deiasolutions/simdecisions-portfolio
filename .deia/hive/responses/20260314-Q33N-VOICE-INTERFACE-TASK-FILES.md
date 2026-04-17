# Q33N Task Files for Voice Interface (BL-045)

**Date:** 2026-03-14
**Briefing:** `.deia/hive/coordination/2026-03-14-BRIEFING-voice-interface.md`
**Status:** Task files ready for Q33NR review

---

## Summary

I've created 3 task files to implement BL-045 Voice Interface using browser-native Web Speech API:

1. **TASK-080:** Voice Input (STT) — microphone button, speech recognition, visual feedback
2. **TASK-081:** Voice Output (TTS) — speaker buttons, auto-read, text-to-speech
3. **TASK-082:** Settings Integration — voice_enabled, voice_auto_read toggles

All task files follow DEIA standards: absolute paths, TDD requirements, 8-section response template, no stubs, var(--sd-*) CSS only.

---

## Task Breakdown

### TASK-080: Voice Input (STT) Hook + Component + Integration
**File:** `.deia/hive/tasks/2026-03-14-TASK-080-voice-input-stt.md`
**Model:** Sonnet
**Test Count:** 13+

**Deliverables:**
- `browser/src/primitives/terminal/useVoiceRecognition.ts` — hook for SpeechRecognition API
- `browser/src/primitives/terminal/VoiceInputButton.tsx` — 🎤 mic button component with pulsing indicator
- CSS additions to `terminal.css` — `.terminal-voice-btn`, pulsing animation
- Integration into `TerminalPrompt.tsx` — mic button next to 📎 file button
- 13+ tests (mock SpeechRecognition)

**Key Features:**
- Graceful fallback (hide button if API not supported)
- Visual pulsing red dot when listening
- Auto-stop after 3s silence timeout
- Stop on Enter key submit
- Interim results (transcript updates as user speaks)
- Vendor prefix handling (`webkitSpeechRecognition`)

**Dependencies:** None (standalone)

---

### TASK-081: Voice Output (TTS) Hook + Speaker Buttons
**File:** `.deia/hive/tasks/2026-03-14-TASK-081-voice-output-tts.md`
**Model:** Sonnet
**Test Count:** 13+

**Deliverables:**
- `browser/src/primitives/terminal/useSpeechSynthesis.ts` — hook for speechSynthesis API
- `browser/src/primitives/terminal/SpeakerButton.tsx` — 🔊 speaker button component
- CSS additions to `terminal.css` — `.terminal-speaker-btn`, pulsing animation
- Integration into `TerminalOutput.tsx` — speaker buttons on each response entry
- Integration into `TerminalPane.tsx` — wire auto-read setting
- 13+ tests (mock speechSynthesis)

**Key Features:**
- Graceful fallback (hide buttons if API not supported)
- Speaker icon changes to ⏸ when speaking
- Pulsing animation while speaking
- Auto-read mode (reads latest response if setting enabled)
- Only one message speaks at a time (stop previous)

**Dependencies:**
- TASK-082 (for auto-read setting, but can be mocked in tests)

---

### TASK-082: Voice Settings Integration
**File:** `.deia/hive/tasks/2026-03-14-TASK-082-voice-settings-integration.md`
**Model:** Sonnet
**Test Count:** 10+

**Deliverables:**
- Update `browser/src/primitives/settings/types.ts` — add `voice_enabled`, `voice_auto_read`
- Update `browser/src/primitives/settings/settingsStore.ts` — add getters/setters, defaults
- Settings UI component updates (find existing or create `SettingsPanel.tsx`)
- CSS for settings (if new component needed)
- 10+ tests

**Key Features:**
- `voice_enabled` defaults to true if SpeechRecognition API available
- `voice_auto_read` defaults to false
- Settings persist to localStorage immediately
- Help text for each setting
- Checkbox UI with var(--sd-*) styling

**Dependencies:** None (standalone)

---

## Test Coverage Summary

| Task | Test Files | Test Count | Mock Strategy |
|------|------------|------------|---------------|
| TASK-080 | 3 files | 13+ | Mock `webkitSpeechRecognition` constructor + instance |
| TASK-081 | 3 files | 13+ | Mock `window.speechSynthesis` + `SpeechSynthesisUtterance` |
| TASK-082 | 2 files | 10+ | Mock localStorage, mock SpeechRecognition availability |
| **Total** | **8 files** | **36+** | All browser APIs mocked |

---

## Acceptance Criteria Alignment

All acceptance criteria from spec (`2026-03-14-0300-SPEC-voice-interface.md`) covered:

- [x] Microphone button in terminal input area (TASK-080)
- [x] Click mic → starts listening → speech transcribed (TASK-080)
- [x] Visual indicator when listening (pulsing dot) (TASK-080)
- [x] Stop listening on: button click, silence timeout, Enter key (TASK-080)
- [x] TTS: speaker button on each message (TASK-081)
- [x] TTS uses browser `speechSynthesis` (TASK-081)
- [x] Settings: enable/disable voice, auto-read toggle (TASK-082)
- [x] Graceful fallback if API not supported (TASK-080, TASK-081)
- [x] 10+ tests → 36+ total (all tasks)
- [x] No file over 500 lines (all tasks checked)
- [x] CSS: var(--sd-*) only (all tasks)

---

## File Count and Size Estimates

**New files (9):**
- `useVoiceRecognition.ts` (~120 lines)
- `VoiceInputButton.tsx` (~80 lines)
- `useSpeechSynthesis.ts` (~100 lines)
- `SpeakerButton.tsx` (~60 lines)
- `SettingsPanel.tsx` (~90 lines, if needed)
- `settings.css` (~80 lines, if needed)
- 3 test files (~500 lines total)

**Modified files (5-7):**
- `TerminalPrompt.tsx` (+10 lines, 173→183)
- `TerminalOutput.tsx` (+40 lines, 220→260)
- `TerminalPane.tsx` (+5 lines)
- `terminal.css` (+60 lines CSS)
- `settingsStore.ts` (+50 lines, 210→260)
- `types.ts` (+2 lines)
- Possibly existing settings UI component (+30 lines)

**No file exceeds 500 lines.** Largest modified file will be TerminalOutput at ~260 lines.

---

## Dependencies and Dispatch Order

**Recommended dispatch order:**

1. **TASK-082** (settings) — independent, provides foundation
2. **TASK-080** and **TASK-081** in parallel — both depend on TASK-082 for settings, but can mock in tests

**Alternative (serial):**
1. TASK-082 (settings)
2. TASK-080 (voice input)
3. TASK-081 (voice output)

Both approaches work. Parallel is faster if bee capacity allows.

---

## Constraints Compliance

All task files comply with DEIA rules:

✅ **Rule 3:** No hardcoded colors — all CSS uses var(--sd-*)
✅ **Rule 4:** No file over 500 lines — all files checked
✅ **Rule 5:** TDD — tests written first, explicit in each task
✅ **Rule 6:** No stubs — explicit "no stubs" constraint in each task
✅ **Rule 8:** Absolute paths — all file paths absolute (Windows format)
✅ **Rule 9:** Response file template — 8-section template included in each task

---

## Risks and Mitigations

### Risk 1: Browser API Support Variability
**Mitigation:** Graceful fallbacks (hide buttons if API not available), vendor prefix handling, comprehensive mocking in tests.

### Risk 2: speechSynthesis "Speaking" State Stuck (rare bug)
**Mitigation:** TASK-081 includes 30s timeout auto-cancel if `synth.speaking` stuck.

### Risk 3: Settings UI Component Not Found
**Mitigation:** TASK-082 includes discovery step (Glob/Grep) + fallback to create minimal component.

### Risk 4: Terminal File Size (TerminalOutput 220 lines)
**Mitigation:** TASK-081 adds ~40 lines → 260 total (well under 500 limit).

---

## Ready for Review

All task files are complete and ready for Q33NR review. Each task:
- Has clear objective, context, and acceptance criteria
- Specifies all deliverables with absolute paths
- Includes comprehensive test requirements (36+ total tests)
- Follows TDD (tests first, then implementation)
- Uses var(--sd-*) CSS only
- Has 8-section response template
- Stays under 500-line file limit
- No stubs or TODOs

**Next steps:**
1. Q33NR reviews these 3 task files
2. Q33NR approves or requests corrections
3. Q33N dispatches bees (parallel: TASK-080 + TASK-081 after TASK-082, or serial)
4. Bees complete work, write response files
5. Q33N reviews responses, reports to Q33NR

---

**Files created:**
- `.deia/hive/tasks/2026-03-14-TASK-080-voice-input-stt.md`
- `.deia/hive/tasks/2026-03-14-TASK-081-voice-output-tts.md`
- `.deia/hive/tasks/2026-03-14-TASK-082-voice-settings-integration.md`
- `.deia/hive/responses/20260314-Q33N-VOICE-INTERFACE-TASK-FILES.md` (this file)
