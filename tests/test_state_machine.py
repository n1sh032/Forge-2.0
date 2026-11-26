import pytest

from src.manager.state_machine import ForgeState, StateMachine


def test_start_planning():

    machine = StateMachine()

    assert machine.get_state() == ForgeState.IDLE

    machine.transition("start")

    assert machine.get_state() == ForgeState.PLANNING

