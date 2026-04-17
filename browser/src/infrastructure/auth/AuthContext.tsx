/**
 * AuthContext
 *
 * * AuthContext.tsx — Global auth state provider with hodeia.auth sync
 *
 * Provides auth state to all panes via React context and MessageBus.
 * Syncs with hodeia.auth via localStorage events (cross-tab) and state polling.
 * Broadcasts auth changes to all mounted panes within 100ms.
 *
 * Events broadcast via MessageBus:
 * - auth_state_changed: { isAuthenticated: boolean, user: AuthUser | null }
 *
 * Storage keys:
 * - hodeia_token: JWT access token
 * - hodeia_refresh_token: refresh token
 * - hodeia_user: user object JSON
 *
 * Dependencies:
 * - import { createContext, useContext, useState, useEffect, useCallback, type ReactNode } from 'react'
 * - import { getToken, getUser, isAuthenticated, clearToken, type AuthUser } from '../../primitives/auth/authStore'
 * - import type { MessageBus } from '../relay_bus'
 *
 * Components/Functions:
 * - AuthContext: TypeScript function/component
 * - AuthProvider: TypeScript function/component
 * - refresh: TypeScript function/component
 * - newState: TypeScript function/component
 * - changed: TypeScript function/component
 * - logout: TypeScript function/component
 * - handleStorageChange: TypeScript function/component
 * - interval: TypeScript function/component
 * - value: TypeScript function/component
 * - useAuth: TypeScript function/component
 * - context: TypeScript function/component
 *
 * SOURCE AVAILABLE ON REQUEST
 * Contact: Dave Eichler — linkedin.com/in/daaaave-atx
 */

// This file is a stub. See README.md for full source access.
