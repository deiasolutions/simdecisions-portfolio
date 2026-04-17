/**
 * TabBarPrimitive
 *
 * * TabBarPrimitive.tsx — Tab bar chrome primitive
 *
 * Horizontal tab strip for mode switching within a pane group.
 * - Binds to targetSplit (nodeId of content pane it controls)
 * - Emits shell:action-requested bus message with SWAP_APP payload
 * - Supports pinned tabs (no close button, shows pin icon)
 * - Supports allowedTabs (+ button menu for adding new tabs)
 * - Horizontally scrollable on narrow viewports
 *
 * Dependencies:
 * - import { useState, type ReactElement } from 'react';
 * - import { useShell, BUS_MESSAGE_TYPES } from '../../infrastructure/relay_bus';
 * - import type { AppRendererProps } from '../../shell/components/appRegistry';
 * - import './TabBarPrimitive.css';
 *
 * Components/Functions:
 * - TabBarPrimitive: TypeScript function/component
 * - shell: TypeScript function/component
 * - tabBarConfig: TypeScript function/component
 * - handleTabClick: TypeScript function/component
 * - handleAddTab: TypeScript function/component
 * - isPinned: TypeScript function/component
 * - isActive: TypeScript function/component
 * - isTabPinned: TypeScript function/component
 *
 * SOURCE AVAILABLE ON REQUEST
 * Contact: Dave Eichler — linkedin.com/in/daaaave-atx
 */

// This file is a stub. See README.md for full source access.
