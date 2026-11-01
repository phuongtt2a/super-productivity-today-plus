# Today+ v2.0.0 — Working Now, Ordering & Release QA

**Status:** Approved for v2.0.0 release. The user confirmed all primary features work in the installed Super Productivity app, including the last feedback corrections (timer status, right-aligned Arrange, and continuing a goal-met habit). Automated CI and screenshots supplement, rather than replace, the user's live-app verification. Device-to-device preference propagation and unusual legacy-host cases are still environment-dependent; avoid presenting them as universally tested.

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

1. Select a task through its target icon. Confirm **only one task or habit** is in Working Now and the task is not duplicated in the list.
2. Select a different task and verify it replaces the former task; the former task returns to the list.
3. Select a task with subtasks and verify the entire group stays accessible and its subtasks can be completed.
4. Test selecting a subtask. Verify the parent remains in Tasks while the selected subtask moves to Working Now.
5. Remove the selected task. Verify it returns to Tasks **without stopping native tracking**.
6. Complete the task or choose **Won't Do** from Working Now. Verify the native record is correct, the Working Zone becomes empty and overall progress is counted only once.
7. Select a **habit** from Habits. Confirm it appears in Working Now, disappears from Habits without duplicating progress, and retains its Complete, +/−, or Log time control as appropriate. Completing it **must not empty Working Now**; the user chooses when to remove or replace it.
7a. Test a **completed 60-minute stopwatch habit**: select it despite already meeting the goal, log another 30 minutes, verify the native total is 90 minutes, daily Done totals do not increase a second time, and the habit remains in Working Now until explicitly removed.
8. Replace a Working Now task with a habit and vice versa. Confirm the previous item returns to its original list.
9. Ensure habits do not show native task-tracking or Focus-mode buttons.
10. Confirm Arrange appears at the far right of Tasks and Habits and is visually distinct from the Overdue/Finished filters.
11. Test unfinished overdue, completed, deleted and rescheduled tasks after a restart. Invalid Working Now references must not surface ghost tasks.

## Native tracking and Focus

1. Selecting a task must **not** start tracking automatically.
2. Click Start tracking; verify Super Productivity tracks the correct task (for a parent, it may track the first unfinished subtask). Repeat on a host without `startTracking` but with the allowed `[Task] SetCurrentTask` action; the button should stay usable.
3. Click Stop tracking; verify the native timer stops and no duplicate elapsed-time counter exists in Today+.
4. Change tracked task from another Super Productivity view. Confirm the Working Now state updates through currentTaskChange when Today+ is active.
5. Restart Today+ during an active tracking session. The API does not provide a direct initial-current-tracker read; the interface must not pretend the tracker was confirmed until it receives a hook or explicitly starts it.
6. Click **Focus on task**. Verify it first activates exactly the Working Now task as the native tracked task and then opens the Focus interface without forcing a Pomodoro/Countdown session. Confirm it does not open unrelated task details.
7. Test with an old host lacking the optional tracking or logical-day API: controls must fall back through allowed native actions or explain unavailability. Confirm no fake timer and no unsafe state writes.

## Visual, input and persistence quality

1. At 320px, 390px, tablet and desktop widths: no horizontal scroll, clipped text, or overlapped buttons.
2. Test with real mouse, touch (tap/drag), keyboard-only Tab/Enter/Space, screen reader labels.
3. Drag handles must not accidentally scroll the task instead of reordering, or prevent scrolling elsewhere.
4. Check light/dark themes, custom wallpaper transparency, native application font with Vietnamese and long task titles. Verify the active Working Now green-and-gold treatment stands out while Arrange is clearly a separate operation from Overdue/Finished filters.
5. Check refresh while an interaction is in progress; task actions must not vanish mid-tap.
6. Force plugin storage errors: Today+ should preserve the task state, explain the preference save failure, and never mutate project ordering.
7. Verify original task/habit controls and native Won't Do remain functional with the known brief navigation blink.

## v2.0.0 release acceptance

- [x] User verified the primary task, habit, arrange, tracking, Focus, and goal-met-habit workflows in the installed app.
- [x] Browser regression verifies no double counting or duplicate Working Now cards.
- [x] Browser regression covers preference restoration, task/subtask order and remote-preference update behavior.
- [x] Browser regression covers 320px mobile layout, drag and accessible reorder controls.
- [x] README, screenshots, changelog, and stable version updated.
- [ ] Optional follow-up: verify cross-device syncing with two real installations, physical touch on additional hardware, and unusual host versions.
- [ ] Future UX improvement: remove the accepted brief screen blink when invoking native Won't Do.
