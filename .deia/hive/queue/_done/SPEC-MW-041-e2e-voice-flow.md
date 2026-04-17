# SPEC: E2E Test — Voice to PRISM-IR Flow

## Priority
P2

## Objective
Create an end-to-end Playwright test that exercises the complete voice-to-execution workflow: user speaks command → voice recognition → command interpreter → PRISM-IR emission → execution → UI updates. This validates the entire Mobile Workdesk pipeline.

## Context
The Mobile Workdesk integrates multiple systems: Web Speech API (voice input), command-interpreter (NL parsing), PRISM-IR (command schema), RTD bus (event routing), and primitives (execution). This E2E test ensures the full pipeline works correctly with no integration gaps.

Files to read first:
- `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/browser/e2e/hodeia-auth.spec.ts` — example Playwright E2E test
- `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/browser/e2e/chat-smoke.spec.ts` — example smoke test
- `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/.deia/hive/queue/backlog/SPEC-MW-040-prism-ir-vocabulary.md` — PRISM-IR schema
- `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/browser/src/primitives/terminal/useVoiceRecognition.ts` — voice input hook
- `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/hivenode/scheduler/scheduler_mobile_workdesk.py:157` — task context in scheduler

## Dependencies
- MW-040 (PRISM-IR vocabulary must be defined before testing)

## Acceptance Criteria
- [ ] Playwright test file: `browser/e2e/mobile-workdesk-voice-flow.spec.ts`
- [ ] Test setup:
  - Start local hivenode server (localhost:8420)
  - Start Vite dev server (localhost:5173)
  - Navigate to `/workdesk` route
  - Wait for Mobile Workdesk to load
- [ ] Test scenario 1: Voice command → terminal open
  - Mock Web Speech API (Playwright can't trigger real voice, use stub/mock)
  - Emit mock transcript: "open terminal"
  - Wait for command-interpreter to parse
  - Assert PRISM-IR emitted: `{ "command": "open", "target": "terminal", "confidence": 0.95 }`
  - Assert terminal pane becomes visible
- [ ] Test scenario 2: Ambiguous command → confirmation dialog
  - Emit mock transcript: "open file" (ambiguous)
  - Assert confirmation dialog appears with alternatives
  - Click "Open Text Pane" option
  - Assert text-pane becomes visible
- [ ] Test scenario 3: Low confidence → picker
  - Emit mock transcript: "xyz foo bar" (gibberish)
  - Assert command picker appears with suggestions
  - Select "Search" from picker
  - Assert search pane becomes visible
- [ ] All tests use Playwright assertions (`expect(...)`)
- [ ] Tests clean up (close servers) after completion
- [ ] Tests run in CI (GitHub Actions compatible)
- [ ] Total: 3 E2E scenarios covering happy path, ambiguity, low confidence

## Smoke Test
- [ ] Run `npx playwright test mobile-workdesk-voice-flow.spec.ts`
- [ ] All 3 scenarios pass
- [ ] No console errors during test execution
- [ ] Test completes in <30 seconds (excluding server startup)

## Model Assignment
sonnet

## Constraints
- Location: `browser/e2e/mobile-workdesk-voice-flow.spec.ts` (new file)
- Use Playwright test framework (already in project)
- Mock Web Speech API (use `page.evaluate()` to stub `SpeechRecognition`)
- Tests must be deterministic (no flaky timing issues)
- Use `page.waitForSelector()` for assertions (not arbitrary timeouts)
- Max 300 lines for test file
- Include setup/teardown in `beforeAll`/`afterAll`
- Tests must pass in headless mode (CI compatible)
