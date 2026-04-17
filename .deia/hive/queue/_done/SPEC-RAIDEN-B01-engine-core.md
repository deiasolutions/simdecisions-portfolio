---
id: RAIDEN-B01
priority: P1
model: sonnet
role: bee
depends_on: [RAIDEN-D01]
---
# SPEC-RAIDEN-B01: Game Engine Core

## Priority
P1

## Model Assignment
sonnet

## Role
bee (b33 — you write code and tests)

## Depends On
- RAIDEN-D01 (game design document)

## Objective
Build the foundational game engine: canvas rendering, game loop, entity system, and collision detection.

## You are in EXECUTE mode
Write all code and tests. Do NOT enter plan mode. Do NOT ask for approval. Just build it.

## Design Reference
Read: `.deia/hive/responses/20260413-RAIDEN-D01-GAME-DESIGN-DOC.md`

## Deliverables

### File: `C:\Users\davee\OneDrive\Documents\GitHub\simdecisions\browser\public\games\raiden-v1-20260413.html`

**Implement:**

1. **Canvas Setup**
   - Create 800x600 canvas, scale to viewport
   - Handle window resize (maintain aspect ratio)
   - Double buffering for smooth rendering

2. **Game Loop**
   - RequestAnimationFrame loop
   - 60fps target
   - Delta time calculation for consistent physics
   - Pause/resume functionality

3. **Entity System**
   - Base Entity class: `{id, x, y, vx, vy, width, height, type, active}`
   - Entity pools for reuse (prevent garbage collection lag)
   - Update and render methods
   - Entity types: PLAYER, ENEMY, BULLET_PLAYER, BULLET_ENEMY, POWERUP, PARTICLE

4. **Collision Detection**
   - AABB (Axis-Aligned Bounding Box) collision
   - Spatial hashing for performance (grid-based partitioning)
   - Collision pairs: player vs enemy bullets, player bullets vs enemies, player vs power-ups
   - Efficient broad-phase (skip distant objects)

5. **Rendering System**
   - Clear canvas each frame
   - Draw entities with CSS colors (use `var(--sd-*)` fallback for HTML context)
   - Glow effects using multiple draw passes
   - FPS counter (debug mode, toggle with F key)

6. **Game States**
   - MENU, PLAYING, PAUSED, GAME_OVER, LEVEL_COMPLETE
   - State machine with enter/exit handlers
   - State-specific rendering and update logic

## Technical Constraints
- Single HTML file, all code inline
- No external libraries (no Three.js, no Phaser, vanilla JS only)
- CSS colors: Since we're in Canvas 2D context, use hex fallbacks for `var(--sd-*)` colors
  - Primary: `#3b82f6` (blue)
  - Danger: `#ef4444` (red)
  - Accent: `#06b6d4` (cyan)
  - Warning: `#f59e0b` (orange)
  - Success: `#10b981` (green)
- Performance: Handle 200 entities at 60fps

## Acceptance Criteria
- [ ] Canvas renders at 800x600, scales to viewport
- [ ] Game loop runs at 60fps (or as close as possible)
- [ ] Entity system supports create, update, render, destroy
- [ ] Collision detection works for AABB overlaps
- [ ] Can toggle between game states (MENU, PLAYING, PAUSED)
- [ ] FPS counter displays when F key pressed
- [ ] No errors in console
- [ ] File under 500 lines (core engine only, game logic comes later)

## Tests (Manual Smoke Tests)
Since this is a single HTML file, tests are manual:

1. **Canvas Test:** Open file, see 800x600 black canvas
2. **Resize Test:** Resize browser window, canvas scales correctly
3. **FPS Test:** Press F, see FPS counter in corner
4. **Entity Test:** Create 100 test entities (circles), they render at 60fps
5. **Collision Test:** Create 2 overlapping entities, collision detected and logged

**Embed test entities in code (behind a TEST_MODE flag):**
```javascript
const TEST_MODE = true; // Set to false when engine complete

if (TEST_MODE) {
  // Create 100 random entities
  for (let i = 0; i < 100; i++) {
    entities.push({
      x: Math.random() * 800,
      y: Math.random() * 600,
      vx: Math.random() * 2 - 1,
      vy: Math.random() * 2 - 1,
      width: 10,
      height: 10,
      type: 'TEST',
      active: true
    });
  }
}
```

## Smoke Test
```bash
test -f "browser/public/games/raiden-v1-20260413.html" && \
grep -q "requestAnimationFrame" "browser/public/games/raiden-v1-20260413.html" && \
grep -q "collision" "browser/public/games/raiden-v1-20260413.html" && \
echo "PASS"
```

## Response Location
`.deia/hive/responses/20260413-RAIDEN-B01-ENGINE-CORE-RESPONSE.md`

## Notes
- This is the foundation. Keep it clean and well-commented.
- Later specs will build on this engine (player, enemies, weapons, AI).
- Use `const`, `let`, modern ES6+ syntax (arrow functions, template literals).
- No jQuery, no frameworks. Pure vanilla JavaScript.
