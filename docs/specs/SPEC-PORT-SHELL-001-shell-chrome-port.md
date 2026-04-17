# SPEC-PORT-SHELL-001: Shell Chrome Component Port

**Status:** Draft
**Priority:** P0
**Source:** `platform/simdecisions-2/src/components/shell/`
**Target:** `shiftcenter/browser/src/shell/components/`
**Rule:** PORT, NOT REWRITE. Same props, same logic, same CSS classes. TypeScript conversion + `var(--sd-*)` theming only.

---

## Mandate

Every file listed below MUST be ported from the old repo to shiftcenter. The port must preserve the original component's behavior, props interface, state management, and user-facing functionality. Acceptable changes:

1. `.jsx` → `.tsx` (add TypeScript types)
2. `useShellStore` / `useSettingsStore` / `useAuthStore` → equivalent ShiftCenter hooks/dispatch
3. CSS class names → keep same names, ensure `var(--sd-*)` variables
4. Portal targets → `.hhp-root` (ShiftCenter portal target)
5. Import paths updated to shiftcenter module structure

Unacceptable changes:
- Removing functionality
- Changing prop interfaces without documenting why
- Rewriting algorithms or state logic
- Adding features not in the original
- Skipping files

---

## Files to Port

### 1. MenuBar.tsx (431 lines → `components/MenuBar.tsx`)

**What it does:** Standard menu bar with File, Edit, View, Help dropdown menus.

**Required behavior:**
- Four menus: File, Edit, View, Help
- Alt+F/E/V/H keyboard shortcuts to open menus
- Escape closes all menus
- **File menu:** New Tab (Hive/Designer/Browser), Close Tab, Settings
- **Edit menu:** Cut, Copy, Paste, Clear Terminal (enabled only when hive pane active)
- **View menu:** Layout presets (single, horizontal split, vertical split, 3-pane, 4-pane), Theme submenu (dark/light)
- **Help menu:** Commands modal (lists 12 slash commands), About modal (version display)
- Modal backdrop click closes modals

**Props:**
```typescript
interface MenuBarProps {
  activeTerminal?: { handleCommand: (cmd: string) => void } | null;
  onNavigate?: (path: string) => void;
}
```

**State:** `openMenu`, `openSubmenu`, `showCommandsHelp`, `showAboutModal`

**CSS classes to preserve:** `.menu-bar`, `.menu-item`, `.menu-button`, `.menu-dropdown`, `.menu-dropdown-item`, `.menu-submenu`, `.menu-divider`, `.menu-modal-overlay`, `.menu-modal`, `.menu-modal-content`, `.menu-modal-close`

**Port notes:** Wire to ShiftCenter's shell dispatch instead of `useShellStore`. Map layout presets to existing `SET_LAYOUT` action.

---

### 2. ShellTabBar.tsx (233 lines → `components/ShellTabBar.tsx`)

**What it does:** Horizontal tab bar showing all open tabs with type icons and close buttons.

**Required behavior:**
- Display all tabs from shell state in horizontal list
- Active tab indicator (highlight)
- Tab type icons: ▶ (hive), ◆ (designer), 🌐 (browser), 📊 (ledger)
- Click tab → activate its pane
- Close button (×) on closeable tabs (hive tab cannot close)
- [+] button opens dropdown to add: Designer, Browser, Ledger tabs
- New tabs assigned to active pane

**Props:** None (reads from shell state)

**State:** `showAddMenu` (add-tab dropdown visibility)

**CSS classes to preserve:** `.shell-tab-bar`, `.tab-list`, `.shell-tab`, `.active`, `.shell-tab-icon`, `.shell-tab-label`, `.shell-tab-close`, `.tab-bar-actions`, `.shell-tab-add-container`, `.shell-tab-add`, `.shell-tab-add-menu`, `.shell-tab-add-option`

---

### 3. WorkspaceBar.tsx (243 lines → `components/WorkspaceBar.tsx`)

**What it does:** Top application bar with logo, undo/redo, active pane indicator, theme toggle, user badge.

**Required behavior:**
- Fixed 36px height bar
- Left: "SHIFTCENTER" logo text
- Undo/Redo buttons with: past/future action labels as tooltips, Ctrl+Shift+Z / Ctrl+Shift+Y shortcuts, disabled when history empty
- Active Pane Indicator: app type icon, label, "active" badge; hides for empty panes
- Theme Toggle: portal-rendered picker (fixed position, z-index 9999) with dark/light options; mouseDown+preventDefault to prevent unmount race
- User Badge: avatar, display name/email, logout link

**Sub-components (all inline, not separate files):**
- `UndoRedoButtons()` — undo/redo with labels and tooltips
- `ActivePaneIndicator()` — shows active pane info
- `ThemeToggle()` — theme picker with portal
- `UserBadge()` — user info and logout

