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
