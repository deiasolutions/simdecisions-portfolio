---
id: FLAPPY-001
priority: P2
model: sonnet
role: bee
depends_on: []
---
# SPEC-FLAPPY-001: Flappy Bird Clone

## Role Override
bee

## Priority
P2

## Model Assignment
sonnet

## Depends On
(none)

## Intent
Build a standalone Flappy Bird clone as a single HTML file with inline CSS and JavaScript. No frameworks, no dependencies. Just a playable game in one file.

## Files to Read First
(none — greenfield)

## Acceptance Criteria
- [ ] New file `browser/public/flappy.html` containing:
  - [ ] Canvas-based game rendering
  - [ ] Bird with gravity and flap (spacebar or tap)
  - [ ] Scrolling pipes with random gap positions
  - [ ] Collision detection (bird vs pipes, bird vs ground/ceiling)
  - [ ] Score counter (increments on each pipe passed)
  - [ ] Game over screen with final score and "tap to restart"
  - [ ] Mobile-friendly (touch events for flap)
  - [ ] Runs at 60fps on modern browsers
- [ ] Everything in ONE file — no external assets, no imports
- [ ] Game is playable and fun

## Constraints
- Single HTML file. No build step. No npm. No React.
- Inline everything — CSS in a style tag, JS in a script tag.
- Canvas API only — no DOM game elements.
- No file over 500 lines.
- Must work on mobile (touch to flap).

## Smoke Test
```bash
# File exists and is valid HTML
test -f browser/public/flappy.html && echo "EXISTS" || echo "MISSING"
# File is self-contained (no script src or link href to external resources)
grep -c 'src=' browser/public/flappy.html  # should be 0 or only data: URIs
grep -c 'href=' browser/public/flappy.html  # should be 0 or only internal
```
