# Today+

**Your tasks and habits, together.**

Today+ is an independent, community-built plugin for [Super Productivity](https://app.super-productivity.com/), created by [phuongtt2a](https://github.com/phuongtt2a). It brings **tasks due today** and **habits scheduled for today** onto one calm screen, so you can see your work and routines without switching views.

> Today+ is separate from [Five](https://github.com/phuongtt2a/super-productivity-five), the five-priority focus plugin. Installing either does not replace the other.

[![For Super Productivity](https://img.shields.io/badge/For-Super%20Productivity-4d7560)](https://app.super-productivity.com/) [![MIT License](https://img.shields.io/badge/license-MIT-informational)](LICENSE)

## Preview

![Today+ desktop view: tasks and habits side by side](docs/screenshots/desktop.webp)

<details>
<summary>Mobile layout and manual time entry</summary>

![Today+ mobile view: tasks followed by habits](docs/screenshots/phone.webp)

![Today+ manual time entry for stopwatch habits](docs/screenshots/log-time.webp)

</details>

*Screenshots use demonstration tasks and habits, not real account data.*

## Why Today+?

Super Productivity organizes tasks and habits in different views. **Today+ brings tasks due today and habits scheduled for today together**, helping you review your work and routines without switching screens. Complete tasks, track habit goals and manually log time spent without replacing the native habit tracker.

## Features

- **Tasks:** See Super Productivity tasks due today and overdue. Toggle overdue tasks and completed tasks, mark a task complete or return it to To Do, and open its details.
- **Scheduled habits:** Read existing enabled habits from Super Productivity. Follow weekday schedules; show weekly-frequency habits during the week.
- **Single-completion habits:** Tap once to complete; tap again to undo.
- **Count or goal-based habits:** Increase or decrease today's value and see progress toward the configured goal.
- **Stopwatch habits:** View accumulated time and the target. Use **Log time** to manually add minutes already spent **only when the built-in stopwatch is not running**. Today+ does not start, stop, or replace the app's timer.
- **One dashboard:** See both sections and overall progress; it automatically refreshes periodically and when the app regains focus.
- **Theme and mobile:** Uses Super Productivity's font and theme variables, keeps the host wallpaper visible, supports light/dark mode and small phone screens.

No separate login, external service, duplicate tasks, or additional local data store is required.

## Install

1. Open the [latest Today+ release](https://github.com/phuongtt2a/super-productivity-today-plus/releases/latest).
2. Under **Assets**, download **`today-plus-super-productivity.zip`** (not GitHub's **Source code (zip)**).
3. In [Super Productivity](https://app.super-productivity.com/), go to **Settings → Plugins** and choose **Choose Plugin File**.
4. Import the downloaded ZIP **without unpacking it**. Then open **Today+** from the plugin menu.

The installable ZIP contains exactly four root files:

```text
today-plus-super-productivity.zip
├── manifest.json
├── plugin.js
├── index.html
└── icon.svg
```

## How Today+ decides what appears

**Tasks:** Today+ reads active tasks using `PluginAPI.getTasks()`. It shows tasks due on or before the local calendar date (`dueDay` or `dueWithTime`). Tasks without a due date are not included. Completed tasks are hidden by default; **Finished** makes them visible. **Overdue** controls whether earlier dates appear. This is a *due-date dashboard*, not an exact copy of Super Productivity's Today work-context ordering.

**Habits:** In Super Productivity, the habit tracker is backed by *Simple Counters*. Today+ reads enabled counters using `PluginAPI.getAllSimpleCounters()`. For streaks scheduled on specific weekdays, only the matching weekdays appear. Weekly-frequency habits are eligible throughout the week; their progress is shown separately. General daily counters are also shown.

**Progress:** Click-counter goals are counts. Stopwatch goal and stored progress values are in **milliseconds** and are displayed in minutes/hours. Completing a task or incrementing a counter writes to Super Productivity through its plugin APIs.

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
python scripts/package.py --tag v1.0.1
```

For browser tests, install Python Playwright and Chromium, then run `python tests/integration_check.py` and `python tests/browser_check.py`. See [development notes](docs/DEVELOPMENT.md) and [release instructions](docs/RELEASING.md).

For the official plugin contract, see the [Super Productivity Plugin Development Guide](https://github.com/super-productivity/super-productivity/blob/master/docs/plugin-development.md).

## About and releases

- [Repository description, website and topics](docs/ABOUT.md)
- [Release notes and version history](CHANGELOG.md)
- [How to publish a new version](docs/RELEASING.md)

## Contributing

Issues and pull requests are welcome. Please read [CONTRIBUTING.md](CONTRIBUTING.md). License: [MIT](LICENSE).
