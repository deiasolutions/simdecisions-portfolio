# Settings Backend Persistence — Manual Smoke Tests
## SPEC-HHPANES-003

These manual tests verify the settings persistence round-trip works correctly.

## Prerequisites
- Hivenode running at http://localhost:8420
- Browser dev server running at http://localhost:5173
- Browser devtools console open

## Test 1: Save triggers API call to backend

1. Open browser to http://localhost:5173
2. Open Settings panel
3. Change a setting (e.g., toggle voice enabled, or change default model)
4. Open browser Network tab
5. **VERIFY:** See POST/PUT request to `/api/user/preferences`
6. **VERIFY:** Request succeeds with 200 OK

## Test 2: Settings load from backend on app init

### Setup
1. Save some settings via Settings panel (creates backend record)
2. Note the current settings values

### Test
1. Clear localStorage: `localStorage.clear()` in console
2. Reload page
3. Open Settings panel
4. **VERIFY:** Settings match what was saved earlier (loaded from backend)
5. **VERIFY:** Console shows no errors

## Test 3: Offline fallback

### Setup
1. Save some settings
2. Note the current values

### Test
1. Stop hivenode: kill the uvicorn process
2. Change a setting in the UI
3. **VERIFY:** Setting saves to localStorage (check via `localStorage.getItem('sd_user_settings')`)
4. **VERIFY:** Console shows warning about backend save failing
5. **VERIFY:** `localStorage.getItem('sd_settings_sync_pending')` returns "true"
6. Restart hivenode
7. Trigger a settings change (or dispatch 'online' event manually)
8. **VERIFY:** Pending settings sync to backend
9. **VERIFY:** `localStorage.getItem('sd_settings_sync_pending')` returns null

## Test 4: Conflict resolution (last-write-wins)

### Setup
1. Save settings with updatedAt: 2026-04-14T10:00:00Z (older)
2. Mock backend to return settings with updatedAt: 2026-04-14T12:00:00Z (newer)

### Test
1. Call `loadSettingsFromBackend()` in console
2. **VERIFY:** Backend settings (newer) win and overwrite localStorage
3. **VERIFY:** Settings UI reflects backend values

## Test 5: Cross-device persistence

### Setup
1. Use two browser windows/profiles (simulate two devices)

### Test
1. In Window A: Change a setting and save
2. In Window B: Reload page
3. **VERIFY:** Window B shows the setting changed in Window A
4. **VERIFY:** Both windows have same settings

## Test 6: Partial update (patch semantics)

1. Set multiple settings (e.g., API key + model + voice settings)
2. Change only one setting (e.g., voice_auto_read)
3. Check Network tab request payload
4. **VERIFY:** Request body contains only the changed fields (patch), not full settings object
5. **VERIFY:** Other settings remain unchanged after save

---

## Expected Behavior Summary

- ✅ Every settings save triggers backend API call
- ✅ Settings load from backend on app init
- ✅ Offline fallback: localStorage cache used if backend unreachable
- ✅ Sync on reconnect: pending settings pushed to backend
- ✅ Last-write-wins conflict resolution (server timestamp wins)
- ✅ All existing settings tests still pass
- ✅ Partial updates work (patch semantics)
