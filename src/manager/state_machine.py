from enum import Enum


class ForgeState(Enum):
    IDLE = "idle"
    PLANNING = "planning"
    WAITING_FOR_PLAN_APPROVAL = "waiting_for_plan_approval"
    WAITING_FOR_STEP_APPROVAL = "waiting_for_step_approval"
    CODING = "coding"
    TESTING = "testing"
    REPAIRING = "repairing"
    COMMITTING = "committing"
    FINAL_REVIEW = "final_review"
    DONE = "done"
    FAILED = "failed"


class StateMachine:

    def __init__(self):
        self.state = ForgeState.IDLE

    def transition(self, event):
        transitions = {
            ForgeState.IDLE: {
                "start": ForgeState.PLANNING
            },

            ForgeState.PLANNING: {
                "plan_ready": ForgeState.WAITING_FOR_PLAN_APPROVAL,
                "fail": ForgeState.FAILED
            },

            ForgeState.WAITING_FOR_PLAN_APPROVAL: {
                "approve_plan": ForgeState.WAITING_FOR_STEP_APPROVAL,
                "reject_plan": ForgeState.PLANNING
            },

            ForgeState.WAITING_FOR_STEP_APPROVAL: {
                "approve_step": ForgeState.CODING,
                "reject_step": ForgeState.WAITING_FOR_STEP_APPROVAL
            },

            ForgeState.CODING: {
                "coding_done": ForgeState.TESTING,
                "apply_failed": ForgeState.REPAIRING,
                "fail": ForgeState.FAILED
            },

            ForgeState.TESTING: {
                "tests_passed": ForgeState.COMMITTING,
                "tests_failed": ForgeState.REPAIRING,
                "fail": ForgeState.FAILED
            },

            ForgeState.REPAIRING: {
                "repair_done": ForgeState.TESTING,
                "retry_coding": ForgeState.CODING,
                "fail": ForgeState.FAILED
            },

            ForgeState.COMMITTING: {
                "commit_done": ForgeState.FINAL_REVIEW,
                "fail": ForgeState.FAILED
            },

            ForgeState.FINAL_REVIEW: {
                "more_steps": ForgeState.WAITING_FOR_STEP_APPROVAL,
                "finished": ForgeState.DONE,
                "fail": ForgeState.FAILED
            },

            ForgeState.DONE: {},
            ForgeState.FAILED: {}
        }

        if event not in transitions[self.state]:
            raise ValueError(
                f"Cannot perform '{event}' while in {self.state.value}"
            )

        self.state = transitions[self.state][event]

    def get_state(self):
        return self.state