**Port notes:** Wire to ShiftCenter auth context for user/logout instead of `useAuthStore`.

---

### 4. GovernanceProxy.tsx (160 lines → `components/GovernanceProxy.tsx`)

**What it does:** Wraps applets and enforces governance capability ceilings on bus messaging.

**Required behavior:**
- Intercept `bus.send()` — block messages not in `bus_emit` whitelist
- Intercept `bus.subscribe()` — filter incoming messages against `bus_receive` whitelist
- Autonomous action gates (REQUIRE_HUMAN)
- **Platform invariants (always allowed):**
  - Emit: relay_bus, ledger_writer, gate_enforcer, settings_advertisement, metrics_advertisement
  - Receive: relay_bus, ledger_writer, gate_enforcer, settings_update, menu_command
- Log blocked events to Event Ledger via dispatch `LOG_EVENT`
- Provide governed context via Provider

**Props:**
```typescript
interface GovernanceProxyProps {
  nodeId: string;
  permissions: ResolvedPermissions;
  children: React.ReactNode;
}
```

**Port notes:** ShiftCenter already has `browser/src/infrastructure/gate_enforcer/`. This component wraps it at the pane level. Verify the existing gate_enforcer types align with the old `ResolvedPermissions` shape.

---

### 5. PaneMenu.tsx (111 lines → `components/PaneMenu.tsx`)

**What it does:** Hamburger (☰) context menu for individual panes.

**Required behavior:**
- Portal to `.hhp-root` for z-index safety
- **Layout section:** Add Tab (Ctrl+T), Split Vertical (Ctrl+\\), Split Horizontal (Ctrl+-), Flip Split Direction (only if parent is split), Maximize/Restore (Ctrl+Shift+M), Swap with… (toggle swap pending)
- **Lock section:** Lock/Unlock Pane toggle
- **Danger section:** Close Tab Group, Close App (disabled if locked)
- Outside-click handler with containment check (prevent mousedown→unmount race)
- `act(fn)` wrapper closes menu after executing action

**Props:** `nodeId: string`, `isTabbedGroup: boolean`

---

### 6. SpotlightOverlay.tsx (93 lines → `components/SpotlightOverlay.tsx`)

**What it does:** Full-screen modal overlay for REQUIRE_HUMAN governance gates.

**Required behavior:**
- Modal dialog (800×600) with orange border (`var(--sd-orange)`)
- Full-screen backdrop with z-index 1000
- Header: "⚠ Spotlight" with "Click backdrop to dismiss" hint
- Click backdrop → dispatch `REPARENT_TO_BRANCH` to move node from spotlight to layout
- Render pane content inside modal via `<PaneChrome>` + `<AppFrame>` or `<EmptyPane>`

**Props:** `node: ShellNode` (the spotlight branch node)

---

### 7. PinnedPaneWrapper.tsx (73 lines → `components/PinnedPaneWrapper.tsx`)

**What it does:** Renders a fixed-position pinned pane that is layout-immune.

**Required behavior:**
- Fixed position using `node.meta` (x, y, w, h); defaults: 100, 100, 600, 400
- `onMouseDown` → dispatch `SET_FOCUS` to bring to front
- Orange border (`2px solid var(--sd-orange)`)
- Header with 📌 "Pinned" label
- Render content via `<PaneChrome>` + `<AppFrame>` or `<EmptyPane>`
- Respect provided `zIndex` prop

**Props:** `node: ShellNode`, `zIndex: number`

---

### 8. NotificationModal.tsx (64 lines → `components/NotificationModal.tsx`)

**What it does:** Generic modal for alerts, confirmations, help overlays, reject feedback, and info.

**Required behavior:**
- 5 notification types: `alert`, `confirmation`, `help-overlay`, `reject-feedback`, `info`
- Visual mute suppresses `info` and `reject-feedback` types (never suppresses `alert`/`confirmation`)
- `reject-feedback` type: shows text input for user feedback
- Keyboard: Enter = confirm, Escape = cancel
- Backdrop click closes modal; click inside prevents close

**Props:**
```typescript
type NotificationType = 'alert' | 'confirmation' | 'help-overlay' | 'reject-feedback' | 'info';

interface NotificationConfig {
  type: NotificationType;
  title: string;
  message?: string;
  confirmLabel?: string;
  cancelLabel?: string;
  onConfirm?: (feedback?: string) => void;
  onCancel?: () => void;
}

interface NotificationModalProps {
  config: NotificationConfig | null;
  muted: boolean;
  onClose: () => void;
}
```

**CSS classes to preserve:** `.applet-modal-backdrop`, `.applet-modal`, `.applet-modal-title`, `.applet-modal-message`, `.applet-modal-input`, `.applet-modal-actions`, `.applet-modal-btn`, `.applet-modal-btn--cancel`, `.applet-modal-btn--confirm`

---

