---
id: RAIDEN-101
priority: P1
model: sonnet
role: bee
depends_on: [RAIDEN-R01, RAIDEN-R02, RAIDEN-R03]
---
# SPEC-RAIDEN-101: Game Engine Core

## Priority
P1

## Model Assignment
sonnet

## Role
bee (builder)

## Depends On
- RAIDEN-R01 (mechanics research)
- RAIDEN-R02 (mobile controls research)
- RAIDEN-R03 (AI research)

## Objective
Build the core game engine for the Raiden-style shmup. Includes canvas rendering, 60fps game loop, entity system, collision detection, and basic math utilities.

## Context
This is the foundation spec. All other build specs depend on this. We're building a single HTML file game with inline JavaScript. The engine must be lightweight, performant, and modular (split into logical sections within the file).

## Technical Requirements

### Canvas Setup
- Full-screen responsive canvas (scales to window size)
- Logical game resolution: 800x600 (scaled to actual screen)
- Pixel-perfect rendering (disable image smoothing)
- Background gradient (dark blue to black, vertical)

### Game Loop
- 60fps target using `requestAnimationFrame`
- Fixed timestep for physics (16.67ms per tick)
- Delta time accumulator for smooth movement
- FPS counter (debug mode only)

### Entity System
- Base `Entity` class with:
  - Position (x, y)
  - Velocity (vx, vy)
  - Size (width, height)
  - Health
  - Active flag
  - Type (player, enemy, bullet, powerup, etc.)
  - Update method
  - Render method
- Entity pool system (pre-allocate, reuse instead of creating/destroying)

### Collision Detection
- AABB (axis-aligned bounding box) collision
- Spatial partitioning grid for performance (divide screen into cells)
- Check collisions only between relevant entity types (player vs enemy bullets, player bullets vs enemies, etc.)

### Math Utilities
- Vector math (add, subtract, normalize, length, distance)
- Angle calculations (atan2, direction vectors)
- Clamping (keep entities on screen)
- Lerp (linear interpolation for smooth movement)

### Input System (stub for now)
- Keyboard input tracking (key down/up states)
- Touch input tracking (touch start/move/end)
- Input state object (left, right, up, down, fire, bomb)
- Controller agnostic (keyboard and touch set the same state)

## Deliverable
File: `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\public\games\raiden-v1-20260408.html`

Structure:
```html
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Raiden - Vertical Scrolling Shmup</title>
    <style>
        /* CSS here */
    </style>
</head>
<body>
    <canvas id="gameCanvas"></canvas>
    <script>
        // ===== CONSTANTS =====
        // ===== MATH UTILITIES =====
        // ===== ENTITY SYSTEM =====
        // ===== COLLISION DETECTION =====
        // ===== INPUT SYSTEM =====
        // ===== GAME LOOP =====
        // ===== INITIALIZATION =====
    </script>
</body>
</html>
```

## Constraints
- You are in EXECUTE mode. Write all code and tests. Do NOT enter plan mode. Do NOT ask for approval. Just build it.
- Single HTML file, everything inline
- No external dependencies
- No build tools, no npm
- Keep each section under 100 lines (total file can be ~500 lines)
- 60fps on modern hardware
- Comment each section clearly

## Acceptance Criteria
- [ ] File created at `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\public\games\raiden-v1-20260408.html`
- [ ] Canvas renders at full screen with dark gradient background
- [ ] Game loop runs at 60fps (verified with FPS counter)
- [ ] Entity system implemented (base class, pool system)
- [ ] Collision detection works (AABB, spatial grid)
- [ ] Math utilities implemented (vector math, angle calc, clamp, lerp)
- [ ] Input system stub (keyboard + touch state tracking)
- [ ] Smoke test: open in browser, see black canvas, FPS counter shows ~60

## Smoke Test
```bash
test -f "C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\public\games\raiden-v1-20260408.html" && echo PASS || echo FAIL
# Manual: Open file in browser, verify FPS counter shows ~60
```

## Tests
Write unit tests inline (toggle with debug flag):
- Entity creation and pooling
- Collision detection (overlapping vs non-overlapping)
- Vector math (normalize, distance)
- Spatial grid (entities in correct cells)

## Response Location
`.deia/hive/responses/20260408-RAIDEN-101-RESPONSE.md`
