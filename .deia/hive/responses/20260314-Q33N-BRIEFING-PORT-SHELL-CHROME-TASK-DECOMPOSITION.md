# Q33N Task Decomposition: Shell Chrome Component Port

**Date:** 2026-03-14
**Briefing:** `.deia/hive/coordination/2026-03-14-BRIEFING-PORT-SHELL-CHROME.md`
**Status:** AWAITING Q33NR REVIEW

---

## Summary

I have decomposed the shell chrome port briefing into **4 task files** organized in 3 waves + integration:

1. **TASK-100** — Wave 1: Standalone components (6 files, ~236 lines total)
2. **TASK-101** — Wave 2: Shell context components (4 files, ~437 lines total)
3. **TASK-102** — Wave 3: Top chrome bars (3 files, ~907 lines total)
4. **TASK-103** — Integration (wire all components into Shell.tsx)

**Total:** 13 components + dragDropUtils + integration = ~1,580 lines of source to port.

---

## Task Files Created

| Task | File | Components | Model | Estimated Effort |
|------|------|------------|-------|------------------|
| TASK-100 | `.deia/hive/tasks/2026-03-14-TASK-100-PORT-SHELL-CHROME-WAVE1.md` | HighlightOverlay, ScrollToBottom, ShortcutsPopup, NotificationModal, LayoutSwitcher, dragDropUtils | Haiku | 2–3 hours |
| TASK-101 | `.deia/hive/tasks/2026-03-14-TASK-101-PORT-SHELL-CHROME-WAVE2.md` | PaneMenu, PinnedPaneWrapper, SpotlightOverlay, GovernanceProxy | Sonnet | 3–4 hours |
| TASK-102 | `.deia/hive/tasks/2026-03-14-TASK-102-PORT-SHELL-CHROME-WAVE3.md` | MenuBar, ShellTabBar, WorkspaceBar | Sonnet | 4–5 hours |
| TASK-103 | `.deia/hive/tasks/2026-03-14-TASK-103-INTEGRATE-SHELL-CHROME.md` | Integration into Shell.tsx, ShellNodeRenderer.tsx, PaneChrome.tsx | Sonnet | 2–3 hours |

---

## Dependency Chain

```
TASK-100 (Wave 1: Standalone)
  ↓
TASK-101 (Wave 2: Shell context — needs NotificationModal, ShortcutsPopup from Wave 1)
  ↓
TASK-102 (Wave 3: Top chrome — needs LayoutSwitcher, NotificationModal, ShortcutsPopup from Wave 1)
  ↓
TASK-103 (Integration — needs all waves complete)
```

**Dispatch strategy:**
- TASK-100 first (parallel bees possible: 2–3 components each)
- TASK-101 after TASK-100 completes (can run in parallel with TASK-102 if needed)
- TASK-102 after TASK-100 completes (Wave 1 provides dependencies)
- TASK-103 after all waves complete

---

## What Each Task Delivers

### TASK-100 (Wave 1: Standalone)
**Files:**
- `browser/src/shell/components/HighlightOverlay.tsx` (16 lines)
- `browser/src/shell/components/ScrollToBottom.tsx` (34 lines)
- `browser/src/shell/components/ShortcutsPopup.tsx` (27 lines)
- `browser/src/shell/components/NotificationModal.tsx` (64 lines)
- `browser/src/shell/components/LayoutSwitcher.tsx` (33 lines)
- `browser/src/shell/dragDropUtils.ts` (62 lines)
- 6 test files

**Why Haiku:** Small, straightforward ports. No shell context dependencies. Minimal logic.

---

### TASK-101 (Wave 2: Shell Context)
**Files:**
- `browser/src/shell/components/PaneMenu.tsx` (111 lines)
- `browser/src/shell/components/PinnedPaneWrapper.tsx` (73 lines)
- `browser/src/shell/components/SpotlightOverlay.tsx` (93 lines)
- `browser/src/shell/components/GovernanceProxy.tsx` (160 lines)
- 4 test files

