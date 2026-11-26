from src.manager.manager import Manager
from src.manager.state_machine import ForgeState


def test_manager_starts_task():

    manager = Manager()

    manager.start_task("Build a calculator")

    assert manager.get_task() == "Build a calculator"
    assert manager.get_state() == ForgeState.PLANNING
