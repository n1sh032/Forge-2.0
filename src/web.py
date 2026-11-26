import argparse
import os
import subprocess
from pathlib import Path

from src.web_runtime import serve


def git(root, *args):
    return subprocess.check_output(
        ["git", *args],
        cwd=root,
        text=True,
        encoding="utf-8",
        timeout=15,
    ).strip()


class ForgeApplication:
    actions = {"plan", "patch", "apply", "commit", "next"}

    def __init__(self):
        self.manager = None
        self.patch = None
        self.root = None

    def describe(self):
        return {"name": "Forge", "project": str(self.root) if self.root else None}

    def result(self, **extra):
        manager = self.manager
        return {
            "state": manager.get_state().value,
            "plan": manager.current_plan,
            "step": manager.current_step_index,
            **extra,
        }

    def execute(self, action, payload):
        from src.manager.manager import Manager
        from src.manager.state_machine import ForgeState
        from src.tools.diff_applier import apply_diff

        if action == "plan":
            if self.manager and self.manager.get_state() not in {
                ForgeState.DONE,
                ForgeState.FAILED,
            }:
                return {
                    "error": "Finish the current plan or restart Forge to choose a different project."
                }
            task = payload.get("task", "")
            raw_root = payload.get("project", "")
            if (
                not isinstance(task, str)
                or not task.strip()
                or len(task) > 4000
                or not isinstance(raw_root, str)
                or not raw_root
            ):
                return {
                    "error": "Enter a task and the absolute path to a clean linked worktree."
                }
            root = Path(raw_root)
            if not root.is_absolute():
                return {"error": "The project path must be absolute."}
            root = root.resolve()
            if root != Path(git(root, "rev-parse", "--show-toplevel")).resolve():
                return {"error": "Choose the root of a linked Git worktree."}
            if git(root, "status", "--porcelain") or git(
                root, "rev-parse", "--git-dir"
            ) == git(root, "rev-parse", "--git-common-dir"):
                return {"error": "Create a clean linked Git worktree first."}
            if not git(root, "branch", "--show-current"):
                return {"error": "The worktree needs a dedicated branch."}
            manager = Manager(project_root=str(root))
            manager.start_task(task.strip())
            manager.create_plan()
            self.root = root
            self.manager = manager
            return self.result()

        if self.manager is None:
            return {"error": "Create a plan first."}
        manager = self.manager
        state = manager.get_state()
        if action == "patch":
            if state == ForgeState.WAITING_FOR_PLAN_APPROVAL:
                manager.approve_plan()
                manager.approve_step()
            elif state == ForgeState.WAITING_FOR_STEP_APPROVAL:
                manager.approve_step()
            elif state == ForgeState.REPAIRING:
                manager.retry_coding()
            elif state != ForgeState.CODING:
                return {"error": "A patch cannot be generated in the current state."}
