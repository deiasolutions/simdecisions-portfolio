# TASK-092: Flow Designer Directory Survey + Dependency Analysis

**Role:** BEE
**Model:** sonnet
**Priority:** P0
**Briefing:** 2026-03-14-BRIEFING-flow-designer-survey.md

## Objective

Survey the Flow Designer source directory in the platform repo and produce a complete file inventory with dependency analysis.

## Source Directory

`C:\Users\davee\OneDrive\Documents\GitHub\platform\efemera\frontend\src\`

If this path doesn't exist or is empty, search these alternatives:
- `C:\Users\davee\OneDrive\Documents\GitHub\platform\efemera\frontend\`
- `C:\Users\davee\OneDrive\Documents\GitHub\platform\simdecisions-2\src\`
- Search for ReactFlow usage: grep for `@xyflow/react` or `reactflow` in package.json files

## Deliverables

### 1. Complete File Inventory

List EVERY file in the directory tree. For each file provide:
- Full relative path
- Line count
- File type (component, hook, store, service, type, test, CSS, config)

Group by subdirectory. Provide subtotals per group and grand total.

### 2. External Dependency Analysis

For EVERY source file (.ts, .tsx, .js, .jsx), scan all import statements. Categorize each import as:
- **npm package** (e.g. `@xyflow/react`, `zustand`, `lodash`)
- **internal-same-dir** (relative imports within the flow designer directory)
- **internal-outside** (imports from elsewhere in the platform repo — these are the critical ones)

For all **internal-outside** imports, list:
- The importing file
- The imported module path
- What it provides (types, functions, components, stores)

### 3. npm Package List

Compile a deduplicated list of all npm packages used, with counts of how many files import each.

## Output

Write your response to: `.deia/hive/responses/20260314-TASK-092-FLOW-DESIGNER-SURVEY.md`

## Rules

- READ ONLY. Do not modify any files.
- Be thorough. Every file, every import.
- If the directory has subdirectories, recurse into all of them.
