# TASK-MON-004: code.shiftcenter.com EGG

**Status:** QUEUED
**Wave:** Wave C (assembles MON-001 + MON-002 + MON-003)
**Assigned To:** BEE-001
**Date:** 2026-03-24
**Depends On:** TASK-MON-001, TASK-MON-002, TASK-MON-003 (all must be complete)
**Blocks:** Nothing

---

## Context

With the Monaco applet built and wired, this task assembles `code.shiftcenter.com` — the
ShiftCenter code editing product as an EGG config. Two tab layouts: `code-default`
(editor + log-viewer side by side) and `code-zen` (editor only, no chrome). Both share
the same `nodeId: "editor-main"` so document content survives tab swaps.

Reference: SPEC-CODE-EGG-001-code-shiftcenter-monaco-playwright.md, SDK-APP-BUILDER-v0.2.0,
SPEC-EGG-SCHEMA-v1.

---

## Scope

Write `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\eggs\code.egg.md` and register it in `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\eggs\index.ts`.

### EGG structure

**Tab 1 — `code-default`**
Layout: horizontal split (60/40), editor left, log-viewer right.
```
editor-main (code-editor) | log-output (log-viewer)
```

**Tab 2 — `code-zen`**
Layout: single pane, editor only, all chrome hidden.
```
editor-main (code-editor)
```

Both tabs declare `nodeId: "editor-main"` — content survives the swap.

### EGG file requirements

1. **Frontmatter:**
   ```yaml
   egg: code
   version: 1.0.0
   displayName: Code
   description: Monaco-powered code editor with AI feedback loop.
   favicon: global-commons://icons/code.png
   subdomain: code
   ```

2. **Two layout blocks** (one per tab, labeled `code-default` and `code-zen`)

3. **links block** — wires pane slots:
   ```json
   {
     "editor": "editor-main",
     "output": "log-output"
   }
   ```

4. **commands block** — registers commands into Command Registry on mount:
   ```json
   [
     { "id": "code.format",      "label": "Format Document", "shortcut": "Shift+Alt+F" },
     { "id": "code.save",        "label": "Save File",       "shortcut": "Ctrl+S" },
     { "id": "code.zen-toggle",  "label": "Zen Mode",        "shortcut": "Ctrl+K Z" }
   ]
   ```

5. **ui block** for `code-zen` tab:
   ```json
   {
     "hideMenuBar": true,
     "hideStatusBar": false,
     "hideTabBar": false,
     "hideActivityBar": true
   }
   ```

6. **settings block** (defaults):
   ```json
   {
     "language": "typescript",
     "theme": "vs-dark",
     "autoSave": false,
     "embeddingStrategy": "tfidf"
   }
   ```

### Subdomain registration

Verify `code` subdomain exists in `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\eggs\eggResolver.ts` hardcoded fallback table (should already be present at line ~135 as `'code.shiftcenter.com': 'code'`). If missing, add it following the same pattern as efemera subdomain.

### index.ts registration

```ts
import codeEgg from './code.egg.md'  // C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\eggs\code.egg.md
export const eggs = { ..., code: codeEgg }
```

---

## File Locations

```
C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\eggs\
  code.egg.md               ← new file (this task)
  index.ts                  ← add code egg registration

C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\eggs\
  __tests__/
    codeEgg.test.ts         ← EGG inflate test (TDD — write first)
```

---

## Constraints

- `.egg.ir.json` is machine-generated — never hand-author it
- `nodeId: "editor-main"` must be identical across both tabs (not a copy — same string)
- EGG format is CC BY 4.0 — no proprietary constructs in the `.egg.md` file itself
- TDD: write inflate test first, then write the EGG
- Do NOT add app-specific bus slots (use `to_bus` for any custom messaging)

---

## Acceptance Criteria

- [ ] `code.egg.md` inflates without errors (EGG loader parses cleanly)
- [ ] `code-default` tab renders editor + log-viewer side by side
- [ ] `code-zen` tab renders editor only with activity bar hidden
- [ ] Switching between tabs preserves editor content (shared `nodeId`)
- [ ] `Ctrl+S` triggers `code.save` command (registered in Command Registry)
- [ ] `code` subdomain routes correctly in EGG router
- [ ] All tests pass (minimum 5 tests)
- [ ] `npx vite build` passes

---

## Response Requirements -- MANDATORY

Write response file: `.deia/hive/responses/20260324-TASK-MON-004-RESPONSE.md`

Required sections (all 8):
1. **Header** — task ID, title, status, model, date
2. **Files Modified** — full absolute paths
3. **What Was Done** — concrete changes, not intent
4. **Test Results** — file names, pass/fail counts
5. **Build Verification** — last 5 lines of `vite build` output
6. **Acceptance Criteria** — each item marked [x] or [ ] with explanation
7. **Clock / Cost / Carbon** — all three, never omit
8. **Issues / Follow-ups** — blockers, edge cases, recommendations

YAML frontmatter required:
```yaml
features_delivered: [code-egg, code-subdomain, code-zen-tab]
features_modified: [egg-registry]
features_broken: []
test_summary: "X/Y passing"
area_code: EGG
```
