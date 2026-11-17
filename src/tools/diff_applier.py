import subprocess
import tempfile
import os
from pathlib import Path

from src.tools.project_paths import project_path


class DiffResult:

    def __init__(self, success, message):
        self.success = success
        self.message = message


def apply_diff(diff_text, project_root="."):
    """
    Validates and applies a unified diff to files in project_root.

    Uses `git apply --check` first to validate without touching any
    files. Only writes to disk if the check passes. Returns a
    DiffResult describing what happened - never raises on a bad diff,
    since a malformed diff from an LLM is an expected, recoverable
    situation, not a bug in this code.
    """

    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".diff", delete=False, encoding="utf-8"
    ) as temp_file:
        temp_file.write(diff_text)
        temp_path = temp_file.name

    try:
        root = Path(project_root).resolve()
        top = subprocess.run(
            ["git", "rev-parse", "--show-toplevel"], cwd=root,
            capture_output=True, text=True,
        )
        if top.returncode or Path(top.stdout.strip()).resolve() != root:
            return DiffResult(False, "Target must be the root of a Git worktree")
        summary = subprocess.run(
            ["git", "apply", "--numstat", "-z", temp_path], cwd=root,
            capture_output=True,
        )
        if summary.returncode or not summary.stdout:
            return DiffResult(False, "Diff has no valid file changes")
        try:
            for record in summary.stdout.rstrip(b"\0").split(b"\0"):
                _, _, name = record.split(b"\t", 2)
                project_path(root, name.decode("utf-8"))
        except (ValueError, OSError) as exc:
            return DiffResult(False, str(exc))
        if any(line.startswith(("new file mode 120000", "new mode 120000", "new file mode 160000", "new mode 160000")) for line in diff_text.splitlines()):
            return DiffResult(False, "Generated symbolic links and submodules are not supported")

        check = subprocess.run(
            ["git", "apply", "--check", temp_path],
            cwd=project_root,
            capture_output=True,
            text=True
        )

        if check.returncode != 0:
            return DiffResult(
                success=False,
                message=f"Diff failed validation:\n{check.stderr}"
            )

        apply = subprocess.run(
            ["git", "apply", temp_path],
            cwd=project_root,
            capture_output=True,
            text=True
        )

        if apply.returncode != 0:
            return DiffResult(
                success=False,
                message=f"Diff passed validation but failed to apply:\n{apply.stderr}"
            )

        return DiffResult(success=True, message="Diff applied successfully")

    finally:
        os.remove(temp_path)
