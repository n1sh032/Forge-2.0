import subprocess

from src.manager.manager import Manager
from src.manager.state_machine import ForgeState
from src.agents.architect import Architect
from src.agents.coder import Coder


class FakeArchitectProvider:
    def __init__(self):
        self.calls = 0

    def ask(self, prompt):
        self.calls += 1
        if self.calls == 1:
            return '["Add a passing test"]'
        else:
            return "feat: add a passing test"


class FakeCoderProvider:
    def __init__(self):
        self.calls = 0

    def ask(self, prompt):
        self.calls += 1
        if self.calls % 2 == 1:
            return '["test_sample.py"]'
        else:
            return (
                "diff --git a/test_sample.py b/test_sample.py\n"
                "index 0000000..1111111 100644\n"
                "--- a/test_sample.py\n"
                "+++ b/test_sample.py\n"
                "@@ -0,0 +1,2 @@\n"
                "+def test_ok():\n"
                "+    assert True\n"
            )


def init_git_repo(project_root):
    subprocess.run(["git", "init"], cwd=project_root, capture_output=True)
    subprocess.run(["git", "config", "user.email", "test@test.com"], cwd=project_root, capture_output=True)
    subprocess.run(["git", "config", "user.name", "Test"], cwd=project_root, capture_output=True)
    subprocess.run(["git", "add", "."], cwd=project_root, capture_output=True)
    subprocess.run(["git", "commit", "-m", "initial"], cwd=project_root, capture_output=True)


def test_commit_creates_git_commit(tmp_path):
    project_root = tmp_path
    test_file = project_root / "test_sample.py"
    test_file.write_text("")

    init_git_repo(project_root)

    manager = Manager(
        architect=Architect(provider=FakeArchitectProvider()),
        coder=Coder(provider=FakeCoderProvider(), project_root=str(project_root)),
        project_root=str(project_root)
    )

    manager.start_task("Add a test")
    manager.create_plan()
    manager.approve_plan()
    manager.approve_step()
    manager.run_step()
    manager.run_tests()

    assert manager.get_state() == ForgeState.COMMITTING

    result = manager.commit()

    assert result.success is True
    assert manager.get_state() == ForgeState.FINAL_REVIEW

    log = subprocess.run(
        ["git", "log", "-1", "--pretty=%s"],
        cwd=project_root,
        capture_output=True,
        text=True
    )
    assert log.stdout.strip() == "feat: add a passing test"