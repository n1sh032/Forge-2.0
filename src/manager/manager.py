from .state_machine import ForgeState, StateMachine


class Manager:

    def __init__(self):
        self.state_machine = StateMachine()
        self.current_task = None

    def start_task(self, task):
        if self.state_machine.get_state() != ForgeState.IDLE:
            raise ValueError("Manager is already working on a task")

        self.current_task = task
        self.state_machine.transition("start")

    def get_state(self):
        return self.state_machine.get_state()
