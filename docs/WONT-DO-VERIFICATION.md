# Today+ native Won't Do — beta verification checklist

Status: **v1.1.1-beta.2 / experimental draft PR**. Super Productivity is unchanged; this is plugin-side UI integration. Do not merge to the release branch until the live-app checks pass.

## Intended native semantics

Won't Do closes **one occurrence** without changing the recurring series. It is not equivalent to clearing its due date or marking it normally Done. Native skip status uses isDone plus matching doneOn and wontDoOn. Skipped tasks must not be counted as completed or close linked issues.

## Implementation

- The Today+ iframe sends a message through the existing Super Productivity plugin bridge.
- The host-side plugin.js checks the task ID and state through PluginAPI.getTasks().
- If the task's native row is visible, the adapter opens its context menu via the keyboard menu shortcut or a desktop context-menu event.
- On touch/small-screen layouts, the adapter opens the native task-list row using its keyboard context-menu shortcut. It never calls selectTask() or opens task details.
- When Today+ hides the task row, the adapter temporarily switches to the app's native Today task list, then (if needed) the project's task list. It opens that task's native row menu and returns to Today+. This route can briefly flash, but never opens a task-detail popup.
- The adapter searches for the icon named "block" instead of translated text, checks for exactly one matching task/menu action, and checks for native wontDoOn/doneOn status afterward.
- If UI elements are missing or ambiguous, it refuses to click, leaves task data unchanged, and shows guidance without opening task details. It never calls updateTask to fake completion or clear scheduling.

This is a deliberately **fragile integration point**: Angular Material's rendered DOM is not a supported plugin API. A Super Productivity update could change it.

## Real-host testing required

1. Install the beta ZIP using a **test profile** in Super Productivity 19.3+; back up any existing test data.
2. On desktop, create a one-off task due today. Tap Won't Do in Today+. Confirm it briefly switches to the host task list, returns to Today+, shows a native skipped state, and is excluded from completed statistics.
3. On mobile/touch, create a one-off task and ensure the action skips it without displaying a task-detail panel.
4. Create a **fixed-schedule daily/weekly repeated task**. Skip only the current occurrence. The repeat rule and next scheduled occurrence must remain intact.
5. Test an **after-completion** repeat. Check the next occurrence follows the host's native skip behavior.
6. Test parent/subtasks and a task with a linked issue. Confirm no unintended updates or issue closure.
7. Test an overdue task, a timed due task, and a task visible only in the project rather than Today.
8. Validate Done, Undo Done, and Reopen continue functioning.
9. Verify task ID matching under multiple visible tasks, duplicate titles, and other open menus.
10. Verify 320px, 390px, desktop, dark/light themes, wallpaper transparency, cross-device sync.
11. Test with a task in the Inbox (no projectId) and an instance whose native task row is not rendered. Verify graceful fallback without corrupting data.
12. Confirm the plugin returns to the **original screen** after temporary navigation; if the user navigates away during the operation, it must not override their navigation.

## Automated test limits

CI validates JavaScript syntax, manifest, packaging, simulated plugin message bridge, a DOM mock for the native task-row menu (no detail selection), temporary hash-route navigation/restoration, touch, and responsive behavior.

**CI cannot prove that a real installed Super Productivity version exposes the same task menu markup and performs the correct recurrence operations.** That must be confirmed manually before release.

## Failure policy

- Never simulate Won't Do using isDone=true or dueDay=null.
- Never click when the native task or menu is ambiguous.
- Never report success unless native wontDoOn === doneOn is observed on the target task.
- If the native UI cannot be invoked safely, leave the task untouched and show guidance; do not auto-open task details.

Upstream references:
- https://github.com/super-productivity/super-productivity/blob/master/src/app/features/tasks/util/is-wont-do-task.ts
- https://github.com/super-productivity/super-productivity/blob/master/src/app/features/tasks/task-detail-panel/task-detail-panel.component.html
- https://github.com/super-productivity/super-productivity/blob/master/src/app/features/tasks/task-context-menu/task-context-menu-inner/task-context-menu-inner.component.ts
