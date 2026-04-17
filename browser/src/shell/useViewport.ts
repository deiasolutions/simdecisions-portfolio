/**
 * useViewport
 *
 * * useViewport.ts — Centralized viewport & orientation detection for the Stage.
 *
 * Single source of truth for breakpoint + orientation. Shell.tsx owns the instance
 * and exposes it on ShellCtx so all children read from one place.
 *
 * Breakpoints (matches chromeMode mapping):
 *   mobile:  < 600px  → immersive
 *   tablet:  600–1023 → compact
 *   desktop: >= 1024  → full
 *
 * Uses matchMedia (event-driven, no resize polling) and screen.orientation API.
 *
 * Dependencies:
 * - import { useState, useEffect, useMemo } from 'react';
 * - import { BREAKPOINT_TABLET, BREAKPOINT_DESKTOP } from './constants';
 *
 * Components/Functions:
 * - MQ_MOBILE: TypeScript function/component
 * - MQ_DESKTOP: TypeScript function/component
 * - getBreakpoint: TypeScript function/component
 * - getOrientation: TypeScript function/component
 * - buildState: TypeScript function/component
 * - useViewport: TypeScript function/component
 * - mobileMql: TypeScript function/component
 * - desktopMql: TypeScript function/component
 * - update: TypeScript function/component
 * - update: TypeScript function/component
 * - screenOrientation: TypeScript function/component
 *
 * SOURCE AVAILABLE ON REQUEST
 * Contact: Dave Eichler — linkedin.com/in/daaaave-atx
 */

// This file is a stub. See README.md for full source access.
