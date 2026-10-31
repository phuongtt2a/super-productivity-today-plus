# Changelog

## Unreleased — minor interface refinements (version stays 1.1.0)

- Display **Not today** as a compact calendar-with-X icon with a 40px touch target, accessible name and desktop tooltip.
- Prevent focus-triggered refreshes from replacing a task action while the user taps it; the first tap now works.
- Hide the action on subtasks without their own due date so there is no nonfunctional control.
- Replace the dashboard headline with “Focus on what matters.” and the supporting line with “Not another endless checklist.”
- Give **Not today** a visible but subtle outlined-button appearance on desktop and mobile.
- Keep the existing task actions, filters and plugin version unchanged; refresh screenshots and the installable ZIP on the main branch.

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
