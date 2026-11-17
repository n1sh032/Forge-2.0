import subprocess
from src.tools.project_paths import project_path


class CommitResult:

    def __init__(self, success, message):
        self.success = success
        self.message = message


def commit_changes(project_root, commit_message, approved_paths=()):
    """
    Stages explicitly reviewed files and commits them with the given message.

    Deterministic - no LLM involved here, just running git. The
    message itself is expected to already be generated elsewhere.
    """

    if not approved_paths or isinstance(approved_paths, str):
        return CommitResult(False, "Review the diff and supply approved file paths")
    try:
        for path in approved_paths:
            if project_path(project_root, path).is_dir():
                return CommitResult(False, "Approve individual files, not directories")
    except (ValueError, OSError) as exc:
        return CommitResult(False, str(exc))
    staged = subprocess.run(
        ["git", "diff", "--cached", "--quiet"], cwd=project_root,
        capture_output=True,
    )
    if staged.returncode:
        return CommitResult(False, "Commit requires an empty Git index")
    add = subprocess.run(
        ["git", "--literal-pathspecs", "add", "--", *approved_paths],
        cwd=project_root,
        capture_output=True,
        text=True
    )

    if add.returncode != 0:
        return CommitResult(success=False, message=f"git add failed:\n{add.stderr}")

    commit = subprocess.run(
        ["git", "commit", "-m", commit_message],
        cwd=project_root,
        capture_output=True,
        text=True
    )

    if commit.returncode != 0:
        return CommitResult(success=False, message=f"git commit failed:\n{commit.stderr}")

    return CommitResult(success=True, message=f"Committed: {commit_message}")
