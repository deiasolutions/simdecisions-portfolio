/**
 * setupDetector
 *
 * * setupDetector.ts — Detect whether the current user needs post-login setup.
 *
 * Reads the `needs_setup` claim from the JWT stored in localStorage.
 * When the wizard is needed, fetches the full profile from hodeia_auth.
 * Session-scoped dismissal: once dismissed, won't show again in this tab.
 *
 * Dependencies:
 * - import { getToken, base64UrlDecode } from './authStore'
 *
 * Components/Functions:
 * - API_BASE: TypeScript function/component
 * - DISMISSED_KEY: TypeScript function/component
 * - tokenNeedsSetup: TypeScript function/component
 * - token: TypeScript function/component
 * - payload: TypeScript function/component
 * - isSetupDismissed: TypeScript function/component
 * - dismissSetup: TypeScript function/component
 * - shouldShowSetup: TypeScript function/component
 * - fetchProfile: TypeScript function/component
 * - token: TypeScript function/component
 * - res: TypeScript function/component
 *
 * SOURCE AVAILABLE ON REQUEST
 * Contact: Dave Eichler — linkedin.com/in/daaaave-atx
 */

// This file is a stub. See README.md for full source access.
