/**
 * TopBar
 *
 * * TopBar.tsx — Top bar primitive component
 *
 * Replaces WorkspaceBar as a pane primitive.
 * Renders: hamburger, brand icon + displayName, Three Currencies chip, kebab menu, user avatar.
 * Slim 28px variant for compact/immersive modes.
 * Subscribes to RTD bus events for currency chip.
 *
 * Dependencies:
 * - import { useState, useEffect, useRef, useCallback, type ReactElement } from 'react'
 * - import { createPortal } from 'react-dom'
 * - import { useShell } from '../../infrastructure/relay_bus'
 * - import { getIdentity } from '../../services/identity/identityService'
 * - import { clearToken, isAuthenticated } from '../../primitives/auth/authStore'
 * - import { getThreeCsVisibility } from '../settings/settingsStore'
 * - import type { Identity } from '../../services/identity/types'
 * - import type { AppRendererProps } from '../../shell/components/appRegistry'
 * - import { CurrencyChip } from './CurrencyChip'
 * - import './TopBar.css'
 *
 * Components/Functions:
 * - getInitials: TypeScript function/component
 * - trimmed: TypeScript function/component
 * - words: TypeScript function/component
 * - word: TypeScript function/component
 * - first: TypeScript function/component
 * - last: TypeScript function/component
 * - UserAvatar: TypeScript function/component
 * - initials: TypeScript function/component
 * - TopBar: TypeScript function/component
 * - shell: TypeScript function/component
 * - cfg: TypeScript function/component
 * - brand: TypeScript function/component
 * - showKebab: TypeScript function/component
 * - showAvatar: TypeScript function/component
 * - chromeMode: TypeScript function/component
 *
 * SOURCE AVAILABLE ON REQUEST
 * Contact: Dave Eichler — linkedin.com/in/daaaave-atx
 */

// This file is a stub. See README.md for full source access.
