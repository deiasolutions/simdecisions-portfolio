/**
 * LoginPage
 *
 * * LoginPage.tsx — GitHub OAuth and dev-login authentication interface
 *
 * Props:
 * - onAuthSuccess: (token: string, user: {id, email, display_name}) => void
 *
 * State:
 * - stage: "consent" (show login UI) | "loading" (spinner, redirecting to GitHub)
 * - devAvailable: true if /dev-login/available returns {available: true}
 * - devLoading: true while POST /dev-login is in flight
 *
 * On mount: fetch hodeia.me /dev-login/available to decide whether to show dev-login button
 * GitHub button: fetch /auth/github/login, redirect to returned URL
 * Dev-login button: POST /dev-login, call onAuthSuccess with token + user
 *
 * Styling: var(--sd-*) CSS variables ONLY, no hardcoded colors
 *
 * Dependencies:
 * - import { useState, useEffect } from 'react'
 * - import { base64UrlDecode } from './authStore'
 * - import './LoginPage.css'
 *
 * Components/Functions:
 * - API_BASE: TypeScript function/component
 * - decodeJwtPayload: TypeScript function/component
 * - parts: TypeScript function/component
 * - payload: TypeScript function/component
 * - LoginPage: TypeScript function/component
 * - params: TypeScript function/component
 * - token: TypeScript function/component
 * - error: TypeScript function/component
 * - payload: TypeScript function/component
 * - user: TypeScript function/component
 * - handleGitHubLogin: TypeScript function/component
 * - origin: TypeScript function/component
 * - handleDevLogin: TypeScript function/component
 *
 * SOURCE AVAILABLE ON REQUEST
 * Contact: Dave Eichler — linkedin.com/in/daaaave-atx
 */

// This file is a stub. See README.md for full source access.
