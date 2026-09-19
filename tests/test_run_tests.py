from src.manager.manager import Manager
from src.manager.state_machine import ForgeState
from src.agents.architect import Architect
from src.agents.coder import Coder
import subprocess


class FakeArchitectProvider:
    def ask(self, prompt):
        return '["Add a passing test"]'


class FakeCoderProvider:
    def __init__(self, diff_text):
        self.calls = 0
        self.diff_text = diff_text

    def ask(self, prompt):
        self.calls += 1
        if self.calls % 2 == 1:
            return '["test_sample.py"]'
        else:
            return self.diff_text


def init_git_repo(project_root):
    subprocess.run(["git", "init"], cwd=project_root, capture_output=True)
    subprocess.run(["git", "config", "user.email", "test@test.com"], cwd=project_root, capture_output=True)
    subprocess.run(["git", "config", "user.name", "Test"], cwd=project_root, capture_output=True)
    subprocess.run(["git", "add", "."], cwd=project_root, capture_output=True)
    subprocess.run(["git", "commit", "-m", "initial"], cwd=project_root, capture_output=True)


def get_to_testing(tmp_path, diff_text):
    project_root = tmp_path
    test_file = project_root / "test_sample.py"
    test_file.write_text("")

    init_git_repo(project_root)

    manager = Manager(
        architect=Architect(provider=FakeArchitectProvider()),
        coder=Coder(provider=FakeCoderProvider(diff_text), project_root=str(project_root)),
        project_root=str(project_root)
    )

    manager.start_task("Add a test")
    manager.create_plan()
    manager.approve_plan()
    manager.approve_step()
    manager.run_step()

    return manager, test_file


def test_run_tests_passes_moves_to_committing(tmp_path):

    diff = (
        "diff --git a/test_sample.py b/test_sample.py\n"
        "index 0000000..1111111 100644\n"
        "--- a/test_sample.py\n"
        "+++ b/test_sample.py\n"
        "@@ -0,0 +1,2 @@\n"
        "+def test_ok():\n"
        "+    assert True\n"
    )

    manager, test_file = get_to_testing(tmp_path, diff)

    assert manager.get_state() == ForgeState.TESTING

    result = manager.run_tests()

    assert result.passed is True
    assert manager.get_state() == ForgeState.COMMITTING


def test_run_tests_fails_moves_to_repairing(tmp_path):

    diff = (
        "diff --git a/test_sample.py b/test_sample.py\n"
        "index 0000000..1111111 100644\n"
        "--- a/test_sample.py\n"
        "+++ b/test_sample.py\n"
        "@@ -0,0 +1,2 @@\n"
        "+def test_broken():\n"
        "+    assert False\n"
    )

    manager, test_file = get_to_testing(tmp_path, diff)

    result = manager.run_tests()

    assert result.passed is False
    assert manager.get_state() == ForgeState.REPAIRING