**Why Sonnet:** Requires understanding shell context integration, dispatch actions, existing PaneChrome/AppFrame/EmptyPane components. GovernanceProxy is complex (bus interception, permission enforcement).

---

### TASK-102 (Wave 3: Top Chrome)
**Files:**
- `browser/src/shell/components/MenuBar.tsx` (431 lines)
- `browser/src/shell/components/ShellTabBar.tsx` (233 lines)
- `browser/src/shell/components/WorkspaceBar.tsx` (243 lines)
- 3 test files

**Why Sonnet:** MenuBar is 431 lines (most complex component). WorkspaceBar has inline sub-components and portal logic. ShellTabBar manages tab state.

---

### TASK-103 (Integration)
**Files Modified:**
- `browser/src/shell/components/Shell.tsx` (replace stubs, add WorkspaceBar/SpotlightOverlay/PinnedPaneWrapper/NotificationModal)
- `browser/src/shell/components/ShellNodeRenderer.tsx` (wrap AppFrame in GovernanceProxy)
- `browser/src/shell/components/PaneChrome.tsx` (wire PaneMenu)
- `browser/src/shell/useEggInit.ts` (add `workspaceBar?: boolean` to EggUiConfig)
- `browser/src/shell/components/__tests__/ShellChromeIntegration.test.tsx` (new integration test)

**Why Sonnet:** Integration requires understanding entire shell architecture, EGG config system, and component wiring.

---

## Verification Checklist

I have verified the following for each task file:

- [ ] All file paths are **absolute** (not relative)
- [ ] **"Files to Read First"** section lists all source files (old repo) and context files (shiftcenter)
- [ ] **Deliverables** are concrete and checkable
- [ ] **Test Requirements** specify TDD, edge cases, and acceptance criteria
- [ ] **Constraints** include: no file over 500 lines, `var(--sd-*)` CSS only, no stubs, props match spec, CSS classes match spec
- [ ] **Response Requirements** section is present and mandatory
- [ ] No hardcoded colors mentioned
- [ ] No vague acceptance criteria (all specific and testable)
- [ ] Dependencies between tasks are explicit

---

## Issues / Questions for Q33NR

1. **NotificationModal state management:** The spec mentions NotificationModal is "driven by notification state" but doesn't specify where this state lives. Current shell state has `notification` per-pane (NotificationLevel), but NotificationModal seems like a shell-level modal. Should TASK-103 add a new shell state slice for this, or is it wired differently?

2. **GovernanceProxy permissions source:** The spec says `permissions: ResolvedPermissions` but doesn't specify where these come from. Should this read from `node.meta.permissions` or is there a global permissions registry? TASK-101 is instructed to verify existing `gate_enforcer/` alignment.

3. **WorkspaceBar auth integration:** WorkspaceBar needs `useAuthStore` for user badge (avatar, display name, logout). Does shiftcenter have an auth context/hook, or should this be stubbed for now?

4. **Parallel dispatch for TASK-100:** Wave 1 has 6 small components. Should I split this into 2 parallel tasks (3 components each) to speed up execution, or keep as one task?

5. **Theme toggle in WorkspaceBar:** The spec mentions a ThemeToggle sub-component with portal rendering. Shell.tsx already has a ThemePicker component. Should WorkspaceBar reuse ThemePicker or port the old ThemeToggle as a separate inline component?

---

## Next Steps

**Awaiting Q33NR approval to dispatch bees.**

Once approved:
1. Dispatch TASK-100 (Haiku)
2. Wait for TASK-100 completion
3. Dispatch TASK-101 and TASK-102 in parallel (both Sonnet)
4. Wait for TASK-101 and TASK-102 completion
5. Dispatch TASK-103 (Sonnet)
6. Review all responses, archive tasks, run inventory

---

**Q33N (Bot ID: QUEEN-2026-03-14-BRIEFING-PORT-SHELL)**
