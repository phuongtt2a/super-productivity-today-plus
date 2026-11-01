# Changelog

## 2.0.0 — Working Now and personalized daily priorities (major release)

**Today+ is now a daily workspace, not just a combined checklist.** This version has been verified in the installed Super Productivity app by the user after three beta iterations.

- **Working Now:** Select one task or habit using its target icon. Keep one visible priority without cloning records or distorting daily progress; replace or remove the selection whenever you want.
- **Task and subtask ordering:** Drag parent task groups or use accessible Move to top / Up / Down controls. Arrange subtasks inside their own parent; reset the task order each logical day without modifying Super Productivity's project task order.
- **Habit routine ordering:** Arrange habits independently and retain their preferred order across days. Persist Today+ preferences through Super Productivity's synced plugin storage where available.
- **Native task tracking and Focus:** Start/Stop through the native tracker, including an allowed-action fallback for older hosts. **Focus on task** activates the selected task before opening Super Productivity's native Focus interface; no duplicate timer or unsupported session-start action.
- **Continue after a habit goal:** Already-completed habits remain selectable for Working Now and can accumulate additional minutes/counts (for example, 90 minutes against a 60-minute goal). Only the user can remove or replace a completed habit from Working Now; completion is counted once.
- **Clear controls and status:** Arrange is right-aligned and visually distinct from Overdue/Finished filters; task tracking reads **Not tracking** or **Tracking in Super Productivity**.
- **Consistent NEO-Zen design:** Highlight the active zone in translucent green-and-gold, use the application's Vietnamese-compatible font, retain wallpaper transparency, and support narrow screens, touch, and keyboard.
- **Preserved behavior:** Native Won't Do, recurrence, scheduled habits, stopwatch logging, task hierarchy, and existing filters are retained. A brief view blink can still occur when native Won't Do temporarily visits the host task list.

**Quality:** Existing regression tests and new browser tests cover ordering, saved preferences, task/habit focus, goal-met extra habit time, Focus/tracking action order, mobile drag, 320px layout, and plugin packaging. Screenshots and installation instructions are refreshed.

## 1.3.0-beta.3 — Completed habits stay focusable (preview only)

- Keep goal-met habits eligible for Working Now; completed stopwatch habits can continue logging time beyond their daily targets.
- Do not automatically remove a habit from Working Now on completion. Removing or replacing the priority is a deliberate user action.
- Simplify status language to **Not tracking** / **Tracking in Super Productivity**, without adding a second timer.
- Put Arrange at the far right of Tasks and Habits, separate from Overdue/Finished filters.
- Extend browser tests and mobile preview screenshots for the already-completed habit scenario.

## 1.3.0-beta.2 — Working Now usability improvements (preview only)

- Add **habits** to Working Now, including native Complete, Increase/Decrease and Log time controls. Selecting or completing a habit never starts a task timer.
- Activate the chosen task before opening the native Focus overlay, without dispatching the restricted Start Session action.
- Support the approved task tracking action when the optional time-tracking methods are absent on older installed hosts.
- Distinguish Arrange actions from Overdue/Finished filters, and give Working Now a stronger translucent green-and-gold treatment.
- Preserve previously saved task selections and habit order. Keep the public 1.2.0 release unchanged.

## 1.3.0-beta.1 — Working Now and personal daily ordering (preview only)

- Add independent user-defined ordering of task groups, nested subtasks and daily habits, with drag handles and accessible Move to top/up/down buttons.
- Save task order for each logical day, a recurring habit routine across days, and a single Working Now task using synced plugin preferences.
- Add a dedicated Working Now area without duplicating its task or altering completion statistics.
- Integrate native Start/Stop tracking and Open Focus overlay; no second timer and no unsupported start-session actions.
- Preserve NEO-Zen styling, transparency, host fonts, existing Won't Do behavior and small-screen usability.
- Preview release only: do not merge into main until mobile and real-host tests pass.


## 1.2.0 — Native Won't Do and clear task actions

- Replace **Not Today** (which cleared due dates) with Super Productivity's genuine **Won't Do** task operation; recurring tasks retain the host's scheduling behavior.
- Use a compact, icon-only **task-with-X** button instead of the ambiguous circle-with-slash symbol. Keep the tooltip and accessible label exactly “Won't Do.”
- Allow skipping regular tasks and subtasks, including subtasks without their own due date.
- Keep the temporary task context menu and detail panel from appearing during automated skipping. Do not change due dates or emulate Done.
- **Known UX limitation:** temporarily switching to the host task list and back can briefly blink the screen. A seamless transition is deferred to a future improvement.
- Preserve Today+'s NEO-Zen styling, host font/transparency, responsive task hierarchy and habit actions.

## Interface refinements incorporated into v1.2.0

- Prevent focus-triggered refreshes from replacing task actions during taps.
- Keep “Focus on what matters.” and “Not another endless checklist.” on the dashboard.
- Retain responsive task actions and refreshed screenshots.

## 1.1.0 — Task hierarchy and clearer status controls

- Group subtasks below their parent tasks, including undated subtasks in today's scheduled parents.
- Hide overdue and finished tasks by default; both remain available through filters.
- Show **Not today** beside each task's completion circle; it clears the scheduled date without completing the task. Native **Won’t do** is a different task status.
- Keep the existing task, habit, manual time logging and synced data behavior.


## Unreleased — logo alignment (manifest stays v1.0.1)

- Use the same calendar-and-check artwork in the Super Productivity plugin menu and the Today+ header.
- Keep the original plugin identifier and the behavior of tasks and habit controls unchanged.
- Refresh desktop and mobile documentation screenshots.


## 1.0.1 — Stable version and clearer documentation

- Publish Today+ as stable **v1.0.1** with matching manifest and GitHub Release.
- Improve project introduction and the description shown in Super Productivity.
- Document the full workflow for tasks, scheduled habits, habit goals and time logging.
- Keep the original plugin ID, native app integration, and tested behavior unchanged.
- Preserve historical v0.2.0 release without rewriting its tag.

## 0.2.0 — Initial public release of Today+

- Publish **Today+** as a separate plugin with tasks due today and scheduled habits in one view.
- Add completion controls for tasks and simple habits; plus/minus for count-based habits.
- Add manual time logging for paused stopwatch habits (without controlling host timers).
- Use the host's theme/font variables and a transparent, responsive layout.
- Add installation and development documentation, automated checks, and a GitHub release ZIP.

## 0.1.0 — Local prototype

- Initial tasks and habits dashboard prototype; not separately published on GitHub.
