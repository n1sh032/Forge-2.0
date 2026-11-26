from src.manager.manager import Manager
from src.agents.architect import Architect
from src.agents.coder import Coder
import subprocess


class FakeArchitectProvider:
    def ask(self, prompt):
        return '["Change old line to new line"]'


class SucceedingCoderProvider:
    def __init__(self):
        self.calls = 0

    def ask(self, prompt):
        self.calls += 1
        if self.calls == 1:
            return '["app.py"]'
        else:
            return (
                "diff --git a/app.py b/app.py\n"
                "index 0000000..1111111 100644\n"
                "--- a/app.py\n"
                "+++ b/app.py\n"
                "@@ -1 +1 @@\n"
                "-old line\n"
                "+new line\n"
            )


class FailingCoderProvider:
    def ask(self, prompt):
        return "this is not a valid diff"


def setup_manager(tmp_path, coder_provider):
    project_root = tmp_path
    app_file = project_root / "app.py"
    app_file.write_text("old line\n")


    subprocess.run(["git", "init"], cwd=project_root, capture_output=True)
    subprocess.run(["git", "config", "user.email", "test@test.com"], cwd=project_root, capture_output=True)
    subprocess.run(["git", "config", "user.name", "Test"], cwd=project_root, capture_output=True)
    subprocess.run(["git", "add", "."], cwd=project_root, capture_output=True)
    subprocess.run(["git", "commit", "-m", "initial"], cwd=project_root, capture_output=True)


    manager = Manager(
        architect=Architect(provider=FakeArchitectProvider()),
        coder=Coder(provider=coder_provider, project_root=str(project_root)),
        project_root=str(project_root)
    )

    manager.start_task("Fix the line")
    manager.create_plan()
    manager.approve_plan()
    manager.approve_step()

    return manager, app_file


def test_run_step_success(tmp_path):

    manager, app_file = setup_manager(tmp_path, SucceedingCoderProvider())

    result = manager.run_step()

    assert result.success is True
    assert app_file.read_text() == "new line\n"

