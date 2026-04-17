# SPEC-FACTORY-002: Register Factory Primitives in App Registry

**MODE: EXECUTE**

**Spec ID:** SPEC-FACTORY-002
**Created:** 2026-04-09
**Author:** Q88N
**Type:** INTEGRATION
**Status:** READY
**Wave:** 1 (no dependencies)

---

## Priority
P0

## Depends On
None

## Model Assignment
haiku

## Purpose

Register `queue-pane` and `notification-pane` in the app registry so they can be instantiated by EGG configs. These primitives already exist and work — they just aren't registered as app types.

**Deliverable:** 2 adapter files + registry updates (~80 lines total)

---

## Current State

The primitives exist:
- `browser/src/primitives/queue-pane/QueuePane.tsx` (906 lines, complete)
- `browser/src/primitives/notification-pane/NotificationPane.tsx` (369 lines, complete)

But they're not in the app registry:
- `browser/src/apps/index.ts` — missing `registerApp()` calls for these

---

## Implementation

### File 1: `browser/src/apps/queuePaneAdapter.tsx`

```tsx
/**
 * Queue Pane App Adapter
 * Wraps QueuePane primitive for EGG instantiation
 */

import React from 'react';
import { QueuePane } from '../primitives/queue-pane/QueuePane';
import type { AppAdapterProps } from './types';

export function QueuePaneAdapter({ config }: AppAdapterProps) {
  return (
    <QueuePane
      autoRefresh={config?.autoRefresh ?? true}
      refreshInterval={config?.refreshInterval ?? 10000}
      showFilters={config?.showFilters ?? true}
      sections={config?.sections ?? ['active', 'queued', 'complete', 'failed']}
    />
  );
}

export const queuePaneAppConfig = {
  appType: 'queue-pane',
  label: 'Queue',
  icon: 'list-checks',
  component: QueuePaneAdapter,
};
```

### File 2: `browser/src/apps/notificationPaneAdapter.tsx`

```tsx
/**
 * Notification Pane App Adapter
 * Wraps NotificationPane primitive for EGG instantiation
 */

import React from 'react';
import { NotificationPane } from '../primitives/notification-pane/NotificationPane';
import type { AppAdapterProps } from './types';

export function NotificationPaneAdapter({ config }: AppAdapterProps) {
  return (
    <NotificationPane
      filter={config?.filter ?? 'all'}
      autoRefresh={config?.autoRefresh ?? true}
      swipeActions={config?.swipeActions ?? true}
    />
  );
}

export const notificationPaneAppConfig = {
  appType: 'notification-pane',
  label: 'Notifications',
  icon: 'bell',
  component: NotificationPaneAdapter,
};
```

### File 3: Modify `browser/src/apps/index.ts`

Add imports and registration:

```tsx
// Add imports
import { queuePaneAppConfig } from './queuePaneAdapter';
import { notificationPaneAppConfig } from './notificationPaneAdapter';

// Add to registerApps() or APP_REGISTRY array
registerApp(queuePaneAppConfig);
registerApp(notificationPaneAppConfig);
```

---

## File Targets

| File | Action | Lines |
|------|--------|-------|
| `browser/src/apps/queuePaneAdapter.tsx` | CREATE | ~30 |
| `browser/src/apps/notificationPaneAdapter.tsx` | CREATE | ~30 |
| `browser/src/apps/index.ts` | MODIFY | +6 |

---

## Reference Files

Read before implementation:
- `browser/src/apps/progressAdapter.tsx` — pattern to follow
- `browser/src/apps/index.ts` — where to register
- `browser/src/apps/types.ts` — AppAdapterProps interface
- `browser/src/primitives/queue-pane/QueuePane.tsx` — props to pass
- `browser/src/primitives/notification-pane/NotificationPane.tsx` — props to pass

---

## Acceptance Criteria

- [ ] `queuePaneAdapter.tsx` exists and exports `queuePaneAppConfig`
- [ ] `notificationPaneAdapter.tsx` exists and exports `notificationPaneAppConfig`
- [ ] Both registered in `apps/index.ts`
- [ ] `queue-pane` instantiates via EGG config without errors
- [ ] `notification-pane` instantiates via EGG config without errors
- [ ] TypeScript compiles without errors
- [ ] Existing app registrations not broken

## Smoke Test

```bash
# Files exist
test -f browser/src/apps/queuePaneAdapter.tsx && echo "Queue adapter exists" || echo "MISSING"
test -f browser/src/apps/notificationPaneAdapter.tsx && echo "Notification adapter exists" || echo "MISSING"

# TypeScript compiles
cd browser && npx tsc --noEmit && echo "TS OK" || echo "TS ERRORS"

# Registry check
grep -q "queue-pane" browser/src/apps/index.ts && echo "Registered" || echo "NOT REGISTERED"
```

## Constraints

- Follow existing adapter pattern exactly (see `progressAdapter.tsx`)
- No changes to primitive components themselves
- Props passed through from EGG config
- All files under 50 lines

## Response File

`.deia/hive/responses/20260409-FACTORY-002-RESPONSE.md`

---

*SPEC-FACTORY-002 — Q88N — 2026-04-09*
