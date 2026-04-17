# Q33N Coordination Report: TASK-244 Landing Page

**Date:** 2026-03-17
**Briefing Source:** `2026-03-17-BRIEFING-TASK-244-landing-page.md`
**Status:** Task file written, awaiting Q33NR review

---

## Summary

I have written one task file for implementing the ShiftCenter landing page (Wave 5 Ship). The landing page will be a standalone React component that renders when users visit the root URL (`/`) without an `?egg=` parameter, serving as the "front door" for new users.

---

## Task File Created

### TASK-244: Landing Page

**Path:** `.deia/hive/tasks/2026-03-17-TASK-244-landing-page.md`

**Objective:** Create a landing page for ShiftCenter that explains what the product does, shows a screenshot placeholder, presents three feature cards, and provides CTAs for sign-up and demo.

**Model Assignment:** Sonnet (front-end UI work with routing logic and responsive design)

**Estimated Effort:** 2 hours

**Deliverables:**
1. **New React Component:** `browser/src/pages/LandingPage.tsx` (~250 lines)
   - Hero section with title "ShiftCenter" and tagline
   - Screenshot placeholder (styled div)
   - Three feature cards: Governed Agents, Constitutional Framework, Simulation Before Execution
   - Primary CTA: "Get Started" → links to ra96it sign-up
   - Secondary CTA: "Try the demo" → links to `?egg=canvas`
   - Footer: "Built by DEIA Solutions" with link

2. **CSS File:** `browser/src/pages/LandingPage.css` (~200 lines)
   - All colors via `var(--sd-*)` variables (Rule 3)
   - Responsive design (mobile, tablet, desktop)
   - Hover animations (subtle)

3. **Routing Logic Update:** `browser/src/App.tsx` (~10 lines)
   - Add conditional logic: if URL is `/` without `?egg=`, render `<LandingPage />`
   - Otherwise, continue with EGG system
   - Preserves existing behavior for all EGG routes

4. **Tests:** `browser/src/pages/__tests__/LandingPage.test.tsx` (~150 lines, minimum 12 tests)
   - Component rendering tests (hero, feature cards, CTAs, footer)
   - Link verification (CTA URLs, demo link, footer link)
   - CSS validation (no hardcoded colors)
   - App.tsx integration tests (landing page vs EGG routing)

**Test Command:**
```bash
cd browser && npx vitest run src/pages/__tests__/LandingPage.test.tsx
```

**Acceptance Criteria:** 9 items (all deliverables, tests passing, no hardcoded colors, responsive design)

---

## Key Design Decisions

### 1. Landing Page as Standalone Component (Not an EGG)

The landing page is NOT an EGG — it's a standalone React component that renders **before** the EGG system. This is the simplest approach:
- No need to create a new EGG file
- No need to modify EGG resolver logic
- Clean separation: marketing page vs application shell

### 2. Routing Logic in App.tsx

Added a `shouldShowLanding()` function in `App.tsx` that checks:
- Is the pathname `/` (root)?
- Is there NO `?egg=` parameter?

If both are true → render `<LandingPage />`
Otherwise → continue with EGG system

This preserves all existing EGG routing:
- `?egg=canvas` → loads canvas EGG
- `/efemera` → loads efemera EGG
- `chat.efemera.live` → loads chat EGG (hostname routing)

### 3. CTA Links

- **Primary CTA:** "Get Started"
  - Links to: `${VITE_RA96IT_API}/signup`
  - If `VITE_RA96IT_API` is empty (local dev), defaults to `/signup`

- **Secondary CTA:** "Try the demo"
  - Links to: `?egg=canvas`
  - Simplest demo EGG, shows the canvas immediately

### 4. Content Strategy

Kept content minimal and focused:
- **Tagline:** "Describe your process. Watch it build. Simulate it. See where it breaks." (action-oriented)
- **Three feature cards:** Benefits, not technical details
- **Screenshot placeholder:** No actual screenshot yet — just a styled div that says "Screenshot coming soon"

