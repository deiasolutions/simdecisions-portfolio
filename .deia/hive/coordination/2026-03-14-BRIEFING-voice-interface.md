# BRIEFING: BL-045 Voice Interface — Browser Native STT/TTS

**Date:** 2026-03-14
**For:** Q33N (coordinator)
**From:** Q88NR (regent)
**Model Assignment:** Sonnet
**Priority:** P2

---

## Objective

Add voice input (speech-to-text) and voice output (text-to-speech) to the terminal using browser-native Web Speech API. No external dependencies.

---

## Context from Spec

The spec requests:
- Microphone button in terminal input area (unicode icon, no images)
- Click mic → starts listening → speech transcribed to text in input field
- Visual indicator when listening (pulsing dot, CSS animation)
- Stop listening on: button click, silence timeout (3s), or Enter key
- TTS: AI responses can be read aloud via speaker button on each message
- TTS uses browser `speechSynthesis` — no external API
- Settings: enable/disable voice, auto-read responses toggle
- Graceful fallback if browser doesn't support SpeechRecognition (hide mic button)
- 10+ tests (mock SpeechRecognition API in tests)
- No file over 500 lines
- CSS: var(--sd-*) only

**Model Assignment:** sonnet

---

## Architecture Notes

### Current Terminal Structure

The terminal uses:
- **TerminalPrompt.tsx** — handles the textarea input with file attachments (line 1-173)
- **TerminalOutput.tsx** — renders terminal entries (line 1-219)
- **useTerminal.ts** — state management hook (line 1-717)

The prompt already has a file attachment button (`📎`) pattern we can mirror for the mic button.

### Web Speech API

Browser-native APIs:
- **SpeechRecognition:** `window.SpeechRecognition || window.webkitSpeechRecognition`
- **SpeechSynthesis:** `window.speechSynthesis`

Both are well-supported in modern browsers (Chrome, Edge, Safari). Firefox has partial support.

### Implementation Strategy

**Voice Input (STT):**
1. Create `VoiceInput.tsx` component with mic button
2. Wrap SpeechRecognition in a React hook (`useVoiceRecognition.ts`)
3. Integrate mic button into `TerminalPrompt.tsx` next to file attachment button
4. Add visual indicator (pulsing dot) when listening
5. Transcription appends to textarea value (same as typing)

**Voice Output (TTS):**
1. Create `useSpeechSynthesis.ts` hook
2. Add speaker button to each response entry in `TerminalOutput.tsx`
3. Add settings for auto-read responses in settings store
4. Wire to settings UI (primitives/settings/)

**Settings:**
- `voice_enabled: boolean` (default: true if API available)
- `voice_auto_read: boolean` (default: false)
- Store in `localStorage` under `sd_user_settings`

---

## Files to Read First

- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\terminal\TerminalPrompt.tsx`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\terminal\TerminalOutput.tsx`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\terminal\useTerminal.ts`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\settings\settingsStore.ts`

---

## Task Breakdown Guidance

Suggested task structure:

1. **TASK-XXX:** Voice input hook + component (STT)
   - Deliverable: `useVoiceRecognition.ts` hook
   - Deliverable: `VoiceInput.tsx` component (mic button + indicator)
   - Deliverable: Integration into `TerminalPrompt.tsx`
   - Tests: 5+ (mock SpeechRecognition, test start/stop, timeout, graceful fallback)

2. **TASK-YYY:** Voice output hook + UI (TTS)
   - Deliverable: `useSpeechSynthesis.ts` hook
   - Deliverable: Speaker button in `TerminalOutput.tsx` for each response
   - Deliverable: Auto-read logic when enabled
   - Tests: 5+ (mock speechSynthesis, test speak/stop, auto-read)

3. **TASK-ZZZ:** Settings integration
   - Deliverable: Add `voice_enabled`, `voice_auto_read` to settings store
   - Deliverable: Settings UI controls (toggle switches)
   - Tests: 2+ (settings persistence)

---

## Constraints

- **No file over 500 lines.** Modularize at 500. Hard limit: 1,000.
- **CSS: var(--sd-*) only.** No hex, no rgb(), no named colors.
- **No stubs.** Every function fully implemented.
- **TDD.** Tests first, then implementation.
- **Browser-native APIs ONLY.** No npm dependencies for speech.
- **Graceful fallback:** Hide mic button if API not available.

---

## Acceptance Criteria (from spec)

- [ ] Microphone button in terminal input area (unicode icon, no images)
- [ ] Click mic → starts listening → speech transcribed to text in input field
- [ ] Visual indicator when listening (pulsing dot, CSS animation)
- [ ] Stop listening on: button click, silence timeout (3s), or Enter key
- [ ] TTS: AI responses can be read aloud via speaker button on each message
- [ ] TTS uses browser `speechSynthesis` — no external API
- [ ] Settings: enable/disable voice, auto-read responses toggle
- [ ] Graceful fallback if browser doesn't support SpeechRecognition (hide mic button)
- [ ] 10+ tests (mock SpeechRecognition API in tests)
- [ ] No file over 500 lines
- [ ] CSS: var(--sd-*) only

---

## Review Checklist

Before submitting task files to me:
1. Every acceptance criterion has a corresponding deliverable in a task
2. All file paths are absolute (Windows format for this repo)
3. Test requirements specified (count, scenarios, mock strategy)
4. CSS uses var(--sd-*) only
5. No file over 500 lines
6. No stubs or TODOs
7. Response file template included in each task

---

## Next Steps

1. Read the referenced terminal files to understand current structure
2. Write 3 task files (STT hook+component, TTS hook+UI, settings integration)
3. Return task files to me for review
4. After approval, dispatch bees

---

**End of Briefing**
