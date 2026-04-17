/**
 * ThemeMenu
 *
 * * ThemeMenu.tsx — Theme submenu for the View menu
 * Replaces the old hardcoded theme list in MenuBar.tsx
 *
 * Two integration points:
 *   1. View menu → Theme → flyout submenu (this component)
 *   2. Settings panel → "Customize..." (ThemeBrowser, separate component, not here)
 *
 * State contract:
 *   - data-theme on .hhp-root  → design id (e.g. "neon-terminal")
 *   - data-mode  on .hhp-root  → "light" | "dark"
 *   - localStorage keys: sd:hhpanes_theme, sd:hhpanes_mode
 *
 * CSS contract: each theme CSS file uses selector
 *   .hhp-root[data-theme="<id>"]  (dark is default)
 *   .hhp-root[data-theme="<id>"][data-mode="light"]  (if light supported)
 *
 * Dependencies:
 * - import { useState, useRef, useEffect, useCallback } from 'react'
 * - import './ThemeMenu.css'
 *
 * Components/Functions:
 * - THEME_REGISTRY: TypeScript function/component
 * - getStoredTheme: TypeScript function/component
 * - getStoredMode: TypeScript function/component
 * - resolveMode: TypeScript function/component
 * - applyTheme: TypeScript function/component
 * - root: TypeScript function/component
 * - ThemeMenu: TypeScript function/component
 * - classicThemes: TypeScript function/component
 * - newThemes: TypeScript function/component
 * - utilityThemes: TypeScript function/component
 * - activeDesign: TypeScript function/component
 * - resolvedMode: TypeScript function/component
 * - handleDesignClick: TypeScript function/component
 * - newMode: TypeScript function/component
 * - handleModeClick: TypeScript function/component
 *
 * SOURCE AVAILABLE ON REQUEST
 * Contact: Dave Eichler — linkedin.com/in/daaaave-atx
 */

// This file is a stub. See README.md for full source access.
