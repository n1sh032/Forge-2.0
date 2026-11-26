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
