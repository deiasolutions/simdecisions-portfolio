/**
 * App.shouldShowLanding.test
 *
 * * App.shouldShowLanding.test.tsx — TDD tests for shouldShowLanding() function
 *
 * Tests the logic that determines when the ShiftCenter LandingPage should be shown.
 * Should NOT show landing when:
 * - Hostname is hodeia.me (or www.hodeia.me) or legacy ra96it.com
 * - User is authenticated (has valid JWT)
 * - ?egg= param is present
 *
 * Should show landing only when:
 * - Root path (/), no ?egg= param, not authenticated, not identity domain
 *
 * Dependencies:
 * - import { describe, it, expect, beforeEach, afterEach, vi } from 'vitest'
 *
 * Components/Functions:
 * - by: TypeScript function/component
 * - mockLocation: TypeScript function/component
 * - original: TypeScript function/component
 * - mockAuthToken: TypeScript function/component
 * - shouldShowLandingTestImpl: TypeScript function/component
 * - params: TypeScript function/component
 * - hasEggParam: TypeScript function/component
 * - isRootPath: TypeScript function/component
 * - identityDomains: TypeScript function/component
 * - result: TypeScript function/component
 * - result: TypeScript function/component
 * - result: TypeScript function/component
 * - result: TypeScript function/component
 * - result: TypeScript function/component
 * - result: TypeScript function/component
 *
 * SOURCE AVAILABLE ON REQUEST
 * Contact: Dave Eichler — linkedin.com/in/daaaave-atx
 */

// This file is a stub. See README.md for full source access.
