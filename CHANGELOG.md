# Changelog

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
