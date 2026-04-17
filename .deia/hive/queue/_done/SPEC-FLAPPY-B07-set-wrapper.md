---
id: FLAPPY-B07
priority: P2
model: sonnet
role: bee
depends_on: [FLAPPY-B06]
---
# SPEC-FLAPPY-B07: Flappy Bird Set Wrapper

## Priority
P2

## Model Assignment
sonnet

## Role
bee

## Depends On
- FLAPPY-B06 (final integrated game HTML)

## Objective
Create a `flappy` set so the Flappy Bird AI v2 game is accessible from the website at `?egg=flappy`. The set should be a simple full-screen iframe wrapper embedding the game HTML. Must work on mobile.

## Context
The game lives at `browser/public/games/flappy-bird-ai-v2-20260407.html` and is already mobile-responsive. We need:

1. A minimal `IframePane` React component (new appType) that renders any URL in a full-screen iframe
2. A `flappy.set.md` set file that uses this component to embed the game

The `IframePane` component should be reusable for future games/embeds — it takes a `src` URL from config.

## You are in EXECUTE mode
**Write all code and tests. Do NOT enter plan mode. Do NOT ask for approval. Just build it.**

## Files to Read First
browser/sets/hodeia.set.md
browser/src/apps/hodeia-landing/HodeiaLanding.tsx
browser/src/shell/components/PaneContent.tsx

## Deliverables

### 1. IframePane Component
- [ ] Create `browser/src/apps/iframe-pane/IframePane.tsx`
- [ ] Props: receives `config.src` (URL string) from set layout
- [ ] Renders a full-viewport `<iframe>` with `width: 100%`, `height: 100%`, `border: none`
- [ ] Sets `allow="autoplay"` for Web Audio API sound effects
- [ ] No scroll bars on the wrapper (the game handles its own scroll)

### 2. Register appType
- [ ] Register `iframe-pane` as an appType in the app registry (follow the pattern of existing app registrations like `hodeia-landing`)
- [ ] Lazy-load the component

### 3. Flappy Set File
- [ ] Create `browser/sets/flappy.set.md`
- [ ] Frontmatter: `egg: flappy`, `displayName: Flappy Bird AI`, `auth: public`, `defaultRoute: /flappy`
- [ ] Layout: single pane, `appType: iframe-pane`, config `src: /games/flappy-bird-ai-v2-20260407.html`
- [ ] No top-bar, no menu-bar, no chrome — just the game full-screen
- [ ] UI chromeMode: hidden

### 4. Verify Mobile
- [ ] Set loads at `?egg=flappy`
- [ ] Game fills the viewport on mobile (no extra padding/margins from shell)
- [ ] Touch controls work through the iframe
- [ ] No double scroll bars

## Test Requirements
- [ ] `?egg=flappy` loads the game in the shell
- [ ] Game is playable (birds spawn, AI evolves)
- [ ] Mobile viewport: game fills screen, touch works
- [ ] IframePane renders with correct src from config

## Constraints
- IframePane component should be under 30 lines
- Set file should be minimal (under 50 lines)
- No hardcoded game URL in the component — read from `config.src`
- Auth: public (no login required)

## Acceptance Criteria
- [ ] `browser/src/apps/iframe-pane/IframePane.tsx` exists and is under 30 lines
- [ ] `iframe-pane` appType is registered and lazy-loaded
- [ ] `browser/sets/flappy.set.md` exists with `egg: flappy`, `auth: public`
- [ ] `?egg=flappy` loads the Flappy Bird AI v2 game full-screen
- [ ] Game is playable through the iframe (AI mode + human mode)
- [ ] Mobile: game fills viewport, touch controls work, no double scrollbars
- [ ] Response file at `.deia/hive/responses/20260414-FLAPPY-B07-RESPONSE.md`

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `.deia/hive/responses/20260414-FLAPPY-B07-RESPONSE.md`

The response MUST contain these 8 sections:
1. **Header** — task ID, title, status (COMPLETE/FAILED), model, date
2. **Files Modified** — every file created/modified/deleted, full paths
3. **What Was Done** — bullet list of concrete changes
4. **Test Results** — manual test observations
5. **Build Verification** — does `?egg=flappy` load the game?
6. **Acceptance Criteria** — copy from task, mark [x] or [ ]
7. **Clock / Cost / Carbon** — all three, never omit any
8. **Issues / Follow-ups** — edge cases, dependencies, next tasks

DO NOT skip any section.

## Output Location
browser/src/apps/iframe-pane/IframePane.tsx
browser/sets/flappy.set.md
.deia/hive/responses/20260414-FLAPPY-B07-RESPONSE.md

## Smoke Test
- [ ] `test -f browser/src/apps/iframe-pane/IframePane.tsx` passes
- [ ] `test -f browser/sets/flappy.set.md` passes
- [ ] `test -f .deia/hive/responses/20260414-FLAPPY-B07-RESPONSE.md` passes
