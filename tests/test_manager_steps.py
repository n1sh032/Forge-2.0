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


def test_get_current_step_before_plan_raises():

    manager = Manager()

    with pytest.raises(ValueError):
        manager.get_current_step()


def test_next_step_advances_index():

    manager = Manager(architect=Architect(provider=FakeProvider()))

    manager.start_task("Build a calculator")
    manager.create_plan()
    manager.approve_plan()
    manager.approve_step()
    manager.coding_done()
    manager.tests_passed()
    manager.commit_done()
    manager.next_step()

    assert manager.get_current_step() == "Step two"