# Today+ native Won't Do — verification checklist

Status: EXPERIMENTAL / draft PR. No changes to Super Productivity. Do not merge or release until live-app checks pass.

## Semantics

Native Won't Do closes only the selected occurrence. It is not equivalent to removing the due date or marking a task Done. The native status uses isDone plus matching doneOn and wontDoOn. A skipped occurrence must not count as successful completion in the host's metrics or unintentionally complete linked issues.

## Architecture

- plugin/index.html: the Won't Do icon sends a message using the existing plugin iframe bridge.
- plugin/plugin.js: receives the request, checks the task with PluginAPI.getTasks(), and only if a uniquely matching native task row is already visible, opens its native context menu and clicks the native "block" menu item. No direct task update is issued by Today+.
- If the row is not present (normal when Today+ occupies the work view), Today+ selects the task and tells the user to use its native Won't Do menu manually.
- If the menu was activated but the native state cannot be verified, Today+ does not claim success.
- The app's recurring-task engine remains responsible for future occurrences.

## Real-app test plan

1. Install the feature-branch ZIP in Super Productivity v19.3+ in a test profile; back up test data.
2. Create a one-off task due today. Click Won't Do in Today+ and if prompted choose Won't Do from the host task menu. Confirm it shows a cross instead of a check and is excluded from completed-task metrics.
3. Create a fixed-schedule daily task. Skip today's occurrence; verify the next scheduled occurrence appears without changing the repeat rule.
4. Create an after-completion recurring task. Skip today's occurrence; verify its next occurrence follows the native skip date.
5. Test a subtask and a parent with multiple subtasks; verify parent/subtask behavior.
6. Test a linked issue; ensure Won't Do does not close or log it.
7. Verify normal Done, Undo Done, and native reopen still work.
8. Exercise both paths: native task row visible vs. Today+ occupying work view. An ambiguous task or menu must never be clicked.
9. Check desktop, mobile touch, 320px and 390px layouts, light/dark themes, and wallpaper transparency.
10. Reopen Today+ or sync another device; confirm native Won't Do semantics survive.

## Automation vs. remaining uncertainty

CI runs a mocked host bridge to test request shape, schedule preservation, no fake completion, fallback, and touch. The mock cannot prove Angular Material's native menu opens reliably on installed app versions. The integration is still experimental until live-host verification.

## Failure policy

- NEVER fall back to updateTask isDone true: that counts a successful completion.
- NEVER clear dueDay/dueWithTime: it leaves an occurrence unfinished.
- NEVER click when the target task or host menu is ambiguous.
- If the native command is unavailable, open the task for the user to choose Won't Do manually.

Sources:
- https://github.com/super-productivity/super-productivity/blob/master/src/app/features/tasks/util/is-wont-do-task.ts
- https://github.com/super-productivity/super-productivity/blob/master/src/app/features/tasks/task-context-menu/task-context-menu-inner/task-context-menu-inner.component.ts
- https://github.com/super-productivity/super-productivity/blob/master/docs/plugin-development.md
