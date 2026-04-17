/**
 * FileOperations.test
 *
 * * FileOperations.test.tsx
 *
 * Tests for the file-operation layer used by the flow-designer dialogs.
 * Since @testing-library/react is not available, this file tests:
 *
 *  - SaveDialog logic:  serializeFlow + localStorage persistence
 *  - LoadDialog logic:  getRecentFlows (localStorage read) + deserializeFlow
 *  - ImportDialog logic: detectDialect + importDialect (dialect selection)
 *  - ExportDialog logic: format modes, share-link generation, YAML/JSON preview
 *  - API adapter mock pattern
 *
 * All tests are pure-function / environment tests with no React rendering.
 *
 * Dependencies:
 * - import { describe, it, expect, vi, beforeEach, afterEach } from "vitest";
 * - import {
 * - import type { PhaseFlow } from "../file-ops/serialization";
 * - import {
 * - import { listAutosavedFlows } from "../file-ops/useAutoSave";
 *
 * Components/Functions:
 * - APIError: TypeScript class
 * - mockClient: TypeScript function/component
 * - FIXED_NOW: TypeScript function/component
 * - makeSampleFlow: TypeScript function/component
 * - localStorageMock: TypeScript function/component
 * - flow: TypeScript function/component
 * - yaml: TypeScript function/component
 * - flow: TypeScript function/component
 * - yaml: TypeScript function/component
 * - index: TypeScript function/component
 * - storedIndex: TypeScript function/component
 * - flow: TypeScript function/component
 * - trimmedName: TypeScript function/component
 * - original: TypeScript function/component
 * - copy: TypeScript function/component
 *
 * SOURCE AVAILABLE ON REQUEST
 * Contact: Dave Eichler — linkedin.com/in/daaaave-atx
 */

// This file is a stub. See README.md for full source access.
