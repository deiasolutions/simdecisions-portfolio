# VERIFY: Voice-Input End-to-End

## Priority
P1

## Depends On
MW-005

## Objective
Comprehensive verification of voice input pipeline: speak → transcribe → parse → confirm → execute. Includes E2E tests, browser compatibility, mobile device testing, and error recovery.

## Context
MW-004 and MW-005 built the voice input stack. This task verifies it works correctly end-to-end across browsers, devices, and error conditions.

This is a VERIFY task — focused on testing, not building new features.

Files to verify:
- `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/browser/src/hooks/useVoiceInput.ts`
- `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/hivenode/routes/voice_routes.py`

## Acceptance Criteria
- [ ] E2E test: start mic → speak "open terminal" → receives PRISM-IR → command executes
- [ ] E2E test: speak gibberish → low confidence → shows disambiguation UI
- [ ] E2E test: deny mic permission → clear error message, graceful fallback
- [ ] Browser test: Chrome desktop — voice input works
- [ ] Browser test: Chrome Android — voice input works
- [ ] Browser test: Safari iOS — voice input works (or clear "not supported" message)
- [ ] Error recovery: network error during parse → retry logic or clear error
- [ ] Error recovery: mic error mid-recognition → stops cleanly, shows error
- [ ] Performance: end-to-end latency (speak → execute) <1 second for high-confidence commands
- [ ] Integration test file: `browser/src/hooks/useVoiceInput.integration.test.ts`
- [ ] All integration tests pass

## Smoke Test
- [ ] Run `npm test useVoiceInput.integration.test.ts` — all tests pass
- [ ] Manual test (Chrome): click mic → speak "open terminal" → terminal opens
- [ ] Manual test (Chrome): click mic → speak gibberish → shows error or alternatives
- [ ] Manual test (mobile emulator): touch mic → speak command → executes

## Model Assignment
sonnet

## Constraints
- Location: `browser/src/hooks/useVoiceInput.integration.test.ts` (enhance existing file)
- 6-10 E2E test cases covering full pipeline
- Max 250 lines for integration tests
- Use real HTTP requests (not mocked backend) for E2E tests
- Mock Web Speech API (browser API still mocked in tests)
- Test output: clear pass/fail with latency measurements
