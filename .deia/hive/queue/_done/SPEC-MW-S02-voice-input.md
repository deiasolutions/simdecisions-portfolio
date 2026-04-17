# SPEC: Voice-Input Web Speech API Wrapper

## Priority
P1

## Objective
Design a React hook for Web Speech API integration that captures voice input, streams transcription, and pipes to command-interpreter for real-time command execution on the Mobile Workdesk.

## Context
Voice input is a critical input surface for mobile. We need a reusable hook that:
- Initializes Web Speech API (with fallback detection)
- Handles microphone permissions
- Streams interim and final transcriptions
- Manages error states gracefully
- Integrates cleanly with command-interpreter for command routing

Files to read first:
- `browser/src/hooks/useMicrophone.ts` — any existing mic utilities (if any)
- `browser/src/primitives/command-palette/CommandPalette.tsx` — command routing pattern
- MDN: Web Speech API (SpeechRecognition, SpeechRecognitionEvent)
- `hivenode/shell/command_interpreter.py` — the consumer of voice transcription

## Acceptance Criteria
- [ ] `useVoiceInput()` hook returns: { transcript, isListening, confidence, error, start, stop, abort }
- [ ] Web Speech API with fallback to mock/stub if not available in test environment
- [ ] Microphone permission request + clear user-facing error if denied
- [ ] Real-time transcript updates (interim results) as user speaks
- [ ] On final result: pipe through command-interpreter for confidence scoring
- [ ] Confidence score from Web Speech API integrated into hook state
- [ ] Error handling: microphone error, aborted recognition, network error
- [ ] Browser compatibility check (Chrome, Safari, Edge)
- [ ] Hook automatically cleans up mic access on unmount
- [ ] 12+ unit tests + 2 integration tests

## Smoke Test
- [ ] Mount component with `useVoiceInput()` — no errors, mic access requested
- [ ] Call `start()` — listening state updates, interim transcriptions appear
- [ ] Say command ("open terminal") — final transcript captured with confidence score
- [ ] Say gibberish — confidence low, error state clear
- [ ] Call `stop()` — mic access released

## Model Assignment
sonnet

## Constraints
- Location: `browser/src/hooks/useVoiceInput.ts` (new file)
- Location: `browser/src/hooks/useVoiceInput.test.ts`
- TDD: tests first (mock Web Speech API via jest.mock)
- Mock Web Speech API for tests — do NOT require actual browser/mic in test
- No blocking async — all non-blocking via callbacks/state
- Max 250 lines for hook
- Max 150 lines for tests
- All CSS variables only (no hardcoded colors)
- No external libs beyond React + existing test setup
