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
