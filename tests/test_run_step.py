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

