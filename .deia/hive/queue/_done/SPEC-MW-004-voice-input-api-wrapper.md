# SPEC: Voice-Input Web Speech API Wrapper

## Priority
P1

## Depends On
MW-T02, MW-V01

## Objective
Build a React hook wrapper for Web Speech API that provides voice input with real-time transcription, confidence scoring, error handling, and integration with command-interpreter.

## Context
Voice input is critical for mobile UX. This task builds `useVoiceInput()` hook that:
- Wraps Web Speech API with clean React state management
- Handles microphone permissions gracefully
- Streams interim and final transcriptions
- Integrates with command-interpreter for real-time command execution

NOTE: `useVoiceInput.ts` already exists in the codebase (written in a previous sprint). This task ENHANCES it with command-interpreter integration and mobile-specific optimizations.

Files to read first:
- `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/browser/src/hooks/useVoiceInput.ts` — existing implementation
- `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/hivenode/shell/command_interpreter.py` — consumer of voice input

## Acceptance Criteria
- [ ] Review existing `useVoiceInput.ts` implementation
- [ ] Add `onInterimTranscript` callback for real-time streaming (not just final)
- [ ] Add `commandInterpreter` option to auto-parse transcripts
- [ ] Add `autoExecute` option to automatically execute high-confidence commands
- [ ] Add mobile-specific error handling: microphone blocked, background tab, iOS Safari quirks
- [ ] Update tests to cover new command-interpreter integration
- [ ] Add integration test: speak → transcribe → parse → emit PRISM-IR
- [ ] Performance: transcription latency <200ms on typical mobile device
- [ ] Browser compat: Chrome Android, Safari iOS, Samsung Internet
- [ ] Hook cleanup: always release mic on unmount, even if error occurred
- [ ] Documentation: JSDoc comments with usage examples

## Smoke Test
- [ ] Mount component with `useVoiceInput({ commandInterpreter: true })` — no errors
- [ ] Call `start()` — mic permission requested, listening state updates
- [ ] Speak "open terminal" → interim transcript shows "open..." → final transcript "open terminal"
- [ ] With `autoExecute: true` and high confidence → command auto-executes
- [ ] With `autoExecute: false` → transcript captured, no execution
- [ ] Call `stop()` → mic released, isListening = false

## Model Assignment
sonnet

## Constraints
- Location: `browser/src/hooks/useVoiceInput.ts` (ENHANCE existing file)
- Location: `browser/src/hooks/useVoiceInput.test.ts` (update existing tests)
- TDD: Update tests first to cover new features
- Mock Web Speech API in tests (no real browser/mic required)
- Max 300 lines for hook (add ~50 lines to existing)
- Max 200 lines for tests (add ~50 lines to existing)
- NO STUBS — full implementation of command-interpreter integration
- Must be backward compatible with existing usage (non-breaking changes only)
