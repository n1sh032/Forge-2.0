from types import SimpleNamespace
from unittest.mock import Mock

from src.manager import manager as module
from src.manager.state_machine import ForgeState
from src.tools.diff_applier import DiffResult
from src.tools.tester import TestResult as CheckResult


