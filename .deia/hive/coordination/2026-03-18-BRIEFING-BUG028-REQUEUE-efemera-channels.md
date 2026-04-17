# BRIEFING: BUG-028 RE-QUEUE — Efemera Channels Click Handler

**From:** Q33NR
**To:** Q33N
**Date:** 2026-03-18
**Priority:** P0
**Model Assignment:** sonnet

---

## Background

Q88N has re-queued BUG-028 with this directive:

> "Previous bee claimed 6/7 tests passing but channelsAdapter.ts has zero references to `channel:selected` event. The click handler was never wired. Backend routes exist at /efemera/ and work. This is a frontend wiring issue."

## Current Architecture (Verified)

I've read the codebase. Here's what exists:

**1. channelsAdapter.ts** (data adapter)
- Loads channel data from `/efemera/channels` API
- Groups channels into Pinned/Channels/DMs
- Returns TreeNodeData[] with channel metadata in `node.meta`
- **Does NOT handle clicks or emit bus events** (it's a data loader)

**2. treeBrowserAdapter.tsx** (UI component)
- Renders the tree-browser UI for ANY adapter (channels, filesystem, members, etc.)
- Lines 173-187: When `adapter === 'channels'` and user clicks a channel node:
  - Extracts channelId, channelName, type from `node.meta`
  - Emits `channel:selected` bus event with `target: '*'`
- This is the SAME pattern used for filesystem adapter (`file:selected`)

**3. Previous bee response (20260317-BUG-028-RESPONSE.md)**
- Created 8 integration tests
- 6/7 tests passing (86% pass rate)
- Concluded: "Feature is already implemented"
- Reason: The click → bus event → message load flow works via treeBrowserAdapter

## Architectural Question

**Is the current architecture correct?**

Current pattern: Data adapters (channelsAdapter, filesystemAdapter) load data → treeBrowserAdapter handles clicks → emits adapter-specific bus events

Alternative pattern: Each data adapter also handles its own click events

**Implications:**
- Current pattern: Centralized click handling, consistent across all adapters
- Alternative pattern: Each adapter controls its own events, but duplicates click logic

## Q88N's Directive Interpretation

Two possible meanings:

**A. Architectural misunderstanding**
Q88N expected channelsAdapter to handle clicks, but the actual architecture delegates this to treeBrowserAdapter. If so, the spec is based on incorrect expectations, and the feature already works.

**B. Intentional architecture change**
Q88N wants to CHANGE the architecture so data adapters handle their own clicks. This would require refactoring treeBrowserAdapter and all other adapters.

## Your Task

**You must determine which interpretation is correct:**

1. **Read the spec** (included in your prompt)
2. **Read the codebase files** listed below
3. **Review the previous bee response** (20260317-BUG-028-RESPONSE.md)
4. **Determine if there's an actual bug or an architectural misunderstanding**

If there's a bug: Write task files to fix it.

If it's a misunderstanding: Write a clarification report back to me (Q33NR) explaining the architecture and recommending the spec be updated or closed.

**DO NOT dispatch bees until you return to me with your assessment.**

## Files to Read

1. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\tree-browser\adapters\channelsAdapter.ts`
2. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\treeBrowserAdapter.tsx` (focus on lines 170-187)
3. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\eggs\efemera.egg.md`
4. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260317-BUG-028-RESPONSE.md`
5. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\text-pane\SDEditor.tsx` (channel:selected handler around line 356-386)
6. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\terminal\useTerminal.ts` (channel:selected handler around line 176-186)

## Acceptance Criteria

**Return to Q33NR with one of these outcomes:**

**Option 1: Bug Confirmed**
- [ ] Clear explanation of what's broken
- [ ] Task files written to fix the issue
- [ ] Wait for Q33NR approval before dispatching

**Option 2: Architecture Clarification**
- [ ] Explanation of current architecture
- [ ] Evidence that feature works (test results, code flow)
- [ ] Recommendation to Q33NR: close spec or update spec understanding

**Option 3: Architecture Change Required**
- [ ] Explanation of proposed architecture change
- [ ] Task files to refactor treeBrowserAdapter + all adapters
- [ ] Wait for Q33NR approval before dispatching

## Constraints

- No file over 500 lines
- CSS: var(--sd-*) only
- TDD: tests first
- No stubs
- All file paths absolute

---

**Q33N: Read the code, assess the situation, and return to me with your findings. Do NOT dispatch yet.**
