from src.manager.manager import Manager
from src.manager.state_machine import ForgeState
from src.agents.architect import Architect


class FakeProvider:
    def ask(self, prompt):
        return '["Understand the requirements", "Design the solution", "Implement the solution", "Test the solution"]'


def test_manager_starts_task():

    manager = Manager()

    manager.start_task("Build a calculator")

    assert manager.get_task() == "Build a calculator"
    assert manager.get_state() == ForgeState.PLANNING


def test_manager_approval_flow():

    manager = Manager(architect=Architect(provider=FakeProvider()))

    manager.start_task("Build a calculator")
    manager.create_plan()

    assert manager.get_state() == ForgeState.WAITING_FOR_PLAN_APPROVAL

    manager.approve_plan()

    assert manager.get_state() == ForgeState.WAITING_FOR_STEP_APPROVAL

    manager.approve_step()

    assert manager.get_state() == ForgeState.CODING


def test_manager_coding_and_testing():

    manager = Manager(architect=Architect(provider=FakeProvider()))

    manager.start_task("Build a calculator")
    manager.create_plan()
    manager.approve_plan()
    manager.approve_step()
    manager.coding_done()

    assert manager.get_state() == ForgeState.TESTING

    manager.tests_passed()

    assert manager.get_state() == ForgeState.COMMITTING


def test_manager_creates_plan():

    manager = Manager(architect=Architect(provider=FakeProvider()))

    manager.start_task("Build a calculator")

    plan = manager.create_plan()

    assert plan["task"] == "Build a calculator"
    assert len(plan["steps"]) > 0
    assert manager.get_state() == ForgeState.WAITING_FOR_PLAN_APPROVAL