### 9. ScrollToBottom.tsx (34 lines → `components/ScrollToBottom.tsx`)

**What it does:** Floating button that appears when user scrolls away from bottom.

**Required behavior:**
- Threshold: visible if `scrollHeight - scrollTop - clientHeight > 40px`
- Smooth scroll to bottom on click
- Optional unread count badge
- Returns null (invisible) when at bottom

**Props:**
```typescript
interface ScrollToBottomProps {
  scrollRef: RefObject<HTMLElement>;
  unreadCount?: number;
}
```

**CSS classes to preserve:** `.applet-scroll-bottom`, `.applet-scroll-unread`

---

### 10. LayoutSwitcher.tsx (33 lines → `components/LayoutSwitcher.tsx`)

**What it does:** Button grid for quick layout preset selection.

**Required behavior:**
- 8 layout presets: single, horizontalSplit, verticalSplit, leftAndTwoRight, twoLeftAndRight, twoTopAndBottom, topAndTwoBottom, fourPane
- Each button: icon, label, onclick → dispatch `SET_LAYOUT(preset)`
- Export `LAYOUT_ICONS` constant

**CSS classes to preserve:** `.layout-switcher`, `.layout-button`

---

### 11. ShortcutsPopup.tsx (27 lines → `components/ShortcutsPopup.tsx`)

**What it does:** Modal popup listing keyboard shortcuts.

**Required behavior:**
- Filter to features with `shortcut` property
- Table: feature label | `<kbd>` shortcut
- Backdrop click closes; click inside prevents close

**Props:**
```typescript
interface ShortcutsPopupProps {
  features: { key: string; label: string; shortcut?: string; description?: string }[];
  onClose: () => void;
}
```

**CSS classes to preserve:** `.applet-modal-backdrop`, `.applet-shortcuts-popup`, `.applet-modal-title`, `.applet-shortcuts-table`, `.applet-shortcuts-label`, `.applet-shortcuts-key`

---

### 12. HighlightOverlay.tsx (16 lines → `components/HighlightOverlay.tsx`)

**What it does:** Simple tooltip overlay for highlighting UI elements.

**Required behavior:**
- Show label and optional `<kbd>` shortcut
- Returns null if not `visible`

**Props:**
```typescript
interface HighlightOverlayProps {
  label: string;
  shortcut?: string;
  visible: boolean;
}
```

**CSS classes to preserve:** `.applet-highlight-tooltip`, `.applet-highlight-label`, `.applet-highlight-shortcut`

---

### 13. dragDropUtils.ts (62 lines → `dragDropUtils.ts`)

**What it does:** Drag-drop pattern matching and MIME type detection utilities.

**Required behavior — 3 functions:**

```typescript
// Exact match or wildcard suffix (e.g. "image/*" matches "image/png")
function matchesAcceptPattern(dataType: string, pattern: string): boolean;

// Check if pane's accept list includes given dataType
function canPaneAcceptDrop(accepts: string[], dataType: string): boolean;

// Map File to MIME-type string
// Special: .ir.json → "file/ir.json", .bpmn → "file/bpmn"
// Fallback: "file/{extension}"
function getDataTypeFromFile(file: File): string;
```

---

## CSS Requirements

All ported components MUST use `var(--sd-*)` CSS variables. No hex colors, no rgb(), no named colors.

Port the following CSS class definitions alongside the components. If a `.css` file existed in old for these components, port it. If styles were inline, create a corresponding CSS file using `var(--sd-*)` variables.

---

## Integration Points

After porting, these components must be wired into the shell:

1. **MenuBar** → rendered at top of Shell.tsx when `ui.menuBar: true` in EGG config
2. **ShellTabBar** → rendered below MenuBar when `ui.shellTabBar: true` in EGG config
3. **WorkspaceBar** → rendered at very top when `ui.workspaceBar: true` in EGG config
4. **GovernanceProxy** → wraps each AppFrame in ShellNodeRenderer.tsx
5. **PaneMenu** → triggered from PaneChrome hamburger button
6. **SpotlightOverlay** → rendered when shell state has spotlight branch nodes
7. **PinnedPaneWrapper** → rendered for pinned nodes in shell state
8. **NotificationModal** → rendered at shell level, driven by notification state
9. **ScrollToBottom** → used inside scrollable pane containers
10. **LayoutSwitcher** → accessible from View menu or command palette
11. **ShortcutsPopup** → accessible from Help menu
12. **HighlightOverlay** → used by onboarding/tutorial system
13. **dragDropUtils** → imported by AppFrame and PaneContent for drop handling

---

## Verification

For each ported component:
1. Vitest unit test covering: renders without crash, props work, key interactions (click, keyboard)
2. Manual check: component appears, behaves identically to old repo
3. No new CSS classes that don't use `var(--sd-*)` variables
4. TypeScript compiles with strict mode

**Total: 13 files, ~1,580 lines of source to port.**
