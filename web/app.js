"use strict";
const $ = (id) => document.getElementById(id);
let busy = false;
let revision = -1;
let latest = null;
async function send(action, payload = {}) {
  if (busy) return;
  try {
    const response = await fetch("/api/actions", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ action, payload }),
    });
    const result = await response.json();
    if (!response.ok) throw new Error(result.error);
    busy = true;
    updateButtons();
    $("status").textContent = "Working…";
  } catch (error) {
    $("status").textContent = error.message;
  }
}
function updateButtons() {
  const stage = latest?.state;
  $("plan").querySelector("button").disabled =
    busy || (stage && !["done", "failed"].includes(stage));
  $("patch").disabled =
    busy ||
    ![
      "waiting_for_plan_approval",
      "waiting_for_step_approval",
      "repairing",
      "coding",
    ].includes(stage);
  $("apply").disabled = busy || stage !== "coding" || !latest?.patch;
  $("commit").disabled = busy || stage !== "committing";
  $("next").disabled = busy || stage !== "final_review";
}
async function poll() {
  try {
    const response = await fetch("/api/state");
    if (!response.ok)
      throw new Error(
        "Could not reach the app. Open the address printed in its terminal.",
      );
    const state = await response.json();
    busy = state.busy;
    updateButtons();
    showInfo(state.application);
    if (revision !== state.revision) {
      revision = state.revision;
      if (state.error) $("status").textContent = state.error;
      else if (state.result) {
        latest = state.result;
        $("status").textContent =
          latest.error || (latest.kind === "error" ? latest.message : "Ready");
        render(latest);
        updateButtons();
      } else $("status").textContent = "Ready";
    }
    if (busy) $("status").textContent = "Working…";
  } catch (error) {
    $("status").textContent = error.message;
  } finally {
    setTimeout(poll, 750);
  }
}
let files = [];
function showInfo(app) {
  $("connection").textContent = app.project || "No worktree selected";
}
function render(r) {
  if (r.error) return;
  $("stage").textContent = (r.state || "Plan").replaceAll("_", " ");
  files = r.files || [];
  $("approve-files").checked = false;
  const evidence = [
    r.plan ? JSON.stringify(r.plan, null, 2) : "",
    r.patch || "",
    r.output || "",
    r.diff || "",
    files.length ? "Changed files:\n" + files.join("\n") : "",
  ]
    .filter(Boolean)
    .join("\n\n");
  const fragment = document.createDocumentFragment();
  for (const line of evidence.split("\n")) {
    const row = document.createElement("span");
    row.textContent = line + "\n";
    if (line.startsWith("+") && !line.startsWith("+++"))
      row.className = "diff-added";
    if (line.startsWith("-") && !line.startsWith("---"))
      row.className = "diff-removed";
    if (line.startsWith("@@")) row.className = "diff-context";
    fragment.append(row);
  }
  $("output").replaceChildren(fragment);
}
$("plan").addEventListener("submit", (e) => {
  e.preventDefault();
  send("plan", { project: $("project").value, task: $("task").value });
});
$("patch").addEventListener("click", () => send("patch"));
$("apply").addEventListener("click", () => {
  if (confirm("Apply the displayed patch and execute the project's tests?"))
    send("apply");
});
$("commit").addEventListener("click", () => {
  if (!$("approve-files").checked) {
    $("status").textContent = "Review and approve the changed files first.";
    return;
  }
  send("commit", { files });
});
$("next").addEventListener("click", () => send("next"));
poll();
