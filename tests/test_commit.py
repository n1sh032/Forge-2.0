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

