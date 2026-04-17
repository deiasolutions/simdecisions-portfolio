# RAIDEN-R02: Mobile Shmup Controls Research -- COMPLETE

**Status:** COMPLETE
**Model:** Sonnet
**Date:** 2026-04-08

## Files Modified
- Created: `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260408-RAIDEN-R02-MOBILE-CONTROLS-REFERENCE.md`

## What Was Done
- Researched 5+ mobile vertical scrolling shoot-em-up control schemes
- Analyzed touch input patterns: direct touch, floating joystick, fixed joystick, drag-to-move, tilt
- Documented auto-fire vs manual shooting UX patterns
- Researched thumb reach zones and mobile ergonomics (75% of touches use thumb)
- Investigated haptic feedback patterns for mobile shooters
- Compiled visual design recommendations for touch zones, buttons, and feedback
- Created comprehensive UX recommendation document with specific measurements and layouts

## Key Findings

### Control Schemes Analyzed
1. **Sky Force Reloaded:** Direct swipe-to-move, auto-fire, 1:1 tracking
2. **Raiden Legacy:** Drag controls with speed modes (120%, 150%, 200%), repositionable buttons
3. **DoDonPachi Resurrection:** Bottom-zone slide controls, auto-fire, mode-switch buttons
4. **Phoenix 2:** Direct touch-and-drag, gesture-based abilities
5. **Geometry Wars:** Dual-stick (reference for twin-stick shooters)

### Recommended Control Scheme
- **Primary Method:** Hybrid direct touch (1:1 tracking) + floating anchor fallback
- **Touch Zone:** Bottom 25% of screen (green thumb zone for easy reach)
- **Auto-Fire:** Enabled by default (reduces cognitive load, focus on dodging)
- **Sensitivity:** 3 presets (Normal 1×, Fast 1.5×, Turbo 2×)
- **Bomb Button:** 88×88px in right thumb zone with haptic feedback
- **Orientation:** Portrait mode (locked), landscape optional for tablets

### Touch Zone Layout (Portrait)
```
┌─────────────────────────────┐
│     PLAYFIELD (75%)         │  ← Bullets, enemies, ship
│                             │
├─────────────────────────────┤
│  [Movement Zone] (25%)      │  ← Bottom green zone
│  [Bomb]          [Pause]    │  ← Right-side buttons
└─────────────────────────────┘
```

### Specific Measurements
- **Movement Zone:** Full width, bottom 167px on 375×667px baseline
- **Bomb Button:** 88×88px at X:270px, Y:550px
- **Pause Button:** 64×64px at X:300px, Y:20px
- **Minimum Touch Target:** 44×44px (accessibility standard)
- **Recommended Target:** 48×48px with 8px spacing

### Haptic Feedback Patterns
- **Ship Hit:** Sharp 50ms strong vibration
- **Bomb Activation:** 200ms sustained medium rumble
- **Power-Up Collect:** 30ms light pulse
- **Boss Spawn:** Three 100ms pulses

### Implementation Notes
- **Touch Event Handling:** Use `touchstart`/`touchmove`/`touchend` (avoid click delay)
- **Input Smoothing:** Lerp at 15% per frame to prevent jitter
- **Multi-Touch:** Track first touch only, ignore secondary touches
- **Performance:** Poll every frame (requestAnimationFrame), no throttling

### User Preference Options
- Auto-fire toggle (on/off)
- Sensitivity slider (1×, 1.5×, 2×)
- Haptic feedback toggle
- Tilt controls toggle
- Button size presets (Small 64px, Medium 88px, Large 112px)
- One-handed mode (left/right)

## Research Sources
Documented 15+ sources including:
- TouchArcade game reviews (Sky Force, Phoenix 2)
- App Store listings (Raiden Legacy, DoDonPachi)
- UX research articles (Parachute Design, Smashing Magazine, Elaris)
- Academic papers (York University tilt-touch synergy, ACM haptics research)
- Mobile game ergonomics studies (CMS Conferences)
- Virtual joystick UI analysis (Medium, Unity discussions)

## Acceptance Criteria
- [x] UX recommendation document written to `.deia/hive/responses/20260408-RAIDEN-R02-MOBILE-CONTROLS-REFERENCE.md`
- [x] At least 5 mobile shmup control schemes analyzed (analyzed 5)
- [x] Recommended control scheme with specific touch zone layout (included with pixel measurements)
- [x] Visual mockup description (ASCII diagrams for portrait and landscape)
- [x] Implementation notes for touch event handling (JavaScript pseudocode included)
- [x] User preference options documented (7 settings with detailed descriptions)

## Smoke Test
```bash
test -f "C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260408-RAIDEN-R02-MOBILE-CONTROLS-REFERENCE.md" && echo PASS || echo FAIL
```
Result: PASS

## Deliverable Summary
Created a comprehensive 12-section UX recommendation document (6,800+ words) covering:
1. Control schemes in 5+ popular mobile shmups
2. Touch input pattern analysis (direct touch, joystick variants, tilt)
3. Auto-fire vs manual shooting recommendations
4. Screen real estate and thumb reach zones (research-backed measurements)
5. Accessibility and comfort considerations
6. Recommended hybrid control scheme with specific layout
7. Implementation pattern with pseudocode
8. Visual design specifications
9. Performance considerations (latency, smoothing, battery)
10. User preference options menu
11. Portrait vs landscape analysis
12. Fallback accessibility options

Document is ready for immediate use by RAIDEN game engine implementation teams.

## Next Steps (Not Part of This Spec)
- RAIDEN-R01 will handle core shmup mechanics (bullets, enemies, collision)
- RAIDEN-101 will implement the game engine using recommendations from this research

## Notes
- No code was written (research-only task as specified)
- All sources cited with markdown hyperlinks
- Specific pixel measurements provided for immediate implementation
- Document balances accessibility (casual players) with precision (hardcore shmup fans)
