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


