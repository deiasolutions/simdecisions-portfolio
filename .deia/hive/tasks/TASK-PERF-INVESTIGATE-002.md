# TASK-PERF-INVESTIGATE-002: Deep Trace of Browser Performance Issue on Set Load

## Role
Queen (Q33N) — Research only, no code changes

## Problem

When loading `localhost:5173/?set=code` (or any set), the browser becomes extremely slow and unresponsive. Killing the tab restores performance.

## CRITICAL INSTRUCTION

Do NOT jump to conclusions. A previous investigation assumed ResizeObservers were the cause without verifying. That was wrong — it was a guess based on pattern-matching, not evidence.

Your job is to TRACE, not guess. For every suspect you find:
1. Trace the full execution path — what calls what, what triggers what
2. Determine if it actually runs in a loop or just once
3. Count how many times it would fire during a page load
4. Estimate the actual CPU cost (a single RAF callback is nothing; 10,000 per second is a problem)
5. Check if there are guards, early exits, or throttles already in place that the previous investigation missed

**If something looks suspicious but you can't prove it causes continuous CPU usage, say so. Don't list it as a cause.**

## Investigation Method

### Phase 1: Trace the Full Load Path

Start from `browser/src/main.tsx` and trace EVERY step of what happens when `?set=code` loads. For each step:
- What function runs?
- Is it sync or async?
- Does it trigger re-renders?
- Does it set up any recurring work (intervals, observers, listeners, polling)?
- Does it fire once and stop, or does it keep running?

Read every file in the chain. Don't skip anything.

### Phase 2: Find All Recurring Work

Search the entire `browser/src/` for things that run continuously:
- `setInterval` — what's the interval? What does the callback do? Does it ever clear?
- `setTimeout` that calls itself (recursive timeout)
- `ResizeObserver` — does the callback dispatch state changes that trigger re-layout?
- `MutationObserver` — same question
- `requestAnimationFrame` loops — does it re-queue itself?
- `addEventListener('resize'|'scroll'|'mousemove')` — unthrottled?
- WebSocket `onmessage` handlers — do they trigger re-renders?
- `useEffect` with no deps or wrong deps — does it re-run on every render?
- Event bus subscriptions — do any create circular chains (A emits → B handles → B emits → A handles)?

For each one you find, trace whether it's active during a set load and whether it could cause continuous CPU usage.

### Phase 3: Find All Render Cascades

Look for patterns where a render triggers another render:
- State update in useEffect that depends on its own state
- Redux dispatch in a component that subscribes to the dispatched state
- Bus event that triggers a state update that emits another bus event
- ResizeObserver that dispatches → re-render → layout change → observer fires again

For each potential cascade, trace it to see if there's a termination condition or if it actually loops forever.

### Phase 4: Check What's Different About Set Load vs No Set

Compare what happens on:
- `localhost:5173/` (no set, landing page) — presumably fast
- `localhost:5173/?set=code` — slow

What additional code runs when a set is loaded? The problem is in the delta.

### Phase 5: Check Specific Primitives

The `code` set loads specific primitives. Read `browser/sets/code.set.md` to see what they are, then check each primitive's mount code:
- Does it start polling?
- Does it load heavy resources (Monaco editor, large bundles)?
- Does it have animation loops?
- Does it make network requests that could hang or retry infinitely?

### Phase 6: Memory and Network

Look for:
- Fetch calls without timeout/abort that could pile up
- Growing data structures (arrays, maps) that never get pruned
- Event listeners that register on mount but don't unregister on unmount
- Closures holding references to large objects

## Output Requirements

For each finding, categorize as:

**CONFIRMED CAUSE** — You traced the full path and can prove it causes continuous CPU/memory usage during set load. Show the exact chain of execution.

**LIKELY CAUSE** — Strong evidence but can't fully trace without runtime profiling. Explain what you'd need to verify.

**SUSPICIOUS BUT UNVERIFIED** — Looks bad in code but you couldn't prove it actually runs during set load or causes problems. Explain why you're uncertain.

**RULED OUT** — You investigated it and determined it's NOT a cause. Explain why (has guards, only runs once, etc.).

## Response

Write to `.deia/hive/responses/20260408-PERF-INVESTIGATE-002-RESPONSE.md`

Structure:
1. Full load trace (step by step)
2. Confirmed causes (with execution chain proof)
3. Likely causes (with evidence and gaps)
4. Suspicious but unverified
5. Ruled out (and why)
6. What a Chrome DevTools profile would need to confirm

## Constraints
- Branch: main
- Do NOT modify any code
- Do NOT guess — trace
- If you can't determine something from code alone, say so explicitly
