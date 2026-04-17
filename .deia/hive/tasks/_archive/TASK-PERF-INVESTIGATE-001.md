# TASK-PERF-INVESTIGATE-001: Investigate Browser Performance Degradation on Set Load

## Role
Queen (Q33N) — Research only, no code changes

## Problem

When loading `shiftcenter.com/?set=code` (or any set via the `?set=` parameter), the browser becomes extremely slow and unresponsive. Killing the tab restores normal browser performance. This suggests the page is consuming excessive CPU, memory, or triggering runaway processes (infinite loops, excessive re-renders, unbounded polling, memory leaks, etc.).

## Your Job

Research the problem. Do NOT fix anything. Produce a diagnosis.

### 1. Trace the Set Loading Path

Start from the entry point and trace what happens when `?set=code` loads:

1. Read `browser/app.html` — the Vite entry point
2. Read `browser/src/App.tsx` — how does it read the `?set=` param?
3. Read `browser/src/shell/` — how does the shell initialize with a set?
4. Find and read the set resolver (likely in `eggResolver.ts` or similar)
5. Read `eggs/code.set.md` (or wherever set definitions live)
6. Trace what primitives/panes the set loads

### 2. Identify Potential Performance Killers

Look for these common causes:

**Infinite loops / unbounded recursion:**
- useEffect with missing or wrong dependency arrays
- State updates that trigger re-renders that trigger more state updates
- Event bus listeners that emit events that trigger more listeners

**Excessive polling:**
- setInterval or setTimeout loops
- WebSocket reconnection loops
- API polling without backoff

**Memory leaks:**
- Event listeners not cleaned up in useEffect returns
- Growing arrays/maps that never get pruned
- Large data structures held in closures

**Heavy rendering:**
- Components re-rendering on every tick
- Large lists without virtualization
- Canvas or animation frames running continuously

**Startup avalanche:**
- All panes loading simultaneously
- Multiple heavy API calls on mount
- Synchronous heavy computation blocking the main thread

### 3. Check the Bus System

The event bus (`relay_bus` or similar) is used heavily. Check:
- How many listeners register on set load?
- Are there circular event chains?
- Do bus events trigger re-renders?

### 4. Check Startup Manager

Read `browser/src/shell/startupManager.ts` (or wherever startup is orchestrated):
- What runs on startup?
- Is anything synchronous that shouldn't be?
- How many parallel initializations happen?

### 5. Check Specific Primitives

The `code` set likely loads several primitives. For each:
- Does it have expensive mount logic?
- Does it poll or subscribe to streams?
- Does it have animation loops?

### 6. Check for Known Performance Patterns

Look for:
- `console.log` in hot paths (surprisingly expensive at scale)
- JSON.stringify/parse of large objects on every render
- Deep object comparisons in useEffect deps
- Unthrottled window resize/scroll handlers

## Response

Write to `.deia/hive/responses/20260408-PERF-INVESTIGATE-001-RESPONSE.md`:

1. **Loading trace** — step by step what happens when `?set=code` loads
2. **Suspect list** — ranked by likelihood, with file paths and line numbers
3. **Evidence** — specific code patterns you found that are problematic
4. **Recommended fixes** — what to change, in priority order
5. **Quick wins** — anything that can be fixed in < 5 minutes

## Constraints
- Branch: main
- Do NOT modify any code
- Research only — read files, trace logic, document findings
- Focus on browser/src/ — the frontend is where the performance issue manifests
