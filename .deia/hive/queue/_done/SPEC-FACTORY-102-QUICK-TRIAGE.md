# SPEC-FACTORY-102: Quick Triage Flow

**MODE: EXECUTE**

**Spec ID:** SPEC-FACTORY-102
**Created:** 2026-04-09
**Author:** Q88N
**Type:** FEATURE
**Status:** READY
**Phase:** P1

---

## Priority
P1

## Depends On
- SPEC-FACTORY-101 (Fr4nk factory context)
- SPEC-FACTORY-003 (response-browser)

## Model Assignment
haiku

## Purpose

Enable quick triage workflow: read response → create follow-up task in one fluid motion. When reviewing a response that needs follow-up work, tap [Follow-up] to pre-fill a spec with context from the response.

**Deliverable:** Triage flow integration (~100 lines)

---

## User Flow

```
1. Open Response Browser
2. Tap a response to view full content
3. Notice an issue or needed improvement
4. Tap [Create Follow-up] button
5. Spec form opens pre-filled with:
   - Title: "Follow-up: {original task title}"
   - Depends On: {original task ID}
   - Description: includes excerpt from response
6. Edit as needed, submit
7. New spec in backlog, linked to original
```

---

## Implementation

### 1. Add Follow-up Button to Response Viewer

In `ResponseBrowser.tsx` full-view modal:

```tsx
<button 
  className="hhp-btn hhp-btn-secondary"
  onClick={() => handleCreateFollowup(response)}
>
  Create Follow-up
</button>
```

### 2. Handle Follow-up Creation

```typescript
const handleCreateFollowup = (response: ResponseItem) => {
  // Extract context from response
  const context = {
    parentTaskId: response.taskId,
    parentResponseId: response.id,
    excerpt: response.excerpt,
    model: response.model,
  };
  
  // Emit bus event to open spec-submit with pre-fill
  messageBus.publish('factory:open-spec-submit', {
    prefill: {
      title: `Follow-up: ${response.taskId}`,
      dependsOn: [response.taskId],
      description: buildFollowupDescription(context),
      type: 'feature', // default, user can change
    },
  });
};

const buildFollowupDescription = (context: FollowupContext): string => {
  return `## Context

This task follows up on ${context.parentTaskId}.

**From response ${context.parentResponseId}:**
> ${context.excerpt}

## Purpose

<!-- Describe what needs to be done -->

## Acceptance Criteria

- [ ] 
`;
};
```

### 3. Update Spec Submit to Accept Prefill

In `SpecSubmitForm.tsx`:

```typescript
interface SpecSubmitFormProps {
  prefill?: Partial<SpecSubmission>;
  onClose: () => void;
}

export function SpecSubmitForm({ prefill, onClose }: SpecSubmitFormProps) {
  const [formData, setFormData] = useState<SpecSubmission>({
    title: prefill?.title ?? '',
    type: prefill?.type ?? 'feature',
    priority: prefill?.priority ?? 'P1',
    model: prefill?.model ?? 'sonnet',
    description: prefill?.description ?? '',
    dependsOn: prefill?.dependsOn ?? [],
  });
  
  // ... rest of form
}
```

### 4. Update Bus Event Handler

In component that renders SpecSubmitForm:

```typescript
useEffect(() => {
  const unsub = messageBus.subscribe('factory:open-spec-submit', (payload) => {
    setShowSpecSubmit(true);
    setPrefillData(payload?.prefill ?? null);
  });
  return unsub;
}, []);
```

---

## Fr4nk Integration

Fr4nk can also trigger follow-ups via voice:

**User:** "Create a follow-up for the last response"
**Fr4nk:** [calls response_list to get latest] "Got it. Creating follow-up for TASK-127. What's the issue?"
**User:** "The SSE reconnect still drops on mobile"
**Fr4nk:** [calls task_create with pre-filled data] "Created SPEC-BUG-SSE-MOBILE-001. Priority P1, assigned to Sonnet. [Edit] [Submit]"

Add to Fr4nk's factory prompt:

```markdown
## Follow-up Flow

When user says "follow up on X" or "create follow-up":
1. Call response_list or task_read to get context
2. Ask what needs to happen (if not stated)
3. Call task_create with:
   - dependsOn: [original task ID]
   - description: includes context from original
4. Confirm before submitting
```

---

## File Targets

| File | Action | Lines |
|------|--------|-------|
| `browser/src/primitives/response-browser/ResponseBrowser.tsx` | MODIFY | +30 |
| `browser/src/primitives/spec-submit/SpecSubmitForm.tsx` | MODIFY | +20 |
| `browser/src/services/frank/prompts/factory.md` | MODIFY | +15 |

---

## Reference Files

Read before implementation:
- `browser/src/primitives/response-browser/ResponseBrowser.tsx`
- `browser/src/primitives/spec-submit/SpecSubmitForm.tsx`
- `browser/src/services/frank/prompts/factory.md`

---

## Acceptance Criteria

- [ ] Response viewer has [Create Follow-up] button
- [ ] Clicking opens spec-submit with pre-filled data
- [ ] Title pre-filled as "Follow-up: {task ID}"
- [ ] Depends On pre-filled with original task ID
- [ ] Description includes context excerpt
- [ ] Fr4nk can create follow-ups via voice/chat
- [ ] Submitted follow-up appears in backlog

## Smoke Test

```bash
# Manual test:
# 1. Open response browser
# 2. Tap a response
# 3. Tap [Create Follow-up]
# 4. Verify form opens with pre-filled data
# 5. Submit and verify file in backlog
```

## Constraints

- No new components — extend existing
- Pre-fill is a convenience, all fields editable
- Linked via dependsOn, not custom field

## Response File

`.deia/hive/responses/20260409-FACTORY-102-RESPONSE.md`

---

*SPEC-FACTORY-102 — Q88N — 2026-04-09*
