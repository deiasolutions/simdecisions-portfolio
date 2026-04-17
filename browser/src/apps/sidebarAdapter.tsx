/**
 * sidebarAdapter
 *
 * * sidebarAdapter.tsx — Activity bar + switchable panel sidebar
 *
 * Renders a vertical icon strip (activity bar) on the left.
 * Clicking an icon switches the panel content on the right.
 * Panel routing:
 *   - explorer → TreeBrowserAdapter (filesystem)
 *   - frank    → TreeBrowserAdapter (chat-history)
 *   - palette  → NodePalette (embedded)
 *   - tree-browser → TreeBrowserAdapter (properties, branches, etc.)
 *   - sim-config-panel → SimConfigPanel (inline)
 *   - others   → placeholder "coming soon"
 *
 * Mode integration: panels with `action` field send a bus event on click
 * (e.g. sim:mode-change) and subscribe to sim:mode-updated to track state.
 *
 * Dependencies:
 * - import { useState, useEffect, useContext, useCallback } from 'react'
 * - import { TreeBrowserAdapter } from './treeBrowserAdapter'
 * - import { ShellCtx } from '../infrastructure/relay_bus'
 * - import { useCommandRegistry } from '../services/commands/commandRegistry'
 * - import NodePalette from './sim/components/flow-designer/NodePalette'
 * - import type { AppRendererProps } from '../shell/components/appRegistry'
 *
 * Components/Functions:
 * - PANEL_TREE_CONFIG: TypeScript function/component
 * - PlaceholderPanel: TypeScript function/component
 * - SidebarAdapter: TypeScript function/component
 * - cfg: TypeScript function/component
 * - ctx: TypeScript function/component
 * - bus: TypeScript function/component
 * - panels: TypeScript function/component
 * - footerPanels: TypeScript function/component
 * - allPanels: TypeScript function/component
 * - defaultId: TypeScript function/component
 * - barWidth: TypeScript function/component
 * - panelWidth: TypeScript function/component
 * - storageKey: TypeScript function/component
 * - stored: TypeScript function/component
 * - unsub: TypeScript function/component
 *
 * SOURCE AVAILABLE ON REQUEST
 * Contact: Dave Eichler — linkedin.com/in/daaaave-atx
 */

// This file is a stub. See README.md for full source access.
