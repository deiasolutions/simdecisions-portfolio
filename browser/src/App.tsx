/**
 * App
 *
 * * App.tsx — Root component for ShiftCenter
 *
 * Resolves EGG, inflates layout, renders Shell.
 * Standalone pages (hodeia.guru landing) bypass the shell entirely.
 *
 * Initialization flow:
 * 0. extractTokenFromUrl() — intercept ?token= from OAuth callback (any EGG)
 * 1. resolveCurrentEgg() determines if this is a standalone page or shell EGG
 * 2. Standalone: render directly (no shell, no EGG loading)
 * 3. Shell EGG: useEggInit → load .egg.md → inflate → render Shell
 *
 * Dependencies:
 * - import { Shell } from './shell/components/Shell'
 * - import { INITIAL_STATE } from './shell/reducer'
 * - import { useEggInit, type EggUiConfig } from './shell/useEggInit'
 * - import { setToken, setUser, setRefreshToken, base64UrlDecode, claimDeviceData } from './primitives/auth/authStore'
 * - import { discoverHivenodeUrl } from './services/hivenodeDiscovery'
 * - import { resolveCurrentEgg } from './sets/eggResolver'
 * - import { SimDecisionsLanding } from './pages/SimDecisionsLanding'
 * - import { HodeiaAuth } from './pages/HodeiaAuth'
 * - import { Portfolio } from './pages/Portfolio'
 * - import { AuthGate } from './shell/AuthGate'
 *
 * Components/Functions:
 * - STANDALONE_EGGS: TypeScript function/component
 * - applyBranding: TypeScript function/component
 * - h: TypeScript function/component
 * - brands: TypeScript function/component
 * - brand: TypeScript function/component
 * - link: TypeScript function/component
 * - extractTokenFromUrl: TypeScript function/component
 * - params: TypeScript function/component
 * - hash: TypeScript function/component
 * - hashParams: TypeScript function/component
 * - parts: TypeScript function/component
 * - payload: TypeScript function/component
 * - user: TypeScript function/component
 * - refreshToken: TypeScript function/component
 * - newSearch: TypeScript function/component
 *
 * SOURCE AVAILABLE ON REQUEST
 * Contact: Dave Eichler — linkedin.com/in/daaaave-atx
 */

// This file is a stub. See README.md for full source access.
