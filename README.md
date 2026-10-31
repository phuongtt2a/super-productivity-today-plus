# Today+

**Focus on what matters. Not another endless checklist.**

**Today+** is an independent, community-built plugin for [Super Productivity](https://app.super-productivity.com/), created by [phuongtt2a](https://github.com/phuongtt2a). It brings **tasks due today** and **habits scheduled for today** onto one calm screen, so you can see your work and routines without switching views.

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

*Screenshots use demonstration tasks and habits, not real account data.*

## Why Today+?

Super Productivity organizes tasks and habits in different views. Today+ brings **tasks due today** and **habits scheduled for today** onto one screen, reducing the need to switch back and forth while keeping Super Productivity as the source of truth. You can complete tasks, update habit goals, and manually log time without replacing the native habit tracker.

## Features

- **Today’s tasks:** See tasks due today, with subtasks nested beneath their parents. Overdue and completed tasks are hidden at first; you can show either when needed.
- **Clear daily actions:** Complete a task, or tap the small **calendar-with-X icon** ("Not Today") to remove its due date without marking it completed. The task remains in its project until you schedule it again.
- **Scheduled habits:** Read existing enabled habits from Super Productivity. Follow weekday schedules; show weekly-frequency habits during the week.
- **Single-completion habits:** Tap once to complete; tap again to undo.
- **Count or goal-based habits:** Increase or decrease today's value and see progress toward the configured goal.
- **Stopwatch habits:** View accumulated time and the target. Use **Log time** to manually add minutes already spent **only when the built-in stopwatch is not running**. Today+ does not start, stop, or replace the app's timer.
- **One dashboard:** See both sections and overall progress; it automatically refreshes periodically and when the app regains focus.
- **Theme and mobile:** Uses Super Productivity's font and theme variables, keeps the host wallpaper visible, supports light/dark mode and small phone screens.

No separate login, external service, duplicate tasks, or additional local data store is required.

## Install

1. [Download the latest installable Today+ ZIP](https://github.com/phuongtt2a/super-productivity-today-plus/raw/refs/heads/main/dist/today-plus-super-productivity.zip) from the current repository build. This also includes minor UI fixes that retain the same version number. (GitHub Release assets are historical, unchanged snapshots; do not install GitHub’s automatic source ZIP.)
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

## How the daily view works

Today+ starts with tasks due **today** and habits scheduled for **today**. Subtasks appear directly beneath their parent task. **Overdue** and **Finished** are hidden by default; turn on either filter to see more.

Habits follow your existing Super Productivity schedule. Daily habits show today's progress, while flexible weekly habits show progress toward their weekly goal. Nothing needs to be configured a second time inside Today+.

## What “Not Today” means

Choosing the **calendar-with-X icon** ("Not Today") clears the task’s scheduled date and removes it from the daily list. The icon is labeled for screen readers and shows a tooltip on desktop. It is only shown when a task has its own scheduled date; undated subtasks inherited from a scheduled parent have no separate date to clear. It does **not** complete, delete, postpone until tomorrow, or mark the task as Super Productivity’s native “Won’t do.” To work on it another day, schedule it again in Super Productivity. For repeating tasks, Today+ asks for confirmation because changing an occurrence’s due date can affect its repetition schedule.

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
.github/workflows/    # CI and versioned GitHub release
```

Run from the repository root:

```bash
python -m unittest discover -s tests -p 'test_*.py' -v
python scripts/package.py --tag v1.1.0
```

For browser tests, install Python Playwright and Chromium, then run `python tests/integration_check.py` and `python tests/browser_check.py`. See [development notes](docs/DEVELOPMENT.md) and [release instructions](docs/RELEASING.md).

For the official plugin contract, see the [Super Productivity Plugin Development Guide](https://github.com/super-productivity/super-productivity/blob/master/docs/plugin-development.md).

## About and releases

- [GitHub About details](docs/ABOUT.md): description, website and repository topics.
- [Changelog](CHANGELOG.md): version history.
- [Release instructions](docs/RELEASING.md): how the four-file ZIP is built and verified.

## Contributing

Issues and pull requests are welcome. Please read [CONTRIBUTING.md](CONTRIBUTING.md). License: [MIT](LICENSE).
