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

    def get_task(self):
        return self.current_task

    def plan_ready(self):
        self.state_machine.transition("plan_ready")

    def approve_plan(self):
        self.state_machine.transition("approve_plan")

    def approve_step(self):
        self.state_machine.transition("approve_step")

    def coding_done(self):
        self.state_machine.transition("coding_done")

    def tests_passed(self):
        self.state_machine.transition("tests_passed")

    def tests_failed(self):
        self.state_machine.transition("tests_failed")

    def repair_done(self):
        self.state_machine.transition("repair_done")

    def commit_done(self):
        self.state_machine.transition("commit_done")

    def next_step(self):
        self.state_machine.transition("more_steps")

    def finish(self):
        self.state_machine.transition("finished")