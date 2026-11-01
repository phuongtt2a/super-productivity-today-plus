# Today+ Working Now and Order — v1.3.0-beta.1 QA

**Status:** preview branch only. Do not merge or publish as stable until real-host verification. GitHub CI runs DOM mocks and screenshots; these do not replace actual installed testing.

## Core order behavior

1. Open Today+. Open **Arrange** for Tasks and for Habits independently.
2. Move a task in the middle of the list to the top using **Move to top**, then test Up/Down and mouse/pointer drag.
3. Ensure grouped subtasks remain attached to their parent when the parent moves. Reorder two subtasks inside the same parent without detaching them.
4. Arrange at least 10 habits as a morning routine. Verify completion buttons and counters remain functional and no habit streaks are changed by reordering.
5. Reopen Today+, refresh, switch away and back, restart the app. Verify task and habit order are restored from plugin-synced preferences.
6. On the next logical day, task order resets while the preferred habit order stays. Verify newly added and removed tasks/habits do not break ordering.
7. Verify **Overdue** and **Finished** filters work when a task is pinned or newly done. Verify native project task order is unchanged.
8. If multiple devices are synced, check whether a change appears after the receiving device has refreshed or reopened the plugin. Do not claim immediate cross-device delivery without a provider sync.

## Working Now

1. Select a task through its target icon. Confirm **only one task** is in Working Now and the task is not duplicated in the list.
2. Select a different task and verify it replaces the former task; the former task returns to the list.
3. Select a task with subtasks and verify the entire group stays accessible and its subtasks can be completed.
4. Test selecting a subtask. Verify the parent remains in Tasks while the selected subtask moves to Working Now.
5. Remove the selected task. Verify it returns to Tasks **without stopping native tracking**.
6. Complete the task or choose **Won't Do** from Working Now. Verify the native record is correct, the Working Zone becomes empty and overall progress is counted only once.
7. Test unfinished overdue, completed, deleted and rescheduled tasks after a restart. Invalid Working Now references must not surface ghost tasks.

## Native tracking and Focus

1. Selecting a task must **not** start tracking automatically.
2. Click Start tracking; verify Super Productivity tracks the correct task (for a parent, it may track the first unfinished subtask).
3. Click Stop tracking; verify the native timer stops and no duplicate elapsed-time counter exists in Today+.
4. Change tracked task from another Super Productivity view. Confirm the Working Now state updates through currentTaskChange when Today+ is active.
5. Restart Today+ during an active tracking session. The API does not provide a direct initial-current-tracker read; the interface must not pretend the tracker was confirmed until it receives a hook or explicitly starts it.
6. Click Focus mode. Verify it opens the application's native Focus interface and does **not** forcibly start a Pomodoro/Countdown session.
7. Test with an old host lacking the optional tracking or logical-day API: controls must disable/fallback safely.

## Visual, input and persistence quality

1. At 320px, 390px, tablet and desktop widths: no horizontal scroll, clipped text, or overlapped buttons.
2. Test with real mouse, touch (tap/drag), keyboard-only Tab/Enter/Space, screen reader labels.
3. Drag handles must not accidentally scroll the task instead of reordering, or prevent scrolling elsewhere.
4. Check light/dark themes, custom wallpaper transparency, native application font with Vietnamese and long task titles.
5. Check refresh while an interaction is in progress; task actions must not vanish mid-tap.
6. Force plugin storage errors: Today+ should preserve the task state, explain the preference save failure, and never mutate project ordering.
7. Verify original task/habit controls and native Won't Do remain functional with the known brief navigation blink.

## Release blockers

- Native tracking Start/Stop and Focus overlay tested on an installed current app version.
- No double counting or duplicate Working Now cards.
- Preference loading and day transition tested.
- Small-screen layout and actual touch drag tested.
- Review README and Changelog, update screenshot references if needed.
