/**
 * messageBus
 *
 * * messageBus.ts — React context and in-memory message bus with governance
 * Ported from simdecisions-2/src/components/shell/shell.context.js
 *
 * IR routing: MessageBus gains setLastFocusedByAppType() and getLastFocusedPane()
 * so TerminalApp can resolve the correct canvas target without accessing React state.
 *
 * Mute enforcement: MessageBus enforces mute levels during send():
 * - 'none': all messages delivered
 * - 'notifications': notification-type messages blocked
 * - 'inbound': all incoming messages to pane blocked
 * - 'outbound': all outgoing messages from pane blocked
 * - 'full': all messages to/from pane blocked
 * Platform invariants (relay_bus, ledger_writer, gate_enforcer) bypass mute.
 *
 * Context value includes mode engine state:
 * @typedef {Object} ShellContext
 * @property {string|null} activeMode - current mode ID or null
 * @property {import('./types/messages').ModeDefinition|null} activeModeDefinition - current mode definition or null
 * @property {Array<{id: string, label: string, icon?: string, active?: boolean}>|undefined} tabs - tabs from egg config
 * @property {Record<string, any>|undefined} settings - EGG-level settings config
 *
 * Context Advertisement Message
 *
 * Published by any applet when it becomes focused.
 * Layout applets (contextual drawers, toolbars, status strips) subscribe and adapt.
 *
 * Message shape:
 * {
 *   type: "context_advertisement",
 *   fromPaneId: string,
 *   target: "*",
 *   appType: string,
 *   offers: {
 *     toolbar?: string,     // Key into drawer's toolbar registry
 *     properties?: string,  // Key into drawer's properties registry
 *     statusBar?: string,   // Key into status bar content registry
 *   }
 * }
 *
 * Rules:
 * - Last-focused applet wins if multiple advertise simultaneously
 * - Drawers have fallback contents for when nothing is advertising
 * - Cross-fade transition: 150ms
 *
 * Dependencies:
 * - import { createContext, useContext } from 'react'
 * - import type { MessageEnvelope } from './types/messages'
 * - import type { MuteLevel } from './constants'
 *
 * Components/Functions:
 * - MessageBus: TypeScript class
 * - uid: TypeScript function/component
 * - nodeId: TypeScript function/component
 * - node: TypeScript function/component
 * - nonce: TypeScript function/component
 * - env: TypeScript function/component
 * - platformInvariants: TypeScript function/component
 * - isPlatformInvariant: TypeScript function/component
 * - sourceMute: TypeScript function/component
 * - targetMute: TypeScript function/component
 * - targetMute: TypeScript function/component
 * - typeListeners: TypeScript function/component
 * - set: TypeScript function/component
 * - listeners: TypeScript function/component
 * - env: TypeScript function/component
 *
 * SOURCE AVAILABLE ON REQUEST
 * Contact: Dave Eichler — linkedin.com/in/daaaave-atx
 */

// This file is a stub. See README.md for full source access.
