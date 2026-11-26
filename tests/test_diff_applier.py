import subprocess

from src.tools.diff_applier import apply_diff
from src.tools.project_paths import project_path
import pytest


@pytest.mark.parametrize("name", ["../outside.py", ".git/config", ".env", "C:/outside.py"])
def test_generated_paths_stay_in_project(tmp_path, name):
    with pytest.raises(ValueError):
        project_path(tmp_path, name)


def init_git_repo(path):
    subprocess.run(["git", "init"], cwd=path, capture_output=True)
    subprocess.run(["git", "config", "user.email", "test@test.com"], cwd=path, capture_output=True)
    subprocess.run(["git", "config", "user.name", "Test"], cwd=path, capture_output=True)


def test_apply_valid_diff_modifies_file(tmp_path):
    init_git_repo(tmp_path)

    target_file = tmp_path / "app.py"
    target_file.write_text("old line\n")

    subprocess.run(["git", "add", "."], cwd=tmp_path, capture_output=True)
    subprocess.run(["git", "commit", "-m", "initial"], cwd=tmp_path, capture_output=True)

    diff = (
        "diff --git a/app.py b/app.py\n"
        "index 0000000..1111111 100644\n"
        "--- a/app.py\n"
        "+++ b/app.py\n"
        "@@ -1 +1 @@\n"
        "-old line\n"
        "+new line\n"
    )

    result = apply_diff(diff, project_root=str(tmp_path))

    assert result.success is True
    assert target_file.read_text() == "new line\n"


def test_apply_invalid_diff_does_not_modify_file(tmp_path):
    init_git_repo(tmp_path)

    target_file = tmp_path / "app.py"
    target_file.write_text("old line\n")

    subprocess.run(["git", "add", "."], cwd=tmp_path, capture_output=True)
    subprocess.run(["git", "commit", "-m", "initial"], cwd=tmp_path, capture_output=True)

    bad_diff = "this is not a real diff at all"

    result = apply_diff(bad_diff, project_root=str(tmp_path))

    assert result.success is False
    assert target_file.read_text() == "old line\n"