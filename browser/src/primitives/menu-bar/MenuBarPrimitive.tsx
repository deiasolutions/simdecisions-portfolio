/**
 * MenuBarPrimitive
 *
 * * MenuBarPrimitive.tsx — Menu bar as a pane primitive
 * Ported from MenuBar.tsx (594 lines), registered as appType: menu-bar
 *
 * Renders File/Edit/View/Help menus plus syndicated toolbar actions.
 * Subscribes to menu:items-changed for app-specific menu items from focused pane.
 * On mobile (immersive), returns null — syndicated items route to command palette.
 *
 * Dependencies:
 * - import { useState, useEffect, useRef, useCallback, useMemo, Fragment, type ReactElement, type ReactNode } from 'react';
 * - import { createPortal } from 'react-dom';
 * - import { useShell } from '../../infrastructure/relay_bus';
 * - import { BUS_MESSAGE_TYPES } from '../../infrastructure/relay_bus/constants';
 * - import { useCommandRegistry, type CommandDefinition } from '../../services/commands/commandRegistry';
 * - import { ThemeMenu, applyTheme } from '../../shell/components/ThemeMenu';
 * - import type { ToolbarAction, SyndicatedMenuGroup } from '../../shell/types';
 * - import type { AppRendererProps } from '../../shell/components/appRegistry';
 * - import './MenuBarPrimitive.css';
 *
 * Components/Functions:
 * - FixedDropdown: TypeScript function/component
 * - dropRef: TypeScript function/component
 * - calculatePosition: TypeScript function/component
 * - rect: TypeScript function/component
 * - dropRect: TypeScript function/component
 * - hhpRoot: TypeScript function/component
 * - themeAttr: TypeScript function/component
 * - modeAttr: TypeScript function/component
 * - MenuBarPrimitive: TypeScript function/component
 * - menuBarRef: TypeScript function/component
 * - fileRef: TypeScript function/component
 * - editRef: TypeScript function/component
 * - viewRef: TypeScript function/component
 * - toolsRef: TypeScript function/component
 * - helpRef: TypeScript function/component
 *
 * SOURCE AVAILABLE ON REQUEST
 * Contact: Dave Eichler — linkedin.com/in/daaaave-atx
 */

// This file is a stub. See README.md for full source access.
