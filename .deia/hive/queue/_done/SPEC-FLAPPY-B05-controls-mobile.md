---
id: FLAPPY-B05
priority: P2
model: sonnet
role: bee
depends_on: [FLAPPY-B04]
---
# SPEC-FLAPPY-B05: Controls + Mobile Responsiveness

## Priority
P2

## Model Assignment
sonnet

## Role
bee

## Depends On
- FLAPPY-B04 (visualization)

## Objective
Implement all controls (keyboard, touch, buttons) and mobile responsiveness.

## Context
This is Phase 5 of the Flappy Bird AI v2 build. Make the game playable on desktop and mobile.

Desktop:
- Spacebar to flap (in human mode)
- R to restart evolution
- 1/3/0 keys for speed (1x, 3x, 10x)

Mobile:
- Tap to flap (in human mode)
- On-screen buttons for speed and restart
- Responsive layout (canvas scales to screen size)

## You are in EXECUTE mode
**Write all code and tests. Do NOT enter plan mode. Do NOT ask for approval. Just build it.**

## Files to Read First
- `browser/public/games/flappy-b04-viz.js`
  Visualization from Phase 4
- `.deia/hive/responses/20260414-FLAPPY-V2-DESIGN-DOC.md`
  Design document with UX details

## Deliverables

### 1. Keyboard Controls
- [ ] Spacebar: flap in human mode
- [ ] R: restart evolution (reset to generation 1, new random population)
- [ ] 1: set speed to 1x
- [ ] 3: set speed to 3x
- [ ] 0: set speed to 10x (use 0 because 10 is two keys)
- [ ] M: toggle mode (AI ↔ Human)

### 2. Touch Controls
- [ ] Canvas tap: flap in human mode
- [ ] Prevent default touch behavior (no scroll, no zoom)
- [ ] Touch works on mobile devices (iOS, Android)

### 3. On-Screen Buttons (Mobile UI)
- [ ] Speed buttons: 1x, 3x, 10x (highlight active speed)
- [ ] Restart button (R)
- [ ] Mode toggle button (AI ↔ Human)
- [ ] Position: below canvas (per design doc)
- [ ] Style: large touch targets (44px min), clear labels
- [ ] Responsive: stack vertically on narrow screens

### 4. Mobile Responsiveness
- [ ] Canvas scales to fit screen width (max 600px wide on desktop, 100% on mobile)
- [ ] Maintain aspect ratio (don't squash)
- [ ] HUD scales appropriately
- [ ] Neural network viz scales or repositions for small screens
- [ ] Buttons are touch-friendly (not tiny)
- [ ] Test on viewport widths: 320px, 375px, 414px, 768px, 1024px

### 5. Accessibility
- [ ] Keyboard focus indicators on buttons
- [ ] ARIA labels for screen readers
- [ ] Color contrast (buttons, text, HUD)

## Test Requirements

Create: `browser/public/games/flappy-b05-test.html` (controls test file)

Test scenarios:
- [ ] Spacebar flaps in human mode
- [ ] R restarts evolution (generation resets to 1, new random birds)
- [ ] 1/3/0 keys change speed (verify speed indicator updates)
- [ ] M toggles mode (AI ↔ Human, verify bird count changes)
- [ ] Canvas tap flaps in human mode (simulate touch event)
- [ ] Speed buttons work (click 1x, 3x, 10x — verify active state)
- [ ] Restart button works (click R button — verify reset)
- [ ] Mode toggle button works (click M button — verify mode change)
- [ ] Canvas scales on window resize (test 320px, 768px widths)
- [ ] All buttons are at least 44px tall (mobile touch target size)
- [ ] Keyboard focus is visible (tab through buttons, verify outline)

Manual mobile test:
- Open on phone (or use Chrome DevTools mobile emulation)
- Tap to flap
- Tap speed buttons
- Tap restart button
- Verify no horizontal scroll
- Verify text is readable

## Constraints
- No external dependencies. Vanilla JS only.
- Target ~50 lines for this phase
- Touch targets must be 44x44px minimum (Apple HIG, Material Design)
- Keyboard shortcuts must not conflict with browser shortcuts
- No stubs — every function fully implemented

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `.deia/hive/responses/20260414-FLAPPY-B05-RESPONSE.md`

The response MUST contain these 8 sections:
1. **Header** — task ID, title, status (COMPLETE/FAILED), model, date
2. **Files Modified** — every file created/modified/deleted, full paths
3. **What Was Done** — bullet list of concrete changes
4. **Test Results** — test scenarios, mobile test observations
5. **Build Verification** — responsive test (320px, 768px, 1024px)
6. **Acceptance Criteria** — copy from task, mark [x] or [ ]
7. **Clock / Cost / Carbon** — all three, never omit any
8. **Issues / Follow-ups** — edge cases, dependencies, next tasks

DO NOT skip any section.

## Output Location
`browser/public/games/flappy-b05-controls.js` — controls code (will integrate into single HTML later)
`browser/public/games/flappy-b05-test.html` — test harness
`.deia/hive/responses/20260414-FLAPPY-B05-RESPONSE.md` — response file

## Acceptance Criteria
- [ ] Keyboard controls: Spacebar (flap), R (restart), 1/3/0 (speed), M (mode toggle)
- [ ] Touch controls: canvas tap to flap, no default scroll/zoom
- [ ] On-screen buttons: speed (1x/3x/10x), restart, mode toggle — min 44px touch targets
- [ ] Canvas scales responsively (100% width on mobile, max 600px on desktop)
- [ ] Aspect ratio maintained on resize
- [ ] Layout works at 320px, 375px, 414px, 768px, 1024px widths
- [ ] ARIA labels and keyboard focus indicators on all buttons
- [ ] Controls code at `browser/public/games/flappy-b05-controls.js`
- [ ] Response file at `.deia/hive/responses/20260414-FLAPPY-B05-RESPONSE.md`

## Smoke Test
- [ ] `test -f browser/public/games/flappy-b05-controls.js` passes
- [ ] `test -f browser/public/games/flappy-b05-test.html` passes
- [ ] `test -f .deia/hive/responses/20260414-FLAPPY-B05-RESPONSE.md` passes
