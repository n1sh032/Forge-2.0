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
