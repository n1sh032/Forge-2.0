import pytest

from src.manager.manager import Manager
from src.agents.architect import Architect


class FakeProvider:
    def ask(self, prompt):
        return '["Step one", "Step two", "Step three"]'


def test_get_current_step_returns_first_step():

    manager = Manager(architect=Architect(provider=FakeProvider()))

    manager.start_task("Build a calculator")
    manager.create_plan()

    assert manager.get_current_step() == "Step one"


