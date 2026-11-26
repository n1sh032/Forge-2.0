from src.manager.manager import Manager
from src.manager.state_machine import ForgeState


def test_manager_starts_task():

    manager = Manager()

    manager.start_task("Build a calculator")

    assert manager.get_task() == "Build a calculator"
    assert manager.get_state() == ForgeState.PLANNING


def test_manager_approval_flow():

    manager = Manager()

    manager.start_task("Build a calculator")
    manager.plan_ready()

    assert manager.get_state() == ForgeState.WAITING_FOR_PLAN_APPROVAL

    manager.approve_plan()

    assert manager.get_state() == ForgeState.WAITING_FOR_STEP_APPROVAL

    manager.approve_step()

    assert manager.get_state() == ForgeState.CODING


def test_manager_coding_and_testing():

    manager = Manager()

    manager.start_task("Build a calculator")
    manager.plan_ready()
    manager.approve_plan()
    manager.approve_step()
    manager.coding_done()

    assert manager.get_state() == ForgeState.TESTING

    manager.tests_passed()

    assert manager.get_state() == ForgeState.COMMITTING