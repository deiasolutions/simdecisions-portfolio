# RAIDEN-R02: Mobile Shmup Controls Research -- COMPLETE

**Status:** COMPLETE
**Model:** Sonnet
**Date:** 2026-04-13

## Files Modified

- Created: `C:\Users\davee\OneDrive\Documents\GitHub\simdecisions\.deia\hive\responses\20260413-RAIDEN-R02-MOBILE-CONTROLS-RESEARCH.md`

## What Was Done

- Researched virtual joystick patterns across modern mobile shmups (Sky Force, Phoenix HD, industry examples)
- Analyzed fixed vs floating joystick implementations with UX best practices
- Investigated auto-fire vs manual fire player preferences and industry standards
- Documented bomb/special weapon button placement and UX patterns
- Evaluated tilt controls as alternative input method with pros/cons analysis
- Researched mobile shmup UI layout, safe zones, and accessibility guidelines
- Determined performance targets for 60fps HTML5 Canvas games on mobile
- Compiled specific recommendations with rationale and research citations
- Created ASCII diagram showing recommended screen layout
- Documented all specs (joystick type, size, position, visual feedback, button sizes)
- Included 18 research sources with proper citations

## Tests Run

Smoke test passed:
- Research file exists at expected location
- Contains all required sections (Recommended Control Scheme, Virtual Joystick Specs, etc.)
- All 8 required sections complete with no TBD or placeholders

## Acceptance Criteria Met

- [x] Specific control scheme recommended with rationale (floating joystick + auto-fire + bomb button)
- [x] Joystick specs defined (type: floating, size: 120px, position: left 50%, visual feedback: opacity/glow)
- [x] Fire control decision made (auto-fire: YES) with justification from research
- [x] Bomb button placement and design specified (bottom-right, 80px diameter, with cooldown overlay)
- [x] Screen layout diagram provided (ASCII portrait layout with safe zones)
- [x] Performance targets documented (60fps target, <16ms latency, Canvas 2D rendering)
- [x] All sections complete (no TBD, no placeholders)

## Key Recommendations Summary

1. **Control Scheme:** Floating joystick (left) + auto-fire + bomb button (right)
2. **Orientation:** Portrait (vertical) - standard for vertical shmups, 73% of top games use portrait
3. **Joystick:** Floating (appears where thumb touches), 120px diameter, left 50% active area
4. **Fire:** Auto-fire (industry standard for mobile shmups, reduces cognitive load)
5. **Bomb:** Fixed button bottom-right, 80px diameter, visible cooldown indicator
6. **Tilt:** Optional setting only (viable but less precise, good for variety)
7. **Performance:** 60fps target, Canvas 2D with hardware acceleration, <16ms input latency
8. **Accessibility:** 80px+ buttons (exceeds 48dp minimum), high contrast, customizable UI scale

## Blockers

None

## Notes

Research based on current mobile shmup industry standards (2026), academic studies on touch vs tilt controls, accessibility guidelines from Material Design and Apple HIG, and HTML5 Canvas performance optimization best practices. All recommendations are implementation-ready with specific pixel values and technical rationale.
