/**
 * diffCommands
 *
 * * diffCommands.ts — Parse terminal diff commands into TextOps
 *
 * Supports shorthand diff syntax for code mode:
 *   -N        delete line N
 *   -N-M      delete lines N through M
 *   +N text   insert text after line N
 *   =N text   replace line N with text
 *
 * Returns null if input doesn't match a diff pattern (falls through to LLM).
 *
 * Dependencies:
 * - import type { TextOp } from './textOps'
 *
 * Components/Functions:
 * - DELETE_SINGLE_RE: TypeScript function/component
 * - DELETE_RANGE_RE: TypeScript function/component
 * - INSERT_RE: TypeScript function/component
 * - REPLACE_RE: TypeScript function/component
 * - parseDiffCommand: TypeScript function/component
 * - trimmed: TypeScript function/component
 * - n: TypeScript function/component
 * - calcDiffStats: TypeScript function/component
 * - op: TypeScript function/component
 *
 * SOURCE AVAILABLE ON REQUEST
 * Contact: Dave Eichler — linkedin.com/in/daaaave-atx
 */

// This file is a stub. See README.md for full source access.
