from .state_machine import ForgeState, StateMachine


class Manager:

    def __init__(self):
        self.state_machine = StateMachine()
        self.current_task = None

