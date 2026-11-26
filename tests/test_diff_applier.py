import subprocess

from src.tools.diff_applier import apply_diff


def init_git_repo(path):
    subprocess.run(["git", "init"], cwd=path, capture_output=True)
    subprocess.run(["git", "config", "user.email", "test@test.com"], cwd=path, capture_output=True)
    subprocess.run(["git", "config", "user.name", "Test"], cwd=path, capture_output=True)


def test_apply_valid_diff_modifies_file(tmp_path):
    init_git_repo(tmp_path)

    target_file = tmp_path / "app.py"
