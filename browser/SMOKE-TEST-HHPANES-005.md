# SMOKE TEST: SPEC-HHPANES-005 — Three Currencies Visibility Toggle

## Test Environment
- Browser: Chrome/Firefox/Safari
- URL: http://localhost:5173?set=default (or any set with TopBar)

## Pre-Test Setup
1. Clear localStorage: `localStorage.clear()` in browser console
2. Reload page

## Test Cases

### TC-1: Default Behavior (3Cs visible in top-menu)

**Steps:**
1. Load app at http://localhost:5173
2. Look at TopBar component (top of screen)

**Expected:**
- ✅ TopBar shows currency chip with three currencies (⏱ CLOCK, 💰 COIN, 🌿 CARBON)
- ✅ Default values shown: `0.0s`, `$0.00`, `0.0g`
- ✅ Currency chip is clickable

**Pass Criteria:**
Currency chip is visible and displays all three currencies.

---

### TC-2: Setting Change to Hidden

**Steps:**
1. Open browser console
2. Run: `import { setThreeCsVisibility } from './src/primitives/settings/settingsStore.ts'; setThreeCsVisibility('hidden')`
3. OR open Settings via kebab menu and change 3Cs visibility to "Hidden"
4. Wait 1 second (for storage event propagation)

**Expected:**
- ✅ Currency chip disappears immediately
- ✅ TopBar still renders (hamburger, brand, kebab, avatar remain)
- ✅ No page reload required

**Pass Criteria:**
3Cs chip is no longer visible in TopBar.

---

### TC-3: Setting Change to Top-Menu (restore)

**Steps:**
1. In browser console, run:
   ```javascript
   import { setThreeCsVisibility } from './src/primitives/settings/settingsStore.ts'
   setThreeCsVisibility('top-menu')
   ```
2. Wait 1 second

**Expected:**
- ✅ Currency chip reappears immediately
- ✅ Values preserved if any RTD events were emitted
- ✅ No page reload required

**Pass Criteria:**
3Cs chip is visible again in TopBar.

---

### TC-4: RTD Events Update Display

**Steps:**
1. Ensure 3Cs visibility is 'top-menu'
2. Open browser console
3. Get the message bus instance:
   ```javascript
   // Assuming you have access to shell context
   const bus = window.__shell_context?.bus
   ```
4. Emit RTD event:
   ```javascript
   bus.send({
     type: 'RTD',
     target: '*',
     data: {
       service_id: 'test',
       metric_key: 'cost_coin',
       value: 1.23,
       unit: 'USD',
       currency: 'COIN',
       timestamp: new Date().toISOString()
     }
   })
   ```

**Expected:**
- ✅ COIN value updates to `$1.23`
- ✅ Other currencies remain at default
- ✅ Update is immediate (no reload)

**Pass Criteria:**
RTD event updates the displayed currency value.

---

### TC-5: Click to Expand

**Steps:**
1. Ensure 3Cs visibility is 'top-menu'
2. Click on the currency chip

**Expected:**
- ✅ Chip expands (CSS class 'expanded' is added)
- ✅ Visual change occurs (padding/spacing increases)
- ✅ Click again collapses it back

**Pass Criteria:**
Currency chip toggles between collapsed and expanded states.

---

### TC-6: Persistence Across Reload

**Steps:**
1. Set visibility to 'hidden'
2. Reload the page (F5 or Ctrl+R)
3. Check TopBar

**Expected:**
- ✅ 3Cs chip remains hidden after reload
- ✅ Setting persists in localStorage

**Pass Criteria:**
Hidden state persists across page reload.

---

### TC-7: No Hardcoded Colors

**Steps:**
1. Inspect currency chip element in DevTools
2. Check inline styles and CSS

**Expected:**
- ✅ No hex colors (#...)
- ✅ No rgb/rgba values
- ✅ All colors use `var(--sd-*)` CSS variables

**Pass Criteria:**
All styling uses CSS variables only.

---

## Post-Test Cleanup

Run in console:
```javascript
localStorage.clear()
location.reload()
```

---

## Test Results Template

| Test Case | Status | Notes |
|-----------|--------|-------|
| TC-1: Default Behavior | ⬜ PASS / ⬜ FAIL | |
| TC-2: Hide 3Cs | ⬜ PASS / ⬜ FAIL | |
| TC-3: Restore 3Cs | ⬜ PASS / ⬜ FAIL | |
| TC-4: RTD Events | ⬜ PASS / ⬜ FAIL | |
| TC-5: Expand/Collapse | ⬜ PASS / ⬜ FAIL | |
| TC-6: Persistence | ⬜ PASS / ⬜ FAIL | |
| TC-7: No Hardcoded Colors | ⬜ PASS / ⬜ FAIL | |

**Overall:** ⬜ PASS / ⬜ FAIL

**Tested By:** ___________________
**Date:** ___________________
**Browser:** ___________________
