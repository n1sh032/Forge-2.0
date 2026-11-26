from types import SimpleNamespace
from unittest.mock import Mock

from src.manager import manager as module
from src.manager.state_machine import ForgeState
from src.tools.diff_applier import DiffResult
from src.tools.tester import TestResult as CheckResult


def test_patches_that_apply_cannot_reset_failed_test_budget(monkeypatch):
    manager = module.Manager(
        architect=SimpleNamespace(run=lambda task: {"steps": ["write patch"]}),
        coder=SimpleNamespace(run=Mock(return_value="patch")),
        max_repair_attempts=2,
    )
    monkeypatch.setattr(module, "apply_diff", lambda *args, **kwargs: DiffResult(True, "applied"))
    monkeypatch.setattr(module, "run_tests", lambda **kwargs: CheckResult(False, "failed"))
    manager.start_task("task")
    manager.create_plan()
    manager.approve_plan()
    manager.approve_step()

    manager.run_step()
    manager.coder.run.assert_called_once_with("write patch")
