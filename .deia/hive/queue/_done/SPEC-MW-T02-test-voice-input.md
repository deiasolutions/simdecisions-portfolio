# SPEC: TEST — Voice-Input Hook Coverage

## Priority
P1

## Objective
Write comprehensive test suite for the useVoiceInput() hook that validates Web Speech API integration, microphone permissions, transcript streaming, error handling, and cleanup with 100% coverage.

## Context
This is a TDD task — write tests FIRST, before implementation exists. Tests must fail initially, then pass after MW-004/MW-005 implementation.

Test coverage must include:
- Hook initialization: returns correct state shape { transcript, isListening, confidence, error, start, stop, abort }
- Start recording: isListening becomes true, mic permission requested
- Interim results: transcript updates in real-time as user speaks
- Final result: confidence score captured, transcript finalized
- Stop recording: isListening becomes false, mic access released
- Error states: permission denied, network error, aborted recognition
- Cleanup: mic access released on unmount
- Browser compatibility: fallback when Web Speech API not available

Files to read first:
- `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/.deia/hive/queue/backlog/SPEC-MW-S02-voice-input.md` — spec to test against
- `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/browser/src/hooks/useVoiceInput.ts` — hook structure (if exists from previous task)
- `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/browser/src/hooks/useVoiceInput.test.ts` — existing test patterns (if any)
- `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/hivenode/scheduler/scheduler_mobile_workdesk.py:70` — task context

## Acceptance Criteria
- [ ] Test file: `browser/src/hooks/useVoiceInput.test.ts` (Jest + React Testing Library)
- [ ] 12+ test cases covering: init, start, interim, final, stop, errors, cleanup, fallback
- [ ] Mock Web Speech API: jest.mock for SpeechRecognition, SpeechRecognitionEvent
- [ ] Test microphone permission flow: mock navigator.permissions.query
- [ ] Test interim transcript updates: simulate multiple onresult events
- [ ] Test confidence score: validate range 0.0-1.0
- [ ] Test error handling: permission denied → error state set, network error → error state set
- [ ] Test cleanup: unmount → mic access released (verify SpeechRecognition.stop called)
- [ ] Test browser compatibility: Web Speech API undefined → fallback state
- [ ] Tests initially FAIL (no implementation exists yet)
- [ ] All tests use renderHook from @testing-library/react-hooks
- [ ] No stubs in tests — real assertions with expected values

## Smoke Test
- [ ] Run `npm test useVoiceInput.test.ts` → 12+ tests FAIL (hook doesn't exist yet)
- [ ] Check test_start_recording() → asserts isListening === true
- [ ] Check test_interim_results() → asserts transcript updates incrementally
- [ ] Check test_permission_denied() → asserts error.type === "permission-denied"
- [ ] Check test_cleanup() → asserts stop() called on unmount
- [ ] All tests use descriptive names (test_* or it("should ..."))

## Model Assignment
sonnet

## Depends On
MW-S02

## Constraints
- Location: `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/browser/src/hooks/useVoiceInput.test.ts` (new file)
- TDD: tests MUST be written before implementation (they will fail initially)
- Max 300 lines for test file
- Use jest.mock() to mock Web Speech API
- Use @testing-library/react-hooks for hook testing
- No implementation code in this task — tests only
- Tests must be runnable even if `useVoiceInput.ts` doesn't exist yet (import should handle missing module gracefully)
