/**
 * SetupWizard
 *
 * * SetupWizard.tsx — 3-step post-login setup modal.
 *
 * Steps:
 *   1. Confirm display name
 *   2. Add phone + verify SMS 2FA (optional)
 *   3. Add recovery email + verify (optional)
 *
 * All steps are skippable. On finish (or skip-all), calls
 * POST /profile/complete-setup and updates the JWT.
 *
 * Dependencies:
 * - import { useState, useEffect } from 'react'
 * - import { getToken, setToken } from './authStore'
 * - import type { UserProfile } from './setupDetector'
 * - import './SetupWizard.css'
 *
 * Components/Functions:
 * - API_BASE: TypeScript function/component
 * - SetupWizard: TypeScript function/component
 * - authHeaders: TypeScript function/component
 * - token: TypeScript function/component
 * - handleNameNext: TypeScript function/component
 * - handleSendPhoneCode: TypeScript function/component
 * - res: TypeScript function/component
 * - data: TypeScript function/component
 * - handleVerifyPhoneCode: TypeScript function/component
 * - res: TypeScript function/component
 * - data: TypeScript function/component
 * - handleSendEmailCode: TypeScript function/component
 * - res: TypeScript function/component
 * - data: TypeScript function/component
 * - handleVerifyEmailCode: TypeScript function/component
 *
 * SOURCE AVAILABLE ON REQUEST
 * Contact: Dave Eichler — linkedin.com/in/daaaave-atx
 */

// This file is a stub. See README.md for full source access.
