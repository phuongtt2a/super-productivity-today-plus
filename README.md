# Today+

**Your tasks and habits, together.**  
An independent, community-built plugin for [Super Productivity](https://app.super-productivity.com/) by [phuongtt2a](https://github.com/phuongtt2a).

**Today+ is a completely separate plugin from Five.** It has its own ID, source and installable ZIP. Installing it doesn't replace or change Five.

## Preview

![Today+ on desktop](docs/screenshots/desktop.webp)

![Today+ on mobile](docs/screenshots/phone.webp)

## What it shows

- **Tasks**: active tasks with a due date on or before today; overdue tasks can be hidden, and finished tasks can be shown. Tasks are read from Super Productivity with `PluginAPI.getTasks()`.
- **Habits**: enabled habit tracker/counters scheduled for today, from `PluginAPI.getAllSimpleCounters()`. Weekday streak schedules are respected; weekly-frequency habits can be completed on any day of the week.
- **Progress**: completion and daily progress for tasks, simple checkbox habits, counter habits and weekly habits.
- **Actions**: mark tasks done / to do, complete or undo one-click habits, and increase/decrease goal counters with the supported API. Stopwatch habits show logged duration and offer **Log time** to add minutes already spent when the native timer is paused. Today+ never starts or stops the native stopwatch.
- **Theme**: inherits host font and theme variables; the page stays transparent over Super Productivity's wallpaper. Works on desktop and mobile.

![Today+ manual time logging for a paused stopwatch habit](docs/screenshots/log-time.webp)

## Installation

1. Download **today-plus-super-productivity.zip** under **Assets** in the [latest GitHub Release](https://github.com/phuongtt2a/super-productivity-today-plus/releases/latest) (not GitHub's automatic Source code archive).
2. In [Super Productivity](https://app.super-productivity.com/), go to **Settings → Plugins**.
3. Choose the plugin ZIP. Do **not** unzip it before importing.
4. Open **Today+** from the plugin navigation.

## Definition of today

The plugin uses the device's local calendar date, matching the task `dueDay` field where present and falling back to `dueWithTime`. It displays tasks due today and overdue, not every task in all projects. The **Overdue** button hides overdue tasks; the **Finished** button includes tasks already marked complete.

Habits use `streakWeekDays` for weekday schedules. Non-streak counters visible in the host's habit tracker appear as general daily counters. Weekly-frequency habits remain visible throughout the week and show weekly progress. Stopwatch habit values are stored in milliseconds. The **Log time** action adds minutes to today's value, and is disabled while the native stopwatch is running.

No data is stored separately by this plugin. Task and habit changes are written to Super Productivity itself. Values refresh when the plugin regains focus, when task hooks fire, and periodically while visible (the host does not provide a dedicated habit-change hook).

## Package structure

```text
plugin/
├── manifest.json
├── plugin.js
├── index.html
└── icon.svg
```

All UI CSS and JavaScript is inlined in `index.html`, consistent with the [official plugin development guide](https://github.com/super-productivity/super-productivity/blob/master/docs/plugin-development.md).

## Development and tests

```bash
python -m unittest discover -s tests -p 'test_*.py' -v
python scripts/package.py --tag v0.2.0
# Browser tests, after installing Playwright and Chromium:
python tests/integration_check.py
python tests/browser_check.py
```

Open `plugin/index.html` in a browser for a clearly labeled static-data preview. Actual API integration must be tested inside a supported Super Productivity build.

## Manual time logging

For a stopwatch habit, click **Log time**, enter the minutes you already spent, then choose **Add time**. The native Super Productivity stopwatch must be paused. Today+ checks its state again before saving, and updates the native habit total instead of maintaining a separate timer.

## Scope and limitations

- Unlike Five, there is **no five-task limit**. The combined view scrolls naturally when you have many items.
- It does not provide task creation, habit creation, or custom habit schedule editing. Use the native app for those.
- For repeated countdown habits, the plugin edits the daily counter, not the countdown timer itself.
- `getAllSimpleCounters()` and `setCounter()` are present in the current Super Productivity iframe plugin bridge. Older host versions may not expose them.
- This is not an official Super Productivity feature or affiliated product.

## More information

- [Development guide](docs/DEVELOPMENT.md)
- [Release process](docs/RELEASING.md)
- [Repository About description and topics](docs/ABOUT.md)
- [Changelog](CHANGELOG.md) · [Contributing](CONTRIBUTING.md) · [MIT License](LICENSE)
