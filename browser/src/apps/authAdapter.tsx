/**
 * authAdapter
 *
 * * authAdapter.tsx — App registry adapter for auth primitive (LoginPage)
 *
 * Maps AppRendererProps to LoginPage props.
 * Wires LoginPage auth success callback to authStore persistence functions.
 * Updates pane title to display_name after login.
 * Shows SetupWizard after first login if JWT has needs_setup claim.
 *
 * Dependencies:
 * - import { useState, useEffect } from 'react'
 * - import { LoginPage, SetupWizard } from '../primitives/auth'
 * - import { setToken, setUser, isAuthenticated, getUser } from '../primitives/auth/authStore'
 * - import { shouldShowSetup, dismissSetup, fetchProfile } from '../primitives/auth/setupDetector'
 * - import type { UserProfile } from '../primitives/auth/setupDetector'
 * - import { useShell } from '../infrastructure/relay_bus'
 * - import type { AppRendererProps } from '../shell/components/appRegistry'
 *
 * Components/Functions:
 * - AuthAdapter: TypeScript function/component
 * - shell: TypeScript function/component
 * - updateAuthState: TypeScript function/component
 * - user: TypeScript function/component
 * - handleAuthSuccess: TypeScript function/component
 * - handleWizardComplete: TypeScript function/component
 * - handleWizardDismiss: TypeScript function/component
 *
 * SOURCE AVAILABLE ON REQUEST
 * Contact: Dave Eichler — linkedin.com/in/daaaave-atx
 */

// This file is a stub. See README.md for full source access.
