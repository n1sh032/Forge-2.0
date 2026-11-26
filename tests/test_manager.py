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

