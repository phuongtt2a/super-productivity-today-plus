// Today+ host-side experimental adapter for Super Productivity's native "Won't Do".
//
// It never edits isDone, due dates, recurrence rules, or private app state.
// It invokes the host's own context-menu command, with fail-closed target checks.
// The plugin's index iframe may unmount during temporary navigation; this host-side
// handler remains alive and restores the original view after the attempt.
(function () {
  "use strict";

  const REQUEST_KIND = "today-plus:native-wont-do";
  const PLUGIN_ID = "sp-today-tasks-habits";
  let pending = false;

  function delay(ms) {
    return new Promise(function (resolve) { setTimeout(resolve, ms); });
  }

  function visible(el) {
    return !!el && el.isConnected && el.getClientRects().length > 0;
  }

  function getRows(taskId) {
    return Array.from(document.querySelectorAll("task[data-task-id]"))
      .filter(function (row) {
        return row.getAttribute("data-task-id") === taskId
          && !row.closest("task-detail-panel")
          && visible(row);
      });
  }

  function hasOtherMenu() {
    return !!document.querySelector(".cdk-overlay-container [role='menu']");
  }

  function findNativeMenuAction() {
    // Material's icon name avoids matching translated labels, including Vietnamese.
    const items = Array.from(
      document.querySelectorAll(".cdk-overlay-container [role='menuitem']")
    );
    const matches = items.filter(function (button) {
      return Array.from(button.querySelectorAll("mat-icon")).some(function (icon) {
        return (icon.textContent || "").trim() === "block";
      });
    });
    return matches.length === 1 ? matches[0] : null;
  }

  async function statusFor(taskId) {
    const current = (await PluginAPI.getTasks()).find(function (item) {
      return item.id === taskId;
    });
    if (current && current.isDone && current.wontDoOn != null
      && current.wontDoOn === current.doneOn) return "confirmed";
    if (current && current.isDone) return "unverified";
    return "pending";
  }

  async function activateMenuItem(taskId) {
    for (let attempt = 0; attempt < 12; attempt += 1) {
      await delay(90);
      const action = findNativeMenuAction();
      if (!action) continue;
      action.click();
      for (let verify = 0; verify < 12; verify += 1) {
        await delay(110);
        const status = await statusFor(taskId);
        if (status === "confirmed") return { status: "confirmed" };
        if (status === "unverified") {
          return { status: "unverified", reason: "The task became Done, not Won't Do." };
        }
      }
      return { status: "unverified", reason: "The native command was activated but not confirmed." };
    }
    return { status: "manual", reason: "Native Won't Do menu item was not found." };
  }

  async function menuFromRow(taskId) {
    const rows = getRows(taskId);
    if (rows.length !== 1 || hasOtherMenu()) {
      return { status: "manual", reason: "Native task row is unavailable or ambiguous." };
    }

    const row = rows[0];
    const rect = row.getBoundingClientRect();

    // Keyboard context-menu shortcut works on touch and desktop where enabled.
    // It avoids relying solely on a simulated right click (ignored on touch).
    row.focus();
    row.dispatchEvent(new KeyboardEvent("keydown", {
      bubbles: true, cancelable: true, key: "ContextMenu", code: "ContextMenu"
    }));

    for (let attempt = 0; attempt < 8; attempt += 1) {
      await delay(75);
      if (row.querySelector("task-context-menu-inner")
        && findNativeMenuAction()) break;
    }

    if (!findNativeMenuAction()) {
      // Desktop fallback: the host's task row listens for contextmenu.
      row.dispatchEvent(new MouseEvent("contextmenu", {
        bubbles: true, cancelable: true, button: 2,
        clientX: rect.left + Math.min(16, rect.width / 2),
        clientY: rect.top + Math.min(16, rect.height / 2)
      }));
    }

    for (let attempt = 0; attempt < 8; attempt += 1) {
      await delay(70);
      if (row.querySelector("task-context-menu-inner")) break;
    }

    if (!row.querySelector("task-context-menu-inner")) {
      return { status: "manual", reason: "The task's context menu did not open." };
    }
    return activateMenuItem(taskId);
  }

  async function menuFromDetail(taskId) {
    if (hasOtherMenu() || typeof PluginAPI.selectTask !== "function"
      || typeof PluginAPI.getSelectedTask !== "function") {
      return { status: "manual", reason: "Detail menu unavailable." };
    }

    // Touch/narrow layouts expose a native .task-detail-more-btn in the detail panel.
    await PluginAPI.selectTask(taskId);
    for (let attempt = 0; attempt < 14; attempt += 1) {
      await delay(85);
      const selected = await PluginAPI.getSelectedTask();
      if (!selected || selected.id !== taskId) {
        return { status: "manual", reason: "Selected task changed." };
      }
      const panels = Array.from(document.querySelectorAll("task-detail-panel"))
        .filter(visible);
      if (panels.length !== 1) continue;
      const more = panels[0].querySelector(".task-detail-more-btn");
      if (!visible(more)) continue;
      if (hasOtherMenu()) return { status: "manual", reason: "Another menu opened." };
      more.click();
      return activateMenuItem(taskId);
    }
    return { status: "manual", reason: "The task detail has no native menu button." };
  }

  async function waitForRow(taskId) {
    for (let attempt = 0; attempt < 42; attempt += 1) {
      const rows = getRows(taskId);
      if (rows.length === 1) return true;
      if (rows.length > 1) return false;
      await delay(80);
    }
    return false;
  }

  async function menuViaTemporaryTaskView(task) {
    const initialHash = window.location.hash;
    // Only navigate away from our own plugin page. Never hijack another view.
    const ownRoute = "#/plugins/" + PLUGIN_ID + "/index";
    if (initialHash !== ownRoute) {
      return { status: "manual", reason: "Not in the Today+ plugin view." };
    }

    let lastRoute = null;
    let result = { status: "manual", reason: "The task is not visible in native lists." };
    try {
      const destinations = ["#/tag/TODAY/tasks"];
      if (task.projectId) {
        destinations.push("#/project/" + encodeURIComponent(task.projectId) + "/tasks");
      }

      for (const route of destinations) {
        if (window.location.hash !== initialHash && window.location.hash !== lastRoute) {
          return { status: "manual", reason: "Navigation changed during the action." };
        }
        window.location.hash = route;
        lastRoute = route;
        if (!await waitForRow(task.id)) continue;
        result = await menuFromRow(task.id);
        if (result.status !== "manual" || hasOtherMenu()) break;
      }
      return result;
    } finally {
      // Do not override navigation performed by the user while the plugin worked.
      if (lastRoute && window.location.hash === lastRoute) {
        window.location.hash = initialHash;
        // The old iframe may already be gone; use a host notification instead.
        if (result.status === "confirmed") {
          PluginAPI.showSnack({ msg: "Today+: task marked Won't Do.", type: "SUCCESS" });
        } else if (result.status !== "unverified") {
          PluginAPI.showSnack({
            msg: "Today+: couldn't invoke Won't Do automatically. Open the task menu to skip it.",
            type: "WARNING"
          });
        } else {
          PluginAPI.showSnack({ msg: "Today+: check the task's Won't Do status.", type: "WARNING" });
        }
      }
    }
  }

  async function tryNativeWontDo(taskId) {
    if (typeof taskId !== "string" || !taskId || taskId.length > 256) {
      return { status: "manual", reason: "Invalid task identifier." };
    }
    if (pending) return { status: "manual", reason: "Another Won't Do request is running." };
    pending = true;
    try {
      const task = (await PluginAPI.getTasks()).find(function (item) {
        return item.id === taskId;
      });
      if (!task || task.isDone) {
        return { status: "unavailable", reason: "Task is missing or already finished." };
      }
      if (hasOtherMenu()) {
        return { status: "manual", reason: "Another task menu is open." };
      }

      if (getRows(taskId).length === 1) {
        const result = await menuFromRow(taskId);
        if (result.status !== "manual") return result;
      }

      // Mobile-first: select the task, then invoke the native menu in its detail panel.
      const detailResult = await menuFromDetail(taskId);
      if (detailResult.status !== "manual") return detailResult;

      // Desktop: Today+ occupies the plugin route, hiding native task rows.
      // Use the regular Today/project task view and return afterward.
      return await menuViaTemporaryTaskView(task);
    } finally {
      pending = false;
    }
  }

  if (typeof PluginAPI.onMessage === "function") {
    PluginAPI.onMessage(function (message) {
      if (!message || message.kind !== REQUEST_KIND) return null;
      return tryNativeWontDo(message.taskId);
    });
  }
})();
