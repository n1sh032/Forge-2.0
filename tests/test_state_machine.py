import pytest

from src.manager.state_machine import ForgeState, StateMachine


def test_start_planning():

    machine = StateMachine()

    assert machine.get_state() == ForgeState.IDLE

    machine.transition("start")

    assert machine.get_state() == ForgeState.PLANNING


def test_plan_approval():

    machine = StateMachine()

    machine.transition("start")
    machine.transition("plan_ready")

    assert machine.get_state() == ForgeState.WAITING_FOR_PLAN_APPROVAL

    machine.transition("approve_plan")

    assert machine.get_state() == ForgeState.WAITING_FOR_STEP_APPROVAL


def test_step_approval():

    machine = StateMachine()

    machine.transition("start")
    machine.transition("plan_ready")
    machine.transition("approve_plan")
    machine.transition("approve_step")

