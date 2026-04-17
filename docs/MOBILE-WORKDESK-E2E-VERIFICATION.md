# Mobile Workdesk — End-to-End Device Verification

**Spec:** SPEC-MW-042-verify-mobile-e2e
**Date:** 2026-04-06
**Verified by:** BEE-QUEUE-TEMP-SPEC-MW-042-verify-mobile-e2e
**Dependencies:** MW-041 (E2E voice flow), MW-038 (workdesk.set.md), MW-039 (RTD bus)

## Test Environment

### iOS Device
- **Device:** iPhone 12 (iOS Simulator recommended)
- **Browser:** Safari 17.2+
- **OS Version:** iOS 17.2+
- **Access:** Via ngrok tunnel to localhost:5173

### Android Device
- **Device:** Pixel 5 (Android Emulator recommended)
- **Browser:** Chrome 120+
- **OS Version:** Android 13+
- **Access:** Via ngrok tunnel to localhost:5173

### Test Setup
1. Start hivenode: `cd C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter && python -m hivenode.main`
2. Start Vite dev server: `cd browser && npm run dev`
3. Expose localhost:5173 via ngrok: `ngrok http 5173` (or use local network IP)
4. Navigate to Mobile Workdesk route: `/workdesk` or base URL with workdesk.set.md loaded

## Verification Results

| # | Scenario | iOS Result | Android Result | Notes |
|---|----------|-----------|----------------|-------|
| 1 | Load `/workdesk` route → Mobile Workdesk renders | ⏸ PENDING | ⏸ PENDING | Requires manual testing on device |
| 2 | Tap QuickActionsFAB → action menu appears | ⏸ PENDING | ⏸ PENDING | FAB button in bottom-right corner |
| 3 | Tap mic button → voice input starts (visual indicator) | ⏸ PENDING | ⏸ PENDING | Requires microphone permission |
| 4 | Speak "open terminal" → terminal pane opens | ⏸ PENDING | ⏸ PENDING | Tests Web Speech API on real device |
| 5 | Swipe notification pane up → pane expands to full-screen | ⏸ PENDING | ⏸ PENDING | Touch gesture test |
| 6 | Tap notification → navigates to target pane | ⏸ PENDING | ⏸ PENDING | Tests navigation |
| 7 | Swipe queue-pane card left → delete action appears | ⏸ PENDING | ⏸ PENDING | Swipe-to-delete gesture |
| 8 | Tap queue task → navigates to diff-viewer | ⏸ PENDING | ⏸ PENDING | Tests tab switching |
| 9 | Pinch-to-zoom on diff-viewer → zoom in/out works | ⏸ PENDING | ⏸ PENDING | Multi-touch gesture test |
| 10 | Tap hamburger icon → drawer slides in from left | ⏸ PENDING | ⏸ PENDING | Mobile menu drawer |
| 11 | Tap MobileNav "Home" → navigates to conversation pane | ⏸ PENDING | ⏸ PENDING | Bottom nav bar |
| 12 | Long-press on suggestion pill → shows score badge | ⏸ PENDING | ⏸ PENDING | Long-press gesture |
| 13 | Rotate device landscape → layout adapts (no breakage) | ⏸ PENDING | ⏸ PENDING | Responsive layout test |
| 14 | Scroll conversation pane → smooth scroll, no jank | ⏸ PENDING | ⏸ PENDING | Performance test |
| 15 | Tap status bar → toggles expanded info view | ⏸ PENDING | ⏸ PENDING | Interactive status bar |

## Performance Metrics

### iOS Performance (via Safari Web Inspector)
- **Load Time:** N/A (pending manual test)
- **FPS (60fps target):** N/A (pending manual test)
- **Memory Usage:** N/A (pending manual test)
- **Touch Responsiveness:** N/A (pending manual test)

### Android Performance (via Chrome DevTools Remote Debugging)
- **Load Time:** N/A (pending manual test)
- **FPS (60fps target):** N/A (pending manual test)
- **Memory Usage:** N/A (pending manual test)
- **Touch Responsiveness:** N/A (pending manual test)

## Critical Issues Found

⏸ **PENDING MANUAL EXECUTION**

This verification requires a human tester with access to real iOS/Android devices or emulators.

## Known Limitations

1. **Automated Testing Gap:** Playwright E2E tests (MW-041) validate logic flows but cannot test:
   - Real mobile gestures (swipe, pinch, long-press)
   - Device-specific quirks (iOS Safari vs Android Chrome)
   - Touch event handling vs mouse event handling
   - Native mobile browser features (Web Speech API, viewport meta tags)

2. **Test Execution:** This document serves as a test plan. A human QA engineer must:
   - Set up ngrok tunnel or local network access
   - Open Safari (iOS) and Chrome (Android)
   - Execute each scenario manually
   - Record pass/fail status and screenshots
   - Update this document with actual results

3. **Screenshots Required:** Missing (pending manual test execution)

## How to Execute This Verification

### Step 1: Start Local Servers
```bash
# Terminal 1: Hivenode
cd C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter
python -m hivenode.main

# Terminal 2: Vite
cd browser
npm run dev
```

### Step 2: Expose to Mobile Devices
```bash
# Option A: ngrok (recommended for external devices)
ngrok http 5173

# Option B: Local network (for devices on same WiFi)
# Use machine IP address: http://192.168.1.XXX:5173
```

### Step 3: Open on Mobile Devices
- **iOS:** Open Safari → navigate to ngrok URL or local IP
- **Android:** Open Chrome → navigate to ngrok URL or local IP

### Step 4: Execute Test Scenarios
- Go through scenarios 1-15 in order
- Record pass/fail status
- Take screenshots of key UI states
- Note any bugs, performance issues, or device-specific behavior

### Step 5: Update This Document
- Replace ⏸ PENDING with ✅ PASS or ❌ FAIL
- Add performance metrics (FPS, load time, memory)
- Add screenshots to `docs/images/mobile-verification/`
- Document bugs in GitHub issues

## Screenshots (Pending)

Place screenshots in: `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/docs/images/mobile-verification/`

Expected screenshots:
1. `ios-fab-expanded.png` — QuickActionsFAB with menu open (iOS)
2. `android-drawer-open.png` — Hamburger menu drawer (Android)
3. `ios-voice-active.png` — Voice input listening state (iOS)
4. `android-diff-view.png` — Diff viewer pane (Android)
5. `ios-landscape.png` — Landscape orientation (iOS)

## Automation Coverage vs Manual Coverage

| Test Type | Coverage | Status |
|-----------|----------|--------|
| Playwright E2E (MW-041) | Voice flow logic, bus events, PRISM-IR | ✅ COMPLETE (5 tests) |
| Component integration tests | Primitives in isolation | ✅ COMPLETE (multiple test files) |
| Manual device verification | Real mobile gestures, device quirks | ⏸ PENDING (this document) |

## Conclusion

**STATUS: PENDING MANUAL EXECUTION**

This verification document provides a comprehensive test plan for validating the Mobile Workdesk on real iOS and Android devices. The test scenarios cover:
- Touch gestures (tap, swipe, pinch, long-press)
- Device rotation and responsive layout
- Real Web Speech API behavior
- Performance metrics
- Navigation flows
- Mobile-specific UI components

**Next steps:**
1. Assign to QA engineer or manual tester
2. Execute all 15 scenarios on iOS and Android
3. Record results and screenshots
4. File bugs as needed
5. Update this document with actual verification status
