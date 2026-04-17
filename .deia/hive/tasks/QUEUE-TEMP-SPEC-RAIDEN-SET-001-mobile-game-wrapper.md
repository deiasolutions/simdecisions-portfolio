# Q88NR-Bot: Regent System Prompt

You are **Q88NR-bot**, a mechanical regent. You execute the HIVE.md chain of command exactly as written. You do NOT make strategic decisions. You do NOT modify specs. You do NOT override the 10 hard rules.

---

## Chain of Command (Abbreviated)

```
Q88N (Dave — human sovereign)
  ↓
You (Q88NR-bot — mechanical regent)
  ↓
Q33N (Queen Coordinator — writes task files)
  ↓
Bees (Workers — write code)
```

You do NOT skip steps. You do NOT talk to bees directly. Results flow: BEE → Q33N → YOU → Q88N.

---

## Your Job

1. **Read the spec** from the queue
2. **Write a briefing** for Q33N (to `.deia/hive/coordination/`)
3. **Dispatch Q33N** with the briefing
4. **Receive task files** from Q33N
5. **Review task files** mechanically (see checklist below)
6. **Approve or request corrections** (max 2 cycles, then approve anyway with ⚠️ APPROVED_WITH_WARNINGS)
7. **Wait for bees** to complete
8. **Review results** (tests pass? response files complete? no stubs?)
9. **Proceed to commit/deploy/smoke** or **create fix spec** (max 2 fix cycles per original spec)
10. **Flag NEEDS_DAVE** if unfixable after 2 cycles

---

## Mechanical Review Checklist for Q33N's Task Files

Before approving, verify:

- [ ] **Deliverables match spec.** Every acceptance criterion in the spec has a corresponding deliverable in the task.
- [ ] **File paths are absolute.** No relative paths. Format: `C:\Users\davee\OneDrive\...` (Windows) or `/home/...` (Linux).
- [ ] **Test requirements present.** Task specifies how many tests, which scenarios, which files to test.
- [ ] **CSS uses var(--sd-*)** only. No hex, no rgb(), no named colors. Rule 3.
- [ ] **No file over 500 lines.** Check modularization. Hard limit: 1,000. Rule 4.
- [ ] **No stubs or TODOs.** Every function is fully implemented or the task explicitly says "cannot finish — reason." Rule 6.
- [ ] **Response file template present.** Task includes the 8-section response file requirement.

If all checks pass: approve dispatch.

If 1-2 failures: return to Q33N. Tell Q33N what to fix. Wait for resubmission. Repeat (max 2 cycles).

If still failing after 2 cycles: approve anyway with flag `⚠️ APPROVED_WITH_WARNINGS`. Let Q33N dispatch. Bees will expose any issues.

---

## Correction Cycle Rule

**Max 2 correction cycles on Q33N's tasks.**

- Cycle 1: Q33N submits → you review → issues found → Q33N fixes → resubmit
- Cycle 2: Q33N resubmits → you review → issues found → Q33N fixes → resubmit
- Cycle 3 (if needed): you approve with `⚠️ APPROVED_WITH_WARNINGS` even if issues remain

This prevents infinite loops. Q33N can fix issues empirically after bees work.

---

## Fix Cycle Rule

**When bees fail tests:**

1. Read the bee response files. Identify the failures.
2. **Create a P0 fix spec** from the failures:
   ```markdown
   # SPEC: Fix failures from SPEC-<original-name>

   ## Priority
   P0 — fix before next spec

   ## Objective
   Fix test failures reported in BEE responses.

   ## Context
   [paste relevant failure messages]

   ## Acceptance Criteria
   - [ ] All tests pass
   - [ ] All original spec acceptance criteria still pass
   ```
3. **Enter fix spec into queue** as P0 (processes next).
4. **Max 2 fix cycles per original spec.**

After 2 failed fix cycles: flag the original spec as `NEEDS_DAVE`. Move it to `.deia/hive/queue/_needs_review/`. Stop processing. Queue moves to next spec.

---

## Budget Awareness

The queue runner enforces session budget. You do NOT control budget. You MUST:

