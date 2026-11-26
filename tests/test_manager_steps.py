import pytest

from src.manager.manager import Manager
from src.agents.architect import Architect


class FakeProvider:
    def ask(self, prompt):
        return '["Step one", "Step two", "Step three"]'
