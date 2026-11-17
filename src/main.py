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
    if not branch or common == local:
        raise ValueError("Use a linked Git worktree on a dedicated branch")

    manager = Manager(project_root=project)
    manager.start_task(task)
    plan = manager.create_plan()
    print(json.dumps(plan, indent=2))
    if not approve("Approve this plan?"):
        return 1
    manager.approve_plan()

    for index, step in enumerate(plan["steps"], 1):
        if not approve(f"Start step {index}: {step}"):
            return 1
        manager.approve_step()
        while manager.get_state() == ForgeState.CODING:
            result = manager.run_step(review_patch=review_patch)
            if result is None:
                return 1
            print(result.message)
            if result.success:
                result = manager.run_tests()
                print(result.output)
            if manager.get_state() == ForgeState.REPAIRING:
                if not approve("Request another patch?"):
                    return 1
                manager.retry_coding()

        if manager.get_state() != ForgeState.COMMITTING:
            return 1
        print(git_output(project, "diff", "--no-ext-diff"))
        paths = set(git_output(project, "diff", "--no-renames", "--name-only", "-z").split("\0"))
        paths.update(git_output(project, "ls-files", "--others", "--exclude-standard", "-z").split("\0"))
        paths.discard("")
        for path in sorted(paths):
            print(f"Changed file: {path}")
        if not paths or not approve("Commit exactly these files?"):
            return 1
        result = manager.commit(sorted(paths))
        print(result.message)
        if not result.success:
            return 1
        if index < len(plan["steps"]):
            manager.next_step()
    manager.finish()
    return 0


def main():
    parser = argparse.ArgumentParser(description="Draft or run a Forge plan with review")
    parser.add_argument("task")
    parser.add_argument("--project", type=Path, help="clean linked Git worktree to change")
    args = parser.parse_args()
    if args.project:
        try:
            return run_project(args.project.resolve(), args.task)
        except (OSError, ValueError, subprocess.CalledProcessError, EOFError) as exc:
            parser.exit(1, f"Forge stopped: {exc}\n")
    print(json.dumps(Architect().run(args.task), indent=2))


if __name__ == "__main__":
    raise SystemExit(main())
