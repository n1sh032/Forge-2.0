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
