# TASK-PERF-FIX-001: Fix ResizeObserver Re-render Storm and Unthrottled Resize Listeners

## Role
Bee — EXECUTE mode

## You are in EXECUTE mode. Write all code. Do NOT enter plan mode. Do NOT ask for approval. Just build it.

## Problem

Loading `?set=code` freezes the browser. Root cause: ResizeObserver infinite re-render loop + unthrottled resize listeners creating layout thrashing.

## Files to Read First

1. `browser/src/shell/components/ShellNodeRenderer.tsx` — lines 119-165 (ResizeObservers)
2. `browser/src/shell/components/Shell.tsx` — lines 142-153 (chrome resize), lines 200-239 (slideover resize)
3. `browser/src/infrastructure/relay_bus/messageBus.ts` — line 219 (LOG_EVENT dispatch)
4. `browser/src/primitives/PaneLoader.tsx` — lines 14-19 (spinner interval)

## Fixes Required

### Fix 1: Debounce ResizeObservers in ShellNodeRenderer.tsx (CRITICAL)

Both ResizeObservers (lines 119-136 and lines 139-165) need:
1. Wrap callback in `requestAnimationFrame` to batch with next frame
2. Add early exit if dimensions haven't changed (compare prev vs current)
3. Cancel pending RAF on cleanup

Pattern:
```tsx
useEffect(() => {
  if (node.type !== 'app' || !ref.current) return;
  let rafId: number | null = null;
  let prevWidth = 0;
  let prevHeight = 0;

  const observer = new ResizeObserver(() => {
    if (rafId !== null) return; // Already queued
    rafId = requestAnimationFrame(() => {
      rafId = null;
      if (!ref.current) return;
      const rect = ref.current.getBoundingClientRect();
      // Early exit if no meaningful change
      if (Math.abs(rect.width - prevWidth) < 1 && Math.abs(rect.height - prevHeight) < 1) return;
      prevWidth = rect.width;
      prevHeight = rect.height;
      // ... dispatch the update
    });
  });

  observer.observe(ref.current);
  return () => {
    observer.disconnect();
    if (rafId !== null) cancelAnimationFrame(rafId);
  };
}, [/* deps */]);
```

Apply this pattern to BOTH ResizeObservers in the file.

### Fix 2: Throttle Window Resize Listeners in Shell.tsx (CRITICAL)

Both resize listeners need throttling. Do NOT add lodash — write a simple inline throttle.

For the chrome mode listener (lines 142-153):
```tsx
useEffect(() => {
  if (state.chromeMode !== 'auto') return;
  let rafId: number | null = null;
  const handleResize = () => {
    if (rafId !== null) return;
    rafId = requestAnimationFrame(() => {
      rafId = null;
      dispatch({ type: 'SET_CHROME_MODE', mode: 'auto' });
    });
  };
  window.addEventListener('resize', handleResize);
  return () => {
    window.removeEventListener('resize', handleResize);
    if (rafId !== null) cancelAnimationFrame(rafId);
  };
}, [state.chromeMode, dispatch]);
```

For the slideover auto-undock listener (lines 200-239): same RAF pattern, plus memoize the tree scan result.

### Fix 3: Disable LOG_EVENT During Startup in messageBus.ts

In the message dispatch function around line 219, guard the LOG_EVENT:
```tsx
// Skip LOG_EVENT during startup to avoid dispatch storm
if (this._startupComplete) {
  dispatch({ type: 'LOG_EVENT', ... });
}
```

Add a `_startupComplete` flag that flips to `true` after 2 seconds (setTimeout in constructor), or better: after a `shell:ready` bus event.

If that's too invasive, just wrap in `requestIdleCallback`:
```tsx
requestIdleCallback(() => {
  dispatch({ type: 'LOG_EVENT', ... });
});
```

### Fix 4: Replace PaneLoader Spinner Interval with CSS Animation

In `PaneLoader.tsx`, replace the `setInterval` state update with a pure CSS animation:
- Remove the `useState` and `useEffect` with setInterval
- Use CSS `@keyframes` for the spinner animation
- This eliminates 7 simultaneous JS intervals during load

## Constraints

- Do NOT add new dependencies (no lodash, no external throttle library)
- Use `requestAnimationFrame` for all throttling (it's built-in and frame-aligned)
- Do NOT change the visual appearance of anything — same layout, same behavior, just without the performance death spiral
- CSS convention: use `var(--sd-*)` tokens only, no hex/rgb
- Keep files under 500 lines
- Run `cd browser && npx tsc --noEmit` after changes to verify no type errors introduced

## Acceptance Criteria

1. ShellNodeRenderer.tsx ResizeObservers debounced with RAF + early exit
2. Shell.tsx resize listeners throttled with RAF
3. messageBus.ts LOG_EVENT guarded or deferred
4. PaneLoader.tsx spinner uses CSS animation instead of setInterval
5. TypeScript compiles without new errors
6. No visual changes to the UI

## Response

Write to `.deia/hive/responses/20260408-PERF-FIX-001-RESPONSE.md`