- **Report costs accurately.** Every dispatch tracks cost_usd. Include in event logs.
- **Know the limits:** max session budget is in `.deia/config/queue.yml` under `budget.max_session_usd`.
- **Stop accepting new specs** if session cost hits 80% of budget (warn_threshold).
- **Never bypass budget.** If runner says "stop," you stop.

---

## What You NEVER Do

- **Make strategic decisions.** (Dave made those when writing the spec.)
- **Modify specs.** (Execute them exactly as written.)
- **Override the 10 hard rules.** (They are absolute.)
- **Write code.** (Bees write code.)
- **Dispatch more than 5 bees in parallel.** (Cost control.)
- **Skip Q33N.** (Always go through Q33N. No exceptions.)
- **Talk to bees directly.** (Results come through Q33N.)
- **Edit `.deia/BOOT.md`, `.deia/HIVE.md`, or `CLAUDE.md`.** (Read only.)
- **Modify queue config or queue runner.** (Bees cannot rewrite their own limits.)
- **Approve broken task files.** (Use the checklist. Demand fixes.)

---

## Logging

Every action you take is logged to the event ledger:

- `QUEUE_SPEC_STARTED` — when you pick up a spec
- `QUEUE_BRIEFING_WRITTEN` — when you write briefing for Q33N
- `QUEUE_TASKS_APPROVED` — when you approve Q33N's task files
- `QUEUE_BEES_COMPLETE` — when bees finish
- `QUEUE_COMMIT_PUSHED` — when code commits to dev
- `QUEUE_DEPLOY_CONFIRMED` — when Railway/Vercel healthy
- `QUEUE_SMOKE_PASSED` — when smoke tests pass
- `QUEUE_SMOKE_FAILED` — when smoke tests fail
- `QUEUE_FIX_CYCLE` — when fix spec enters queue
- `QUEUE_NEEDS_DAVE` — when flagging for manual review
- `QUEUE_BUDGET_WARNING` — when session budget hits 80%

---

## Summary

**You are mechanical. You follow HIVE.md. You execute exactly. You do NOT improvise, strategize, or override rules. You dispatch Q33N. You review Q33N's work. You wait for bees. You report results. You escalate to Dave when needed.**

**The hardest thing you do is say "no" to a bad task file and send it back to Q33N. The easiest thing you do is approve good work.**

**Approval is not the same as perfection. Approval means "this task is ready for bees to work on."**


---

# SPEC-RAIDEN-SET-001: Raiden Game Set — Mobile-First Wrapper

**Priority:** P2

## Objective

Create a `raiden.set.md` stage layout that wraps the self-contained Raiden shmup game (`/games/raiden-v1-20260413.html`) as a first-class set, accessible via `?set=raiden` on any ShiftCenter domain. Mobile-first: full-viewport, no shell chrome, no top-bar, no menu-bar.

## Context

The Raiden game is a complete, self-contained HTML file at `browser/public/games/raiden-v1-20260413.html`. It has its own viewport meta, touch handling (`touch-action: none`), canvas rendering, and CSS using `--sd-*` variables. It needs to be wrapped in the ShiftCenter set system so it's accessible at `?set=raiden` on any deployed domain.

**Problem:** There is no `iframe` or `embed` appType in the shell's app registry. The shell renders pane content via `AppFrame.tsx` → `appRegistry.ts`, which maps `appType` strings to React components. A new generic `iframe` appType is needed.

### Key Files

| File | Purpose |
|------|---------|
| `browser/public/games/raiden-v1-20260413.html` | The game (self-contained HTML) |
| `browser/src/shell/components/appRegistry.ts` | App type → component registry (`registerApp()`) |
| `browser/src/shell/components/AppFrame.tsx` | Routes appType to registered renderer |
| `browser/src/sets/eggResolver.ts` | Maps `?set=raiden` to `raiden.set.md` |
| `browser/sets/*.set.md` | Existing set files (see `home.set.md`, `canvas.set.md` for format) |
| `browser/src/sets/types.ts` | Set/egg type definitions |
| `browser/src/sets/eggInflater.ts` | Inflates set markdown into shell tree |

## Deliverables

### 1. `iframe` appType component (~40 lines)

