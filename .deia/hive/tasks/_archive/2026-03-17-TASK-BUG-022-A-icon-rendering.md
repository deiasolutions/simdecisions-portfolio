# TASK-BUG-022-A: Fix Icon Rendering in TreeNodeRow

## Objective
Palette component icons must display visually in the tree-browser. TreeNodeRow must handle both CSS class icons AND Unicode/emoji text icons.

## Context

**Problem:** The Canvas components/palette panel shows a plain text list with no visible icons.

**Root cause:** TreeNodeRow line 82 renders: `<span className={tree-node-icon ${node.icon}} />`. This works for CSS class icons (e.g., `icon: "icon-task"`) but FAILS for Unicode character icons (e.g., `icon: "◉"`). When the icon is a Unicode character, it's added as a className (invalid CSS), so nothing renders.

**paletteAdapter provides 8 Unicode icons:**
- Process: '◉' (Task), '◈' (Queue)
- Flow Control: '●' (Start), '○' (End), '◆' (Decision), '◈' (Checkpoint)
- Parallel: '⊢' (Split), '⊣' (Join)
- Resources: '▭' (Group)

**Category group icons are also Unicode:** '⚙', '⊙', '⫷', '📦'

**Fix required:** TreeNodeRow must detect icon type and render appropriately:
- If `node.icon` is a single Unicode character or emoji → render as text content: `<span className="tree-node-icon">{node.icon}</span>`
- If `node.icon` is a CSS class identifier → render as className: `<span className={tree-node-icon ${node.icon}} />`

## Files to Read First
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\tree-browser\TreeNodeRow.tsx` (114 lines — modify line 82)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\tree-browser\adapters\paletteAdapter.ts` (96 lines — reference, do NOT modify)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\tree-browser\types.ts` (80 lines — reference)

## Deliverables
- [ ] TreeNodeRow.tsx modified to detect icon type (Unicode vs CSS class)
- [ ] Detection logic: if icon length is 1-2 chars OR starts with emoji range → text icon
- [ ] Unicode icons render as text: `<span className="tree-node-icon">{node.icon}</span>`
- [ ] CSS class icons render as className: `<span className={tree-node-icon ${node.icon}} />`
- [ ] All 8 palette component icons render correctly: ◉, ◈, ●, ○, ◆, ⊢, ⊣, ▭
- [ ] All 4 category group icons render correctly: ⚙, ⊙, ⫷, 📦

## Test Requirements
- [ ] **TDD:** Tests written FIRST before modifying TreeNodeRow.tsx
- [ ] **Unit test 1:** TreeNodeRow with `icon: "◉"` renders `<span class="tree-node-icon">◉</span>` (text content, NOT className)
- [ ] **Unit test 2:** TreeNodeRow with `icon: "icon-task"` renders `<span class="tree-node-icon icon-task"></span>` (className)
- [ ] **Unit test 3:** TreeNodeRow with `icon: "📦"` renders emoji as text content
- [ ] **Integration test:** paletteAdapter → TreeBrowser → verify all palette node icons render with text content (use test query to check DOM)
- [ ] **Edge case:** `icon: undefined` or `icon: ""` → no icon span rendered (existing behavior preserved)
- [ ] All tests pass

## Constraints
- No file over 500 lines (TreeNodeRow.tsx is 114 lines — will not exceed limit)
- CSS: `var(--sd-*)` only (no CSS changes required for this task)
- No stubs — full implementation of icon detection logic
- Do NOT modify paletteAdapter.ts — icons are correct, only TreeNodeRow needs fixing

## Implementation Guidance

**Detection heuristic (simple and robust):**
```typescript
// Detect if icon is Unicode text vs CSS class
const isTextIcon = node.icon && (
  node.icon.length <= 2 ||               // Single char or 2-char emoji
  /[\u{1F300}-\u{1F9FF}]/u.test(node.icon)  // Emoji range
);
```

**Render logic:**
```typescript
{node.icon && (
  isTextIcon
    ? <span className="tree-node-icon">{node.icon}</span>
    : <span className={`tree-node-icon ${node.icon}`} />
)}
```

## Acceptance Criteria
- [ ] TreeNodeRow handles both CSS class and Unicode icons correctly
- [ ] All 8 palette component types show icons in components panel (visual verification via test)
- [ ] All 4 category group icons show in palette tree (visual verification via test)
- [ ] Tests pass: minimum 5 tests (3 unit + 1 integration + 1 edge case)
- [ ] No hardcoded colors introduced
- [ ] No stubs shipped
- [ ] TreeNodeRow.tsx remains under 500 lines

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `.deia/hive/responses/20260317-TASK-BUG-022-A-RESPONSE.md`

The response MUST contain these 8 sections:
1. **Header** — task ID, title, status (COMPLETE/FAILED), model, date
2. **Files Modified** — every file created/modified/deleted, full paths
3. **What Was Done** — bullet list of concrete changes
4. **Test Results** — test files run, pass/fail counts
5. **Build Verification** — test/build output summary
6. **Acceptance Criteria** — copy from task, mark [x] or [ ]
7. **Clock / Cost / Carbon** — all three, never omit any
8. **Issues / Follow-ups** — edge cases, dependencies, next tasks

DO NOT skip any section.
