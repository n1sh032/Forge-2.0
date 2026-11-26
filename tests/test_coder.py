from src.agents.coder import Coder


class FakeProvider:
    def __init__(self):
        self.calls = 0

    def ask(self, prompt):
        self.calls += 1
