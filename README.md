# Today+

**Focus on what matters. Not another endless checklist.**

> Today+ is separate from [Five](https://github.com/phuongtt2a/super-productivity-five), the five-priority focus plugin. Installing either does not replace the other.

[![For Super Productivity](https://img.shields.io/badge/For-Super%20Productivity-4d7560)](https://app.super-productivity.com/) [![MIT License](https://img.shields.io/badge/license-MIT-informational)](LICENSE)

## Preview

Today+ uses one consistent calendar-and-check icon in both the Super Productivity plugin menu and the dashboard header.

![Today+ desktop view with tasks, subtasks and habits](docs/screenshots/today-plus-tasks-desktop-v1.1.0.webp)

<details>
<summary>Mobile layout and manual time entry</summary>

![Today+ mobile view with subtasks beneath the parent](docs/screenshots/today-plus-tasks-phone-v1.1.0.webp)

![Today+ manual time entry for stopwatch habits](docs/screenshots/log-time.webp)

</details>

<details>
<summary>New in the workspace preview: active task and rearranging a day</summary>

![Today+ Working Now with a selected task and its subtasks](docs/screenshots/working-now-active.webp)

![Today+ mobile arrangement mode with Move to top and up/down controls](docs/screenshots/arrange-mode-phone.webp)

</details>

## Why Today+?

Super Productivity organizes tasks and habits in different views. Today+ brings **tasks due today** and **habits scheduled for today** onto one screen, reducing the need to switch back and forth while keeping Super Productivity as the source of truth. You can complete tasks, update habit goals, and manually log time without replacing the native habit tracker.

## Features

- **Arrange your day (preview):** Open **Arrange** in Tasks or Habits. Drag by the grip or use the keyboard/touch-friendly **Move to top / Move up / Move down** controls. Top-level tasks move as a group; subtasks are arranged within their parent. This changes only Today+'s display, not project order.
- **Saved routines (preview):** Task order is saved per logical day; habit order remains your preferred recurring daily routine. Today+ saves the preferences using Super Productivity's synced plugin storage, where supported.
- **Working Now (preview):** Tap the target icon on one task or habit to bring it into **Working Now**, without copying, completing, or automatically tracking it. Pick another task or habit to replace it; **Remove** returns it to the normal list. Habits retain their native Complete/Increase/Log time controls.
- **Native tracking and Focus (preview):** **Start tracking / Stop tracking** uses the application's own time tracker, with an approved action fallback for older hosts lacking the newer optional tracking methods. **Focus on task** activates your selected Working Now task before opening Super Productivity's native Focus interface. It does **not** automatically start a Pomodoro or replace its built-in timer. Native task tracking and Focus sessions do not apply to habits.

- **Today’s tasks:** See tasks due today, with subtasks nested beneath their parents. Overdue and completed tasks are hidden at first; you can show either when needed.
- **Native Won't Do:** Tap **Won’t Do** to invoke Super Productivity’s native skip using its task-row menu. Today+ briefly visits the native task list if needed, visually conceals only the temporary task menu, and returns to Today+. Task details do not open. If the native menu cannot be reached, it leaves the task unchanged and shows guidance. Native recurrence and completion semantics are preserved.
- **Scheduled habits:** Read existing enabled habits from Super Productivity. Follow weekday schedules; show weekly-frequency habits during the week.
- **Single-completion habits:** Tap once to complete; tap again to undo.
- **Count or goal-based habits:** Increase or decrease today's value and see progress toward the configured goal.
- **Stopwatch habits:** View accumulated time and the target. Use **Log time** to manually add minutes already spent **only when the built-in stopwatch is not running**. Today+ does not start, stop, or replace the app's timer.
- **One dashboard:** See both sections and overall progress; it automatically refreshes periodically and when the app regains focus.
- **Theme and mobile:** Uses Super Productivity's font and theme variables, keeps the host wallpaper visible, supports light/dark mode and small phone screens.

No separate login, external service, duplicate tasks, or additional local data store is required.

> **Known limitation in v1.2.0:** Won't Do uses Super Productivity's native task menu through a plugin-side workaround. Today+ may briefly switch to the host task list and back, causing a momentary screen blink. We are retaining this behavior for now rather than faking task completion or changing recurring-task schedules. The action is verified by checking the native `wontDoOn` state; UI automation may need maintenance after host updates.

> **v1.3.0-beta.2 preview:** The new ordering and Working Now features are in an unreleased branch for testing, not in the official v1.2.0 download below. Install the preview ZIP from the GitHub Actions artifact when available. See [workspace QA checklist](docs/WORKSPACE-VERIFICATION.md). The existing native Won't Do workaround and its brief screen blink are unchanged.

## Install

1. [Download the latest installable Today+ ZIP](https://github.com/phuongtt2a/super-productivity-today-plus/releases/latest/download/today-plus-super-productivity.zip) from the official latest GitHub Release. New builds are published automatically after tested changes merge into `main` (including same-version UI fixes). Install the ZIP under **Assets**, not GitHub's automatically generated source archive.
2. In [Super Productivity](https://app.super-productivity.com/), go to **Settings → Plugins** and choose **Choose Plugin File**.
3. Import the downloaded ZIP **without unpacking it**. Then open **Today+** from the plugin menu.


The installable ZIP contains exactly four root files:

```text
today-plus-super-productivity.zip
├── manifest.json
├── plugin.js
├── index.html
└── icon.svg
```

## What changed in beta.2

The **Arrange** buttons are now visually distinct from the **Overdue** and **Finished** filters, and the **Working Now** area has a stronger green-and-gold treatment that retains wallpaper transparency. Your priority can be a task **or** a habit; the habit can be completed, incremented, or logged from Working Now without being counted twice.

If the optional `startTracking()` API is unavailable, Today+ uses the approved `[Task] SetCurrentTask` host action; Start tracking should no longer be an unexplained disabled control on hosts that support the task action. **Focus on task** activates the task first, then opens Focus mode. Choosing Focus starts native task time tracking, but leaves native session duration/confirmation to Super Productivity.

## Organizing tasks and habits

Open **Arrange** in either list to reveal a drag handle and Move to top/up/down buttons. Parent task rows move as a group, and subtasks are rearranged inside their parent. On phones and with keyboard or assistive technology, the explicit buttons are an alternative to dragging.

Today+'s task order resets each logical day; recurring habits retain the order you chose until you change it. Ordering and the Working Now task ID are stored as preferences, not copied tasks. No native task project order is changed, and progress totals still include the task in Working Now.

Selecting a task for Working Now does not start time tracking. Start/Stop operates on the native tracker when supported. The app's `currentTaskChange` event supplies updates while Today+ is running; a refreshed iframe cannot reliably read the already-active tracker, so it does not claim tracking is active unless confirmed. Removing a task from Working Now does not stop native tracking.

## How the daily view works

Today+ starts with tasks due **today** and habits scheduled for **today**. Subtasks appear directly beneath their parent task. **Overdue** and **Finished** are hidden by default; turn on either filter to see more.

Habits follow your existing Super Productivity schedule. Daily habits show today's progress, while flexible weekly habits show progress toward their weekly goal. Nothing needs to be configured a second time inside Today+.

## What “Won't Do” means

Choose the compact **task-with-X icon** (with the exact tooltip and accessibility label **"Won't Do"**) to intentionally skip the current task occurrence using Super Productivity's **native Won't Do** action. Unlike the old **Not Today** action, this does **not** clear the scheduled date and is not a normal Done completion. The host records the skipped outcome; for recurring tasks, the app controls when the next occurrence appears.

Today+ hides finished tasks by default. Turn on the **Finished** filter to review a skipped occurrence labelled **Won't Do** (×). If the host task row cannot be reached safely, the task is left unchanged and Today+ explains the problem. A brief screen blink may occur because the plugin temporarily visits the native task list.


## Safety and limitations

- Today+ does not create tasks or habits. Manage definitions and habit schedules in the main Super Productivity app.
- To log a stopwatch habit, pause its existing stopwatch in Super Productivity first. The dialog **adds** time already spent, not a replacement total. It does not control the native stopwatch or countdown reminders.
- Updates to habits made in another screen may appear after refresh or when the plugin regains focus. The API does not provide a dedicated habit-change hook.
- In a desktop app or mobile app, Super Productivity's own stored data remains the source of truth. In a standalone browser preview without the plugin API, Today+ shows explicitly labelled demo data only.
- Compatible with Super Productivity versions exposing the documented iframe Plugin API, including `getAllSimpleCounters()` and `setCounter()`. Older versions may differ; please report issues with app version and reproduction steps.
- Today+ is a community project, not an official Super Productivity feature or an affiliated product.

## Development

Today+ is intentionally lightweight: no framework, build chain, external scripts or network requests.

```text
plugin/               # Files packaged at ZIP root
scripts/package.py    # Deterministic ZIP builder
scripts/              # Preview and screenshot helpers
tests/                # Package and browser integration tests
docs/                 # Screenshots and guides
.github/workflows/    # PR validation and automatic release publishing
```

Run from the repository root:

```bash
python -m unittest discover -s tests -p 'test_*.py' -v
python scripts/package.py --tag v1.2.0
```

For browser tests, install Python Playwright and Chromium, then run `python tests/integration_check.py` and `python tests/browser_check.py`. See [development notes](docs/DEVELOPMENT.md) and [release instructions](docs/RELEASING.md).

For the official plugin contract, see the [Super Productivity Plugin Development Guide](https://github.com/super-productivity/super-productivity/blob/master/docs/plugin-development.md).

## About and releases

- [GitHub About details](docs/ABOUT.md): description, website and repository topics.
- [Changelog](CHANGELOG.md): version history.
- [Release instructions](docs/RELEASING.md): how the four-file ZIP is built and verified.

## Contributing

Issues and pull requests are welcome. Please read [CONTRIBUTING.md](CONTRIBUTING.md). License: [MIT](LICENSE).

### NEO-Zen design family

Today+ uses the shared [NEO-Zen Design System](docs/NEO-ZEN-DESIGN.md) with Five and Deadline Watch: crisp outlines, hard offset shadows, thoughtfully tinted task/habit cards and a 1220px shared desktop shell. The plugin's runtime font remains **Super Productivity's own configured font**, including Vietnamese diacritics. The iframe and page canvas are **transparent** so the host wallpaper and opacity settings remain visible through theme-aware individual surfaces. No task, habit or Not Today behavior changes were made for this visual refresh. The screenshots above were regenerated from synthetic Vietnamese sample data and checked at desktop, 390px and 320px.
