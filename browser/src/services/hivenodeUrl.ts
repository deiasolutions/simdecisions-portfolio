/**
 * hivenodeUrl
 *
 * * hivenodeUrl.ts — Single source of truth for the hivenode base URL.
 *
 * In production (non-localhost), returns "" so fetch() uses same-origin
 * relative paths, which Vercel rewrites proxy to Railway.
 *
 * In dev (localhost), returns "http://localhost:8420" for direct access.
 *
 * If VITE_HIVENODE_URL is explicitly set, always uses that value.
 *
 * Dependencies:
 * - (see source)
 *
 * Components/Functions:
 * - envUrl: TypeScript function/component
 * - resolveHivenodeUrl: TypeScript function/component
 * - HIVENODE_URL: TypeScript function/component
 *
 * SOURCE AVAILABLE ON REQUEST
 * Contact: Dave Eichler — linkedin.com/in/daaaave-atx
 */

// This file is a stub. See README.md for full source access.
