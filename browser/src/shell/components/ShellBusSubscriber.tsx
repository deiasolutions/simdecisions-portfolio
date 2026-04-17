/**
 * ShellBusSubscriber
 *
 * * ShellBusSubscriber.tsx — Converts bus messages to reducer dispatches
 *
 * Chrome primitives emit bus messages (shell:action-requested, command:execute).
 * This subscriber listens and converts them to reducer dispatches.
 * Keeps primitives decoupled from the shell reducer.
 *
 * Dependencies:
 * - import { useEffect } from 'react';
 * - import type { MessageBus } from '../../infrastructure/relay_bus';
 * - import { BUS_MESSAGE_TYPES } from '../../infrastructure/relay_bus/constants';
 * - import { useCommandRegistry } from '../../services/commands/commandRegistry';
 * - import type { ShellAction } from '../types';
 *
 * Components/Functions:
 * - ALLOWED_SHELL_ACTIONS: TypeScript function/component
 * - ShellBusSubscriber: TypeScript function/component
 * - commandRegistry: TypeScript function/component
 * - unsubShellAction: TypeScript function/component
 * - actionType: TypeScript function/component
 * - unsubCommand: TypeScript function/component
 *
 * SOURCE AVAILABLE ON REQUEST
 * Contact: Dave Eichler — linkedin.com/in/daaaave-atx
 */

// This file is a stub. See README.md for full source access.
