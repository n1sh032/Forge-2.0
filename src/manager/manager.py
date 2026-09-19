from .state_machine import ForgeState, StateMachine
from src.agents.architect import Architect
from src.agents.coder import Coder
from src.tools.diff_applier import apply_diff
from src.tools.tester import run_tests
from src.tools.git_committer import commit_changes



class Manager:

    def __init__(self, architect=None, coder=None, project_root=".", max_repair_attempts=3):
        self.state_machine = StateMachine()
        self.project_root = project_root
        self.architect = architect or Architect()
        self.coder = coder or Coder(project_root=project_root)

        self.current_task = None
        self.current_plan = None
        self.current_step_index = 0
        self.repair_attempts = 0
        self.max_repair_attempts = max_repair_attempts

    def start_task(self, task):

        if self.state_machine.get_state() != ForgeState.IDLE:
            raise ValueError("Manager is already working on a task")

        self.current_task = task
        self.state_machine.transition("start")

    def create_plan(self):

        if self.state_machine.get_state() != ForgeState.PLANNING:
            raise ValueError("Manager is not currently planning")

        self.current_plan = self.architect.run(self.current_task)

        self.state_machine.transition("plan_ready")

        return self.current_plan

    def get_current_step(self):

        if self.current_plan is None:
            raise ValueError("No plan exists yet")

        steps = self.current_plan["steps"]

        if self.current_step_index >= len(steps):
            raise ValueError("No more steps remaining in the plan")

        return steps[self.current_step_index]

    def run_step(self):

        if self.state_machine.get_state() != ForgeState.CODING:
            raise ValueError("Manager is not currently in the CODING state")

        step = self.get_current_step()
        diff = self.coder.run(step)
        result = apply_diff(diff, project_root=self.project_root)

        if result.success:
            self.repair_attempts = 0
            self.state_machine.transition("coding_done")
            return result

        self.repair_attempts += 1

        if self.repair_attempts >= self.max_repair_attempts:
            self.state_machine.transition("fail")
        else:
            self.state_machine.transition("apply_failed")

        return result

    def run_tests(self):

        if self.state_machine.get_state() != ForgeState.TESTING:
            raise ValueError("Manager is not currently in the TESTING state")

        result = run_tests(project_root=self.project_root)

        if result.passed:
            self.repair_attempts = 0
            self.state_machine.transition("tests_passed")
            return result

        self.repair_attempts += 1

        if self.repair_attempts >= self.max_repair_attempts:
            self.state_machine.transition("fail")
        else:
            self.state_machine.transition("tests_failed")

        return result

    def commit(self):

        if self.state_machine.get_state() != ForgeState.COMMITTING:
            raise ValueError("Manager is not currently in the COMMITTING state")

        message = self.architect.generate_commit_message(self.get_current_step())
        result = commit_changes(self.project_root, message)

        if result.success:
            self.state_machine.transition("commit_done")
        else:
            self.state_machine.transition("fail")

        return result

    def retry_coding(self):
        self.state_machine.transition("retry_coding")

    def get_state(self):
        return self.state_machine.get_state()

    def get_task(self):
        return self.current_task

    def get_plan(self):
        return self.current_plan

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
        self.current_step_index += 1

    def finish(self):
        self.state_machine.transition("finished")