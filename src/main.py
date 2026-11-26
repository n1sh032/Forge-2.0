import argparse
import json
import subprocess
from pathlib import Path

from src.agents.architect import Architect
from src.manager.manager import Manager
from src.manager.state_machine import ForgeState


def git_output(project, *args):
    return subprocess.check_output(["git", *args], cwd=project, text=True, encoding="utf-8")


def approve(prompt):
    return input(f"{prompt} [y/N] ").strip().lower() == "y"


def review_patch(diff):
    print(diff)
    return approve("Apply this patch and run the project's pytest suite?")


def run_project(project, task):
    root = Path(git_output(project, "rev-parse", "--show-toplevel").strip()).resolve()
    if project != root or git_output(project, "status", "--porcelain"):
        raise ValueError("Provide the root of a clean dedicated Git worktree")
    branch = git_output(project, "branch", "--show-current").strip()
    common = git_output(project, "rev-parse", "--git-common-dir").strip()
    local = git_output(project, "rev-parse", "--git-dir").strip()
