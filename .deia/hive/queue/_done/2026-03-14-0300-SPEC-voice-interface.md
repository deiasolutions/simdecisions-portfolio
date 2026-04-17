# SPEC: BL-045 Voice Interface — Browser Native STT/TTS

## Priority
P2

## Objective
Add voice input and output to the terminal using browser-native Web Speech API. No external dependencies.

## Context
Uses `window.SpeechRecognition` (or `webkitSpeechRecognition`) for speech-to-text and `window.speechSynthesis` for text-to-speech. Wire to terminal input/output.

Files to read first:
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\terminal\TerminalInput.tsx`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\terminal\TerminalOutput.tsx`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\terminal\useTerminal.ts`

## Acceptance Criteria
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

## Model Assignment
sonnet

## Constraints
- Browser-native APIs ONLY — no external speech services
- No npm dependencies for speech
- Separate file: `browser/src/primitives/terminal/VoiceInput.tsx`
