import subprocess
import tempfile
import os


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