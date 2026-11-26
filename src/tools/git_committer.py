import subprocess


class CommitResult:

    def __init__(self, success, message):
        self.success = success
        self.message = message


def commit_changes(project_root, commit_message):
    """
    Stages all changes and commits them with the given message.

    Deterministic - no LLM involved here, just running git. The
    message itself is expected to already be generated elsewhere.
    """

    add = subprocess.run(
        ["git", "add", "-A"],
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