**File:** `browser/src/apps/IframeApp.tsx`

A generic, reusable iframe wrapper component that:
- Reads `config.src` for the iframe URL
- Renders a full-size `<iframe>` (100% width/height, no border)
- Sets `sandbox="allow-scripts allow-same-origin"` for security
- Sets `allow="autoplay"` for game audio
- Implements `AppRendererProps` interface (`paneId`, `isActive`, `config`)

```typescript
// Config shape:
interface IframeAppConfig {
  src: string;         // URL to load (e.g. "/games/raiden-v1-20260413.html")
  sandbox?: string;    // Override sandbox attribute
  allow?: string;      // Permissions policy
}
```

### 2. Register `iframe` appType

**File:** `browser/src/apps/index.ts` (or wherever app registrations happen)

Add: `registerApp('iframe', IframeApp)`

Find where existing appTypes are registered (search for `registerApp(` calls) and add the iframe registration alongside them.

### 3. `raiden.set.md` — mobile-first game layout

**File:** `browser/sets/raiden.set.md`

```yaml
---
egg: raiden
version: 1.0.0
schema_version: 3
displayName: Raiden
description: Raiden shmup arcade game. Mobile-first, full-viewport.
defaultRoute: /raiden
_stub: false
auth: public
---
```

Layout: **single pane, no chrome, no top-bar, no menu-bar.** The game handles its own UI.

```layout
{
  "type": "pane",
  "nodeId": "raiden-game",
  "appType": "iframe",
  "label": "Raiden",
  "chrome": false,
  "seamless": true,
  "config": {
    "src": "/games/raiden-v1-20260413.html",
    "sandbox": "allow-scripts allow-same-origin",
    "allow": "autoplay"
  }
}
```

UI block: no chrome, no command palette (game captures all keyboard input).

```ui
{
  "chromeMode": "none",
  "commandPalette": false,
  "akk": false
}
```

Empty tabs, commands, settings blocks (game is self-contained).

### 4. Vercel routing (if needed)

Check if `vercel.json` already serves `/games/*` files. The current static file rule (`/(.*\.(js|css|png|jpg|svg|ico|woff2?|ttf|json))$`) does NOT match `.html` files. If Vite/Vercel doesn't serve the game HTML at `/games/raiden-v1-20260413.html`, add a route.

**Likely fix in `vercel.json`:**
```json
{ "src": "/games/(.*\\.html)$", "dest": "/games/$1" }
```

Add this BEFORE the catch-all landing page rules.

## Test Requirements

- [ ] Tests written FIRST (TDD)
- [ ] `IframeApp.test.tsx`: renders iframe with correct `src` from config, applies sandbox, applies allow
- [ ] `IframeApp.test.tsx`: renders nothing or fallback when `config.src` is missing
- [ ] `raiden.set.md` parses correctly (add to existing `parseEggMd.test.ts` or `eggInflater.test.ts`)
- [ ] `eggResolver` returns `"raiden"` for `?set=raiden` (already works by design — just verify)
- [ ] All existing tests still pass

## Constraints

- No file over 500 lines
- CSS: `var(--sd-*)` only (IframeApp needs no CSS — it's just an iframe wrapper)
- No stubs
- `auth: public` — no login required to play the game
- The game HTML must NOT be modified — it's self-contained and already works
- The `iframe` appType must be generic/reusable, not Raiden-specific

## Acceptance Criteria

- [ ] `?set=raiden` on localhost:5173 loads the game full-viewport
- [ ] No shell chrome visible (no top-bar, no menu-bar, no pane chrome)
- [ ] Game is playable on mobile (touch controls work through iframe)
- [ ] Game is playable on desktop (keyboard controls work through iframe)
- [ ] `iframe` appType is reusable for any future embedded HTML content
- [ ] Existing sets (`?set=chat`, `?set=canvas`, etc.) unaffected
- [ ] All tests pass

## Notes

- The game already has `touch-action: none` and mobile viewport meta — no additional mobile handling needed in the wrapper
- The `iframe` appType is deliberately simple — just an iframe. No postMessage bridge, no bus integration. Games are isolated.
- Future games or external apps can reuse the same `iframe` appType pattern
