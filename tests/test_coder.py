from src.agents.coder import Coder


class FakeProvider:
    def __init__(self):
        self.calls = 0

    def ask(self, prompt):
        self.calls += 1
        if self.calls == 1:
            return '["app.py"]'
        else:
            return "--- a/app.py\n+++ b/app.py\n@@ -1 +1 @@\n-old line\n+new line\n"


def test_coder_picks_and_reads_relevant_file(tmp_path):
    app_file = tmp_path / "app.py"
    app_file.write_text("old line\n")

    coder = Coder(provider=FakeProvider(), project_root=str(tmp_path))

    diff = coder.run("change old line to new line")

    assert "new line" in diff


class NewFileProvider:
    def __init__(self):
        self.calls = 0

    def ask(self, prompt):
        self.calls += 1
        if self.calls == 1:
            return '["login.py"]'
        else:
            assert "does not exist yet" in prompt
            return "+++ b/login.py\n@@ -0,0 +1 @@\n+print('login')\n"


def test_coder_handles_new_file(tmp_path):

    coder = Coder(provider=NewFileProvider(), project_root=str(tmp_path))

    diff = coder.run("create a login file")

    assert "login.py" in diff