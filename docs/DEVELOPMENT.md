# Architecture and local development

Today+ runs as a self-contained Super Productivity iframe plugin. All runtime HTML, CSS and JavaScript live in `plugin/index.html`. The host injects its theme variables and the filtered `PluginAPI` bridge. `plugin/plugin.js` is intentionally a minimal host-side file to match the four-file packaging pattern.

## Data and supported APIs

- `getTasks()` / `getAllProjects()` load task and project records.
- `getAllSimpleCounters()` loads existing enabled habits and their `countOnDay` history, goals and weekday configurations.
- `updateTask(id,{isDone})` completes or reopens tasks; `selectTask(id)` opens the native task details.
- `setCounter(id,value)` updates the daily value for simple-completion, count, or paused stopwatch habits. Stopwatch counts are measured in milliseconds.
- `registerHook(...)` listens for task changes. Habits have no dedicated hook; the UI refreshes when focused and every 30 seconds while visible.

## Habits

- `ClickCounter` + streak tracking + goal 1: show toggle. Other click counters: plus/minus.
- `RepeatedCountdownReminder`: show count-based progress only; do not take over the native reminder timer.
- `StopWatch`: show accumulated time and goal, with **Log time** input in minutes. Do not start/stop the host stopwatch; disable manual logging when `isOn` is true.
- `streakWeekDays`: specific weekdays; `streakMode=weekly-frequency`: eligible throughout the week.

## Run locally

```bash
python -m unittest discover -s tests -p 'test_*.py' -v
python scripts/package.py --tag v0.2.0
node --check plugin/plugin.js
python tests/integration_check.py
python tests/browser_check.py
```

The browser tests use Playwright and Chromium; `pip install playwright` and `python -m playwright install chromium` if necessary. Do not use real task data for testing. The `index.html` demo preview is explicitly labelled.

## Accessibility and theme guidance

- Use `var(--font-primary-stack)` for Vietnamese support and host consistency.
- Prefer injected text, divider and primary-color tokens; keep the iframe background transparent to show the host wallpaper.
- On small screens, keep buttons tappable and avoid horizontal page overflow.
- Prefer buttons with descriptive accessible labels. Keep dialog actions keyboard accessible.
- Treat numerical progress values as numbers, not Boolean completion except for one-click habits.

## Limitations

The plugin does not replicate Super Productivity's Today virtual-tag membership; it selects by due date. Data changes are written to Super Productivity and are not stored in a separate plugin database. Verify behavior on desktop/mobile hosts before sharing a release widely.
