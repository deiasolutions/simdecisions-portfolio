/**
 * treeBrowserAdapter
 *
 * * treeBrowserAdapter.tsx — App registry adapter for tree-browser primitive
 *
 * Maps AppRendererProps to TreeBrowser props.
 * Dispatches to correct adapter based on config.adapter:
 *   - 'chat-history': loads conversations from chatApi
 *   - 'filesystem': loads directory tree from hivenode /repo/tree
 *   - 'palette': canvas node palette (drag-to-create)
 *   - 'properties': selected canvas node properties inspector
 *
 * Dependencies:
 * - import { useState, useEffect, useCallback, useContext, useRef } from 'react'
 * - import { TreeBrowser } from '../primitives/tree-browser'
 * - import type { TreeNodeData, TreeBrowserPaneConfig } from '../primitives/tree-browser'
 * - import { loadChatHistory } from '../primitives/tree-browser/adapters/chatHistoryAdapter'
 * - import {
 * - import { createPaletteAdapter } from '../primitives/tree-browser/adapters/paletteAdapter'
 * - import { createPropertiesAdapter } from '../primitives/tree-browser/adapters/propertiesAdapter'
 * - import type { PropertiesAdapter } from '../primitives/tree-browser/adapters/propertiesAdapter'
 * - import { createBranchesAdapter } from '../primitives/tree-browser/adapters/branchesAdapter'
 * - import type { BranchesAdapter } from '../primitives/tree-browser/adapters/branchesAdapter'
 *
 * Components/Functions:
 * - EMPTY_TEXT: TypeScript function/component
 * - AUTO_EXPAND_ADAPTERS: TypeScript function/component
 * - TreeBrowserAdapter: TypeScript function/component
 * - paneConfig: TypeScript function/component
 * - adapter: TypeScript function/component
 * - ctx: TypeScript function/component
 * - bus: TypeScript function/component
 * - propsAdapterRef: TypeScript function/component
 * - branchesAdapterRef: TypeScript function/component
 * - busRef: TypeScript function/component
 * - nodesRef: TypeScript function/component
 * - expandedIdsRef: TypeScript function/component
 * - load: TypeScript function/component
 * - rp: TypeScript function/component
 * - pa: TypeScript function/component
 *
 * SOURCE AVAILABLE ON REQUEST
 * Contact: Dave Eichler — linkedin.com/in/daaaave-atx
 */

// This file is a stub. See README.md for full source access.
