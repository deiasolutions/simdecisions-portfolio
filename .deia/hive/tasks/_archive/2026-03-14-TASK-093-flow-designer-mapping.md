# TASK-093: Flow Designer Mapping to ShiftCenter

**Role:** BEE
**Model:** sonnet
**Priority:** P0
**Briefing:** 2026-03-14-BRIEFING-flow-designer-survey.md

## Objective

Read the key Flow Designer files in the platform repo and determine where each piece maps to in shiftcenter's architecture. Identify overlaps with existing code.

## Source Directory

`C:\Users\davee\OneDrive\Documents\GitHub\platform\efemera\frontend\src\`

If this path doesn't exist, search these alternatives:
- `C:\Users\davee\OneDrive\Documents\GitHub\platform\efemera\frontend\`
- `C:\Users\davee\OneDrive\Documents\GitHub\platform\simdecisions-2\src\`

## ShiftCenter Target

`C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\`

Key existing directories:
- `browser/src/primitives/canvas/` — canvas nodes, edges, animations (already ported)
- `browser/src/primitives/terminal/` — terminal primitive
- `browser/src/primitives/text-pane/` — text display
- `browser/src/primitives/tree-browser/` — tree navigation
- `browser/src/primitives/settings/` — settings panel
- `browser/src/primitives/dashboard/` — dashboard
- `browser/src/shell/` — shell frame, reducer, actions
- `browser/src/apps/` — app adapters
- `browser/src/services/` — services (terminal, chat, etc.)
- `browser/src/infrastructure/` — relay bus, event system
- `browser/src/eggs/` — EGG resolver

## Deliverables

### 1. Read Key Files

Read the main entry point(s) and the largest/most important files. Understand:
- What is the top-level component structure?
- How does simulation playback work?
- How does comparison mode work?
- How does collaboration/tabletop work?
- What state management pattern is used (Zustand, Redux, Context)?

### 2. Overlap Analysis

Compare with shiftcenter's existing `browser/src/primitives/canvas/` directory:
- List every file in shiftcenter's canvas directory with line counts
- For each flow designer component, note if an equivalent already exists in shiftcenter
- Identify what's NEW (not yet in shiftcenter) vs what's a DUPLICATE

### 3. Placement Mapping

For each functional group in the flow designer, recommend placement:

| Flow Designer Group | Recommended ShiftCenter Location | Rationale |
|---------------------|--------------------------------|-----------|
| ... | ... | ... |

### 4. Port Complexity Assessment

Rate each group: EASY (copy + fix imports), MEDIUM (needs adaptation), HARD (significant rework needed).

## Output

Write your response to: `.deia/hive/responses/20260314-TASK-093-FLOW-DESIGNER-MAPPING.md`

## Rules

- READ ONLY. Do not modify any files.
- Be specific about file paths, not vague.
- If something doesn't exist where expected, say so — don't guess.
