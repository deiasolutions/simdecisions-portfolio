/**
 * PaneMenu
 *
 * * PaneMenu.tsx — Hamburger ☰ menu with labeled layout actions (portal for z-safety).
 * Fix: outside-click handler checks containment before closing, preventing the
 * mousedown→unmount race that swallowed item clicks.
 *
 * Dependencies:
 * - import { createPortal } from 'react-dom';
 * - import { useState, useEffect, useRef, useMemo } from 'react';
 * - import type React from 'react';
 * - import { useShell } from '../../infrastructure/relay_bus';
 * - import { findNode, findParent } from '../utils';
 * - import { ChromeBtn } from './ChromeBtn';
 * - import type { ContextMenuItem } from './ContextMenu';
 *
 * Components/Functions:
 * - PaneMenu: TypeScript function/component
 * - shell: TypeScript function/component
 * - dispatch: TypeScript function/component
 * - root: TypeScript function/component
 * - maximizedPaneId: TypeScript function/component
 * - swapPendingId: TypeScript function/component
 * - btnRef: TypeScript function/component
 * - menuRef: TypeScript function/component
 * - h: TypeScript function/component
 * - toggle: TypeScript function/component
 * - btnRect: TypeScript function/component
 * - paneRect: TypeScript function/component
 * - btnCenterX: TypeScript function/component
 * - btnCenterY: TypeScript function/component
 * - paneCenterX: TypeScript function/component
 *
 * SOURCE AVAILABLE ON REQUEST
 * Contact: Dave Eichler — linkedin.com/in/daaaave-atx
 */

// This file is a stub. See README.md for full source access.