### 5. Responsive Design

Mobile-first approach:
- Feature cards: 3-column grid on desktop, 1-column on mobile
- Hero text: larger on desktop, smaller on mobile
- Spacing: tighter on mobile

### 6. Test Coverage

12+ tests covering:
- Component rendering (all sections present)
- Link verification (correct URLs)
- CSS validation (no hardcoded colors)
- Integration with App.tsx (routing logic)

---

## Files Referenced in Task

The bee must read these files first:
- `browser/src/App.tsx` — Root component (where routing logic will be added)
- `browser/src/eggs/eggResolver.ts` — EGG resolution logic
- `browser/src/primitives/auth/LoginPage.tsx` — Design reference
- `browser/src/primitives/auth/LoginPage.css` — CSS reference
- `browser/src/shell/shell-themes.css` — Theme variables

---

## Constraints Enforced

- ✅ Rule 3: NO hardcoded colors (all `var(--sd-*)`)
- ✅ Rule 4: No file over 500 lines (LandingPage.tsx ~250, CSS ~200, tests ~150)
- ✅ Rule 5: TDD — tests first, then implementation
- ✅ Rule 6: NO stubs — every function fully implemented
- ✅ Production-ready code (Wave 5 Ship)

---

## Estimated File Sizes

| File | Lines | Status |
|------|-------|--------|
| `LandingPage.tsx` | ~250 | New |
| `LandingPage.css` | ~200 | New |
| `LandingPage.test.tsx` | ~150 | New |
| `App.tsx` | +10 | Modified |
| **Total** | **~610** | **4 files** |

All files well under 500-line limit (Rule 4).

---

## Dependencies

- **VITE_RA96IT_API env var** — Used for sign-up CTA link. Already exists in codebase (used by LoginPage.tsx).
- **CSS theme variables** — Already defined in `shell-themes.css`. No new variables needed.
- **EGG system** — Landing page bypasses EGG system entirely, so no dependencies on EGG loader/resolver changes.

---

## Related Tasks

- **TASK-245:** ra96it sign-up flow (E2E test) — Sign-up link on landing page should be tested E2E
- **TASK-241:** Production URL smoke test — Should verify landing page loads on production
- **TASK-243:** Global Commons Phase A — Footer link to deiasolutions.org (future content)

---

## Risk Assessment

**Low risk:**
- Isolated change (new component, minimal routing logic)
- No dependencies on other in-flight tasks
- Preserves all existing EGG routing
- Well-tested (12+ tests)

**Potential issues:**
- **ENV VAR:** If `VITE_RA96IT_API` is misconfigured, sign-up link will break. Mitigation: Task includes tests for link href.
- **Mobile layout:** Feature cards might need adjustment on very small screens. Mitigation: Responsive design with tested breakpoints.

---

## Next Steps for Q33NR

1. **Review task file:** `.deia/hive/tasks/2026-03-17-TASK-244-landing-page.md`
2. **Check for:**
   - Missing deliverables
   - Vague acceptance criteria
   - Hardcoded colors (all should be `var(--sd-*)`)
   - Files that would exceed 500 lines (all are well under)
   - Missing test requirements
   - Imprecise file paths (all are absolute)
3. **If approved:** I will dispatch the bee with Sonnet model
4. **If corrections needed:** I will revise and return

---

## Q33N Notes

- This is a **Wave 5 Ship** task — production-ready code, not a prototype.
- The landing page is the "front door" for new users. It needs to be polished.
- Kept content minimal to avoid over-engineering (Rule 4: avoid over-engineering).
- Screenshot is a placeholder — actual screenshot will come later (out of scope for this task).
- Footer link to deiasolutions.org is a forward reference to TASK-243 (Global Commons Phase A).

---

**Status:** Awaiting Q33NR review and approval for dispatch.
