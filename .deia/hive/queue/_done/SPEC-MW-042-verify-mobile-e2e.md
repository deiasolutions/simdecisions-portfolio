# SPEC: VERIFY — End-to-End Mobile Device Test

## Priority
P2

## Objective
Execute full end-to-end verification of the Mobile Workdesk on a real mobile device or emulator. Tests all primitives, gestures, navigation, voice input, and responsive layouts across iOS and Android. Validates that the product works correctly on actual mobile hardware, not just desktop browsers with responsive mode.

## Context
The Mobile Workdesk is designed for mobile-first usage. While Playwright tests (MW-041) validate logic flows, they don't test real mobile gestures (swipe, pinch, long-press), touch events, or device-specific quirks. This spec uses real device testing to catch mobile-only bugs.

Files to read first:
- `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/.deia/hive/queue/backlog/SPEC-MW-041-e2e-voice-flow.md` — Playwright E2E test (desktop)
- `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/.deia/hive/queue/backlog/SPEC-MW-038-workdesk-egg.md` — Mobile Workdesk EGG config
- `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/browser/src/shell/components/Shell.tsx` — responsive shell
- `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/hivenode/scheduler/scheduler_mobile_workdesk.py:158` — task context in scheduler

## Dependencies
- MW-041 (E2E voice flow test must pass before mobile verification)
- MW-038 (workdesk.set.md EGG must exist)
- MW-039 (RTD bus integration must be complete)

## Acceptance Criteria
- [ ] Test document: `docs/MOBILE-WORKDESK-E2E-VERIFICATION.md` with test scenarios and results
- [ ] Test environment:
  - iOS device: iPhone 12+ or iPad (Safari browser)
  - Android device: Pixel 5+ (Chrome browser)
  - Or emulators: iOS Simulator (Xcode) + Android Emulator (Android Studio)
- [ ] Test scenarios (15 total):
  - **Scenario 1:** Load `/workdesk` route → Mobile Workdesk renders without errors
  - **Scenario 2:** Tap QuickActionsFAB → action menu appears
  - **Scenario 3:** Tap mic button → voice input starts (visual indicator)
  - **Scenario 4:** Speak "open terminal" → terminal pane opens
  - **Scenario 5:** Swipe notification pane up → pane expands to full-screen
  - **Scenario 6:** Tap notification → navigates to target pane
  - **Scenario 7:** Swipe queue-pane card left → delete action appears
  - **Scenario 8:** Tap queue task → navigates to diff-viewer
  - **Scenario 9:** Pinch-to-zoom on diff-viewer → zoom in/out works
  - **Scenario 10:** Tap hamburger icon → drawer slides in from left
  - **Scenario 11:** Tap MobileNav "Home" → navigates to conversation pane
  - **Scenario 12:** Long-press on suggestion pill → shows score badge
  - **Scenario 13:** Rotate device landscape → layout adapts (no breakage)
  - **Scenario 14:** Scroll conversation pane → smooth scroll, no jank
  - **Scenario 15:** Tap status bar → toggles expanded info view
- [ ] Results table: each scenario has columns [Scenario, iOS Result, Android Result, Notes]
- [ ] Screenshots: 5+ screenshots of key UI states (FAB, drawer, voice active, diff view, notifications)
- [ ] Performance metrics: record FPS, load time, memory usage (Chrome DevTools remote debugging)
- [ ] Bug log: document any bugs found (file as GitHub issues or JIRA tickets)

## Smoke Test
- [ ] All 15 scenarios executed on iOS device/emulator
- [ ] All 15 scenarios executed on Android device/emulator
- [ ] Results documented in `docs/MOBILE-WORKDESK-E2E-VERIFICATION.md`
- [ ] At least 13/15 scenarios pass (90% success rate)
- [ ] Critical bugs (app crashes, data loss) are zero
- [ ] Screenshots attached to verification doc

## Model Assignment
sonnet

## Constraints
- Location: `docs/MOBILE-WORKDESK-E2E-VERIFICATION.md` (new file)
- Use real devices or official emulators (no third-party browser testing services)
- Remote debugging: use Chrome DevTools (Android) or Safari Web Inspector (iOS)
- Ngrok or similar for exposing localhost:5173 to mobile devices (if testing on real hardware)
- Document test environment details (device model, OS version, browser version)
- Max 80 lines for verification doc (concise table format)
- Include pass/fail status for each scenario
- Include screenshots (embed or link to images/)
