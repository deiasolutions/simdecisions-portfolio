# TASK-BUG-068: Fix Explorer Tree File Type Icons and Directory Indicators

## Objective

Fix explorer tree items in Code EGG so they render with correct file type icons and directory indicators. Currently items show no visual differentiation between files and directories, and no file type icons (e.g., TypeScript, Python, Markdown).

## Context

The filesystemAdapter already has a `getFileIcon()` function (lines 22-40) that returns emoji icons for different file types:
- Directories: 📁
- TypeScript: 🟦
- JavaScript: 🟨
- Python: 🐍
- Markdown: 📝
- JSON: 📋
- CSS: 🎨
- HTML: 🌐
- YAML: ⚙️
- Default: 📄

The TreeNodeRow component (lines 106-109) renders the icon:
```tsx
{node.icon && (/^[a-zA-Z]/.test(node.icon)
  ? <span className={`tree-node-icon ${node.icon}`} />
  : <span className="tree-node-icon">{node.icon}</span>
)}
```

**Problem:** The filesystemAdapter may not be calling `getFileIcon()` or not passing the icon to the TreeNodeData. Or the icon is being passed but not rendered correctly.

## Files to Read First

- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\tree-browser\adapters\filesystemAdapter.ts`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\tree-browser\TreeNodeRow.tsx` (lines 106-109)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\tree-browser\types.ts` (TreeNodeData interface)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\treeBrowserAdapter.tsx` (how filesystem adapter is invoked)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\eggs\code.egg.md` (explorer config)

## Deliverables

- [ ] Root cause identified: why are icons not showing?
- [ ] Icons populated in TreeNodeData by filesystemAdapter
- [ ] Directory indicator: trailing `/` or folder icon for directories
- [ ] File type icons: correct emoji for each extension
- [ ] Unknown file types: default file icon (📄)
- [ ] TreeNodeRow renders icons correctly
- [ ] Test file: `browser/src/primitives/tree-browser/adapters/__tests__/filesystemAdapter.icons.test.ts` (8+ tests)
- [ ] Test file: `browser/src/primitives/tree-browser/__tests__/TreeNodeRow.icon.test.tsx` (6+ tests)
- [ ] All tests pass (existing + new)

## Test Requirements

- [ ] Tests written FIRST (TDD)
- [ ] All tests pass
- [ ] Edge cases covered:
  - Directory nodes (should show folder icon)
  - TypeScript files (.ts, .tsx)
  - JavaScript files (.js, .jsx)
  - Python files (.py)
  - Markdown files (.md)
  - JSON files (.json)
  - CSS files (.css)
  - HTML files (.html)
  - YAML files (.yml, .yaml)
  - Unknown extension (should show default file icon)
  - File with no extension (should show default file icon)
  - Deeply nested directory (icons should still render)
  - Empty directory (folder icon, no children)
- [ ] Minimum 14 test cases total (8 filesystemAdapter + 6 TreeNodeRow)
- [ ] No existing tests broken

## Constraints

- No file over 500 lines
- CSS: `var(--sd-*)` only — no hardcoded colors
- No stubs — fully implement all functions
- Do NOT change icon set (emoji icons) — keep existing getFileIcon() logic
- Do NOT modify TreeNodeRow icon rendering logic (lines 106-109) — focus on adapter
- Do NOT add new dependencies (icon libraries) — use existing emoji icons

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `.deia/hive/responses/20260324-TASK-BUG-068-RESPONSE.md`

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

## Bug Details (from inventory)

- **ID:** BUG-068
- **Severity:** P0
- **Component:** browser/tree-browser
- **Title:** Explorer tree items not rendering with correct file type icons or directory indicators
- **Status:** OPEN
- **Description:** Items in the code app explorer don't show file type differentiation or directory markers. All items appear with no icon or generic icon regardless of type.

## Manual Verification Steps (to include in response)

After implementation, verify manually:
1. Load Code EGG
2. Open explorer tree (sidebar)
3. Navigate to a directory with mixed file types (e.g., `browser/src`)
4. **Expected:**
   - Directories show folder icon (📁)
   - TypeScript files show blue square (🟦)
   - Markdown files show memo icon (📝)
   - JSON files show clipboard icon (📋)
   - Other file types show appropriate icons
5. Expand a directory
6. **Expected:** Child items also show correct icons
7. Navigate to root
8. **Expected:** All icons render correctly at all nesting levels

Document these steps in the response with screenshots or text description of actual vs expected behavior.

## Likely Root Cause

Based on reading filesystemAdapter.ts:
- `getFileIcon()` function exists (lines 22-40)
- Function takes `(name: string, isDir: boolean)`
- Function returns correct emoji icons for known file types

**Hypothesis:** The function exists but is NOT being called when creating TreeNodeData nodes. Check line ~80-100 where TreeNodeData is constructed. The `icon` field may be missing or undefined.

**Fix:** Call `getFileIcon(name, isDir)` and assign result to `node.icon` when creating TreeNodeData.
