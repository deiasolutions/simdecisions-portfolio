/**
 * HodeiaAuth
 *
 * * HodeiaAuth.tsx — Basque signup/login page for hodeia.me
 *
 * Flow:
 * 1. Show OAuth buttons (GitHub + Google) + form fields below
 * 2. OAuth → authenticate → return with token → show profile completion
 * 3. Profile completion: alias + API key → submit → welcome page
 * 4. Welcome page: "Enter" → redirect to efemera.live?token=X
 *
 * Tuesday launch: OAuth only, no email/password. Basque UI.
 *
 * Dependencies:
 * - import { useState, useEffect } from 'react'
 * - import { getToken, getUser, setToken, setUser, base64UrlDecode } from '../primitives/auth/authStore'
 *
 * Components/Functions:
 * - API_BASE: TypeScript function/component
 * - EU: TypeScript function/component
 * - GitHubIcon: TypeScript function/component
 * - GoogleIcon: TypeScript function/component
 * - S: TypeScript function/component
 * - decodeJwtPayload: TypeScript function/component
 * - parts: TypeScript function/component
 * - HodeiaAuth: TypeScript function/component
 * - link: TypeScript function/component
 * - params: TypeScript function/component
 * - token: TypeScript function/component
 * - payload: TypeScript function/component
 * - user: TypeScript function/component
 * - newSearch: TypeScript function/component
 * - existingToken: TypeScript function/component
 *
 * SOURCE AVAILABLE ON REQUEST
 * Contact: Dave Eichler — linkedin.com/in/daaaave-atx
 */

// This file is a stub. See README.md for full source access.
