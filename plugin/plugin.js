// Today+ host-side adapter for Super Productivity's native "Won't Do" action.
//
// This runs in the host renderer. It deliberately does not alter task data,
// call private Angular services, or mark an occurrence Done as a substitute.
// The native context-menu path is attempted only if the matching task row is
// already mounted. Otherwise Today+ opens the task for manual completion.
(function () {
  "use strict";

  const REQUEST_KIND = "today-plus:native-wont-do";

  function delay(ms) {
    return new Promise(function (resolve) { setTimeout(resolve, ms); });
  }

  function findNativeMenuAction(doc) {
    // The icon name is stable across translations; never match translated text.
    const items = Array.from(
      doc.querySelectorAll(".cdk-overlay-container [role='menuitem']")
    );
    const matches = items.filter(function (button) {
      return Array.from(button.querySelectorAll("mat-icon")).some(function (icon) {
        return (icon.textContent || "").trim() === "block";
      });
    });
    return matches.length === 1 ? matches[0] : null;
  }

  async function tryNativeWontDo(taskId) {
    if (typeof taskId !== "string" || !taskId || taskId.length > 256) {
      return { status: "manual", reason: "Invalid task identifier." };
    }

    const tasks = await PluginAPI.getTasks();
    const task = tasks.find(function (item) { return item.id === taskId; });
    if (!task || task.isDone) {
      return { status: "unavailable", reason: "Task is missing or already finished." };
    }

    const visibleRows = Array.from(document.querySelectorAll("task[data-task-id]"))
      .filter(function (row) {
        return row.getAttribute("data-task-id") === taskId
          && row.isConnected
          && row.getClientRects().length > 0;
      });

    // Today+ usually owns the work-view surface, so this often falls back.
    if (visibleRows.length !== 1) {
      return { status: "manual", reason: "The native task row is not visible." };
    }

    // Do not click into someone else's open menu.
    if (document.querySelector(".cdk-overlay-container [role='menu']")) {
      return { status: "manual", reason: "Another native menu is already open." };
    }

    const row = visibleRows[0];
    const rect = row.getBoundingClientRect();
    row.dispatchEvent(new MouseEvent("contextmenu", {
      bubbles: true,
      cancelable: true,
      button: 2,
      clientX: rect.left + Math.min(16, rect.width / 2),
      clientY: rect.top + Math.min(16, rect.height / 2)
    }));

    let opened = false;
    for (let attempt = 0; attempt < 10; attempt += 1) {
      await delay(75);
      opened = Boolean(row.querySelector("task-context-menu-inner"));
      if (!opened) continue;
      const action = findNativeMenuAction(document);
      if (!action) continue;
      // The menu was opened from the uniquely matched task row, and there was
      // no pre-existing menu. Click the native item, never emulate task updates.
      action.click();
      await delay(180);
      const current = (await PluginAPI.getTasks()).find(function (item) {
        return item.id === taskId;
      });
      if (current && current.isDone && current.wontDoOn != null
        && current.wontDoOn === current.doneOn) {
        return { status: "confirmed" };
      }
      return {
        status: "unverified",
        reason: "The native menu was activated but Won't Do status was not confirmed."
      };
    }

    return {
      status: opened ? "menu-opened" : "manual",
      reason: opened
        ? "The native menu is open, but its Won't Do item was not identified."
        : "Could not open the native task menu."
    };
  }

  if (typeof PluginAPI.onMessage === "function") {
    PluginAPI.onMessage(function (message) {
      if (!message || message.kind !== REQUEST_KIND) return null;
      return tryNativeWontDo(message.taskId);
    });
  }